#!/usr/bin/env python3
"""
Phase 1 预采集 Python 脚本 — 并行获取 Coding Bug 信息
=====================================================
替代浏览器自动化，使用 Coding REST API / Open API 并行抓取 Bug 详情和评论。
输出格式与现有 Phase 1 完全兼容（metadata.json / detail.txt / comments.txt / prefetch-summary.json）。

用法:
  # 从筛选器 URL 抓取（默认并发 5）
  python3 prefetch.py --filter "https://yldc.coding.yili.com/p/fssc/all/issues?filter=..."

  # 抓取分配给我的 Bug
  python3 prefetch.py --mine

  # 指定并发数 + 强制刷新已有数据
  python3 prefetch.py --mine --workers 8 --force

  # 仅抓取指定 Bug（逗号分隔）
  python3 prefetch.py --bugs 5186,5200,5399

  # 空跑模式（只获取列表，不抓详情）
  python3 prefetch.py --mine --dry-run

认证方式（按优先级）:
  1. Personal Access Token (coding-auth.yaml 中 personal_access_token 字段)
  2. Cookie 文件 (config/coding-cookies.json，由 browser-use 导出)
  3. 交互式 SSO 登录（自动获取 session）

依赖:
  pip3 install requests pyyaml --user --break-system-packages

@author sevenxiao
"""

import os
import sys
import json
import re
import time
import argparse
import logging
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, parse_qs, urljoin
from typing import Optional

try:
    import requests
except ImportError:
    print("错误: 缺少 requests 库，请执行: pip3 install requests --user --break-system-packages")
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("错误: 缺少 pyyaml 库，请执行: pip3 install pyyaml --user --break-system-packages")
    sys.exit(1)

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------
# 项目根目录（相对于脚本位置向上 5 级）
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[4]  # ai-spec/skills/code/bug-fix-cycle/bug-fix-pipeline/scripts → 项目根

CONFIG_PATH = PROJECT_ROOT / "ai-spec/skills/code/bug-fix-cycle/coding-bug-ops/config/coding-auth.yaml"
COOKIE_PATH = PROJECT_ROOT / "ai-spec/skills/code/bug-fix-cycle/coding-bug-ops/config/coding-cookies.json"
OUTPUT_DIR = PROJECT_ROOT / "yili-out/bug-prefetch"

# Coding 项目标识
CODING_PROJECT = "fssc"

# 优先级映射（Coding API 返回的优先级值 → 中文）
PRIORITY_MAP = {
    "0": "低",
    "1": "中",
    "2": "高",
    "3": "紧急",
    "low": "低",
    "medium": "中",
    "high": "高",
    "critical": "紧急",
}

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("prefetch")


# ---------------------------------------------------------------------------
# 配置加载
# ---------------------------------------------------------------------------
class Config:
    """从 coding-auth.yaml 加载认证配置"""

    def __init__(self, config_path: Path = CONFIG_PATH):
        if not config_path.exists():
            raise FileNotFoundError(
                f"认证配置文件不存在: {config_path}\n"
                f"请复制 coding-auth.yaml.example 并填写实际信息"
            )
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        self.coding_url: str = data.get("coding_url", "https://yldc.coding.yili.com").rstrip("/")
        self.user_id: str = data.get("user_id", "")
        self.user_display_name: str = data.get("user_display_name", "")
        self.personal_access_token: str = data.get("personal_access_token", "")
        self.cookie_file: str = data.get("cookie_file", "")
        self.sso_username: str = data.get("sso_username", "")
        self.sso_password: str = data.get("sso_password", "")

    def get_cookie_path(self) -> Path:
        """获取 Cookie 文件的绝对路径"""
        if self.cookie_file:
            p = Path(self.cookie_file)
            if not p.is_absolute():
                p = PROJECT_ROOT / p
            return p
        return COOKIE_PATH


# ---------------------------------------------------------------------------
# Coding API 客户端
# ---------------------------------------------------------------------------
class CodingClient:
    """Coding 平台 API 客户端，支持 Open API 和内部 API"""

    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) prefetch/1.0",
            "Accept": "application/json",
        })
        self.base_url = config.coding_url
        self._auth_method: Optional[str] = None
        # API 模式: 'open_api' 或 'internal_api'
        self._api_mode: Optional[str] = None

    # ----- 认证 -----

    def authenticate(self) -> bool:
        """
        按优先级尝试认证:
        1. Personal Access Token (PAT)
        2. Cookie 文件导入
        3. SSO 登录获取 session
        """
        # 策略1: Personal Access Token
        if self.config.personal_access_token:
            log.info("尝试 Personal Access Token 认证...")
            self.session.headers["Authorization"] = f"token {self.config.personal_access_token}"
            if self._verify_auth_open_api():
                self._auth_method = "PAT"
                self._api_mode = "open_api"
                log.info("✓ PAT 认证成功 (Open API 模式)")
                return True
            else:
                log.warning("✗ PAT 认证失败，尝试下一策略")
                self.session.headers.pop("Authorization", None)

        # 策略2: Cookie 文件
        cookie_path = self.config.get_cookie_path()
        if cookie_path.exists():
            log.info(f"尝试 Cookie 文件认证: {cookie_path}")
            if self._load_cookies(cookie_path):
                if self._verify_auth_internal_api():
                    self._auth_method = "Cookie"
                    self._api_mode = "internal_api"
                    log.info("✓ Cookie 认证成功 (内部 API 模式)")
                    return True
                # Cookie 加载了但验证失败，也试试 Open API
                if self.config.personal_access_token:
                    pass  # 已经试过了
                log.warning("✗ Cookie 认证失败，尝试下一策略")

        # 策略3: SSO 登录
        if self.config.sso_username and self.config.sso_password:
            log.info("尝试 SSO 登录...")
            if self._sso_login():
                if self._verify_auth_internal_api():
                    self._auth_method = "SSO"
                    self._api_mode = "internal_api"
                    log.info("✓ SSO 登录成功 (内部 API 模式)")
                    # 导出 Cookie 供后续使用
                    self._export_cookies()
                    return True
                log.warning("✗ SSO 登录后验证失败")

        log.error(
            "所有认证策略均失败！请检查:\n"
            "  1. 在 coding-auth.yaml 中配置 personal_access_token\n"
            "     (Coding → 个人设置 → 访问令牌 → 新建令牌)\n"
            "  2. 或使用 browser-use cookies export 导出 Cookie\n"
            "  3. 或检查 sso_username/sso_password 是否正确"
        )
        return False

    def _load_cookies(self, cookie_path: Path) -> bool:
        """从 JSON 文件加载 Cookie"""
        try:
            with open(cookie_path, "r", encoding="utf-8") as f:
                cookies = json.load(f)
            # 支持 browser-use 导出的格式（数组 [{name, value, domain, ...}]）
            if isinstance(cookies, list):
                for c in cookies:
                    name = c.get("name", "")
                    value = c.get("value", "")
                    domain = c.get("domain", "")
                    if name and value:
                        self.session.cookies.set(name, value, domain=domain)
            elif isinstance(cookies, dict):
                # 简单 {name: value} 格式
                for name, value in cookies.items():
                    self.session.cookies.set(name, value)
            log.info(f"  加载了 {len(self.session.cookies)} 条 Cookie")
            return len(self.session.cookies) > 0
        except Exception as e:
            log.warning(f"  Cookie 文件加载失败: {e}")
            return False

    def _sso_login(self) -> bool:
        """
        通过 SSO 接口登录获取 session cookie。
        Coding 的 SSO 登录通常涉及 OAuth/SAML 重定向，此处尝试常见模式。
        """
        try:
            # 步骤1: 访问 Coding 登录页，获取重定向到 SSO 的 URL
            login_url = f"{self.base_url}/login"
            resp = self.session.get(login_url, allow_redirects=True, timeout=15)

            # 步骤2: 尝试直接 POST SSO 凭证
            # 常见 SSO 登录端点模式
            sso_endpoints = [
                f"{self.base_url}/api/sso/login",
                f"{self.base_url}/api/v1/sso/login",
                f"{self.base_url}/api/auth/login",
            ]

            for endpoint in sso_endpoints:
                try:
                    resp = self.session.post(
                        endpoint,
                        json={
                            "username": self.config.sso_username,
                            "password": self.config.sso_password,
                        },
                        timeout=15,
                    )
                    if resp.status_code == 200:
                        data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
                        if data.get("code") == 0 or data.get("status") == "ok" or "token" in data:
                            log.info(f"  SSO 登录端点命中: {endpoint}")
                            return True
                except Exception:
                    continue

            # 步骤3: 尝试 Coding 自带的登录 API
            try:
                resp = self.session.post(
                    f"{self.base_url}/api/v1/login",
                    json={
                        "account": self.config.sso_username,
                        "password": self.config.sso_password,
                    },
                    timeout=15,
                )
                if resp.status_code == 200:
                    return True
            except Exception:
                pass

            log.warning("  SSO 自动登录未命中已知端点，请使用 PAT 或 Cookie 方式")
            return False

        except Exception as e:
            log.warning(f"  SSO 登录异常: {e}")
            return False

    def _export_cookies(self):
        """导出当前 session 的 Cookie 到文件"""
        try:
            cookie_path = self.config.get_cookie_path()
            cookie_path.parent.mkdir(parents=True, exist_ok=True)
            cookies = []
            for c in self.session.cookies:
                cookies.append({
                    "name": c.name,
                    "value": c.value,
                    "domain": c.domain,
                    "path": c.path,
                })
            with open(cookie_path, "w", encoding="utf-8") as f:
                json.dump(cookies, f, indent=2, ensure_ascii=False)
            log.info(f"  Cookie 已导出到: {cookie_path}")
        except Exception as e:
            log.warning(f"  Cookie 导出失败: {e}")

    def _verify_auth_open_api(self) -> bool:
        """通过 Open API 验证认证是否有效"""
        try:
            resp = self.session.post(
                f"{self.base_url}/open-api",
                json={
                    "Action": "DescribeIssueListWithPage",
                    "ProjectName": CODING_PROJECT,
                    "IssueType": "DEFECT",
                    "PageSize": 1,
                    "PageNumber": 1,
                },
                timeout=15,
            )
            if resp.status_code == 200:
                data = resp.json()
                # Coding Open API 成功时 Response 中不含 Error
                if "Response" in data and "Error" not in data.get("Response", {}):
                    return True
                # 某些版本返回 code=0
                if data.get("code") == 0:
                    return True
            return False
        except Exception as e:
            log.debug(f"  Open API 验证异常: {e}")
            return False

    def _verify_auth_internal_api(self) -> bool:
        """通过内部 API 验证认证是否有效"""
        try:
            resp = self.session.get(
                f"{self.base_url}/api/v2/project/{CODING_PROJECT}/issues",
                params={"type": "DEFECT", "pageSize": 1},
                timeout=15,
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get("code") == 0 or "data" in data or "Data" in data:
                    return True
            # 尝试另一个内部端点
            resp2 = self.session.get(
                f"{self.base_url}/api/project/{CODING_PROJECT}/issues",
                params={"type": "DEFECT", "pageSize": 1},
                timeout=15,
            )
            if resp2.status_code == 200:
                return True
            return False
        except Exception as e:
            log.debug(f"  内部 API 验证异常: {e}")
            return False

    # ----- Bug 列表获取 -----

    def get_bug_list(self, filter_url: Optional[str] = None, assignee: Optional[str] = None) -> list[dict]:
        """
        获取 Bug 列表。
        :param filter_url: Coding 筛选器 URL（含 filter ID）
        :param assignee: 处理人 ID（用于 --mine 模式）
        :return: Bug 列表 [{id, title, status, assignee, priority, ...}]
        """
        if self._api_mode == "open_api":
            return self._get_bug_list_open_api(filter_url, assignee)
        else:
            return self._get_bug_list_internal_api(filter_url, assignee)

    def _get_bug_list_open_api(self, filter_url: Optional[str], assignee: Optional[str]) -> list[dict]:
        """通过 Open API 获取 Bug 列表"""
        all_bugs = []
        page = 1
        page_size = 100

        while True:
            body = {
                "Action": "DescribeIssueListWithPage",
                "ProjectName": CODING_PROJECT,
                "IssueType": "DEFECT",
                "PageSize": page_size,
                "PageNumber": page,
                "SortKey": "PRIORITY",
                "SortValue": "DESC",
            }
            if assignee:
                body["AssigneeId"] = assignee

            resp = self._request("POST", f"{self.base_url}/open-api", json_body=body)
            if not resp:
                break

            data = resp.get("Response", resp)
            issue_data = data.get("Data", data.get("data", {}))
            issues = issue_data.get("List", issue_data.get("list", []))
            total = issue_data.get("TotalCount", issue_data.get("totalCount", 0))

            for issue in issues:
                bug = self._normalize_issue(issue)
                if bug:
                    all_bugs.append(bug)

            log.info(f"  第 {page} 页: 获取 {len(issues)} 条, 总计 {total} 条")

            if len(all_bugs) >= total or len(issues) < page_size:
                break
            page += 1

        return all_bugs

    def _get_bug_list_internal_api(self, filter_url: Optional[str], assignee: Optional[str]) -> list[dict]:
        """通过内部 API 获取 Bug 列表"""
        all_bugs = []
        page = 1
        page_size = 100

        # 尝试从 filter URL 提取参数
        params = {"type": "DEFECT", "pageSize": page_size}
        if filter_url:
            parsed = urlparse(filter_url)
            qs = parse_qs(parsed.query)
            if "filter" in qs:
                params["filter"] = qs["filter"][0]

        if assignee:
            params["assignee"] = assignee

        # 尝试多个可能的内部 API 路径
        api_paths = [
            f"/api/v2/project/{CODING_PROJECT}/issues",
            f"/api/project/{CODING_PROJECT}/issues",
            f"/api/v1/project/{CODING_PROJECT}/issues",
        ]

        working_path = None
        for path in api_paths:
            try:
                params["page"] = page
                resp = self.session.get(
                    f"{self.base_url}{path}",
                    params=params,
                    timeout=15,
                )
                if resp.status_code == 200:
                    working_path = path
                    break
            except Exception:
                continue

        if not working_path:
            log.error("  未找到可用的内部 API 路径")
            return []

        while True:
            params["page"] = page
            resp_data = self._request("GET", f"{self.base_url}{working_path}", params=params)
            if not resp_data:
                break

            data = resp_data.get("data", resp_data.get("Data", resp_data))
            if isinstance(data, dict):
                issues = data.get("list", data.get("List", data.get("issues", [])))
                total = data.get("totalCount", data.get("TotalCount", data.get("total", 0)))
            elif isinstance(data, list):
                issues = data
                total = len(data)
            else:
                break

            for issue in issues:
                bug = self._normalize_issue(issue)
                if bug:
                    all_bugs.append(bug)

            log.info(f"  第 {page} 页: 获取 {len(issues)} 条")

            if not issues or len(all_bugs) >= total or len(issues) < page_size:
                break
            page += 1

        return all_bugs

    # ----- Bug 详情获取 -----

    def get_bug_detail(self, bug_id: int) -> Optional[dict]:
        """获取单个 Bug 的完整详情"""
        if self._api_mode == "open_api":
            return self._get_bug_detail_open_api(bug_id)
        else:
            return self._get_bug_detail_internal_api(bug_id)

    def _get_bug_detail_open_api(self, bug_id: int) -> Optional[dict]:
        resp = self._request("POST", f"{self.base_url}/open-api", json_body={
            "Action": "DescribeIssue",
            "ProjectName": CODING_PROJECT,
            "IssueCode": bug_id,
        })
        if not resp:
            return None
        data = resp.get("Response", resp)
        issue = data.get("Issue", data.get("issue", data.get("data", {})))
        return self._normalize_issue_detail(issue, bug_id)

    def _get_bug_detail_internal_api(self, bug_id: int) -> Optional[dict]:
        paths = [
            f"/api/v2/project/{CODING_PROJECT}/issues/{bug_id}",
            f"/api/project/{CODING_PROJECT}/issues/{bug_id}",
            f"/api/v2/project/{CODING_PROJECT}/issue/{bug_id}",
        ]
        for path in paths:
            resp = self._request("GET", f"{self.base_url}{path}")
            if resp:
                data = resp.get("data", resp.get("Data", resp.get("issue", resp)))
                if data and isinstance(data, dict):
                    return self._normalize_issue_detail(data, bug_id)
        return None

    # ----- 评论获取 -----

    def get_bug_comments(self, bug_id: int) -> list[dict]:
        """获取 Bug 的所有评论"""
        if self._api_mode == "open_api":
            return self._get_comments_open_api(bug_id)
        else:
            return self._get_comments_internal_api(bug_id)

    def _get_comments_open_api(self, bug_id: int) -> list[dict]:
        resp = self._request("POST", f"{self.base_url}/open-api", json_body={
            "Action": "DescribeIssueCommentList",
            "ProjectName": CODING_PROJECT,
            "IssueCode": bug_id,
            "PageSize": 100,
            "PageNumber": 1,
        })
        if not resp:
            return []
        data = resp.get("Response", resp)
        comment_data = data.get("Data", data.get("data", {}))
        comments_raw = comment_data.get("List", comment_data.get("list", []))
        return [self._normalize_comment(c) for c in comments_raw if c]

    def _get_comments_internal_api(self, bug_id: int) -> list[dict]:
        paths = [
            f"/api/v2/project/{CODING_PROJECT}/issues/{bug_id}/comments",
            f"/api/project/{CODING_PROJECT}/issues/{bug_id}/comments",
            f"/api/v2/project/{CODING_PROJECT}/issue/{bug_id}/comments",
        ]
        for path in paths:
            resp = self._request("GET", f"{self.base_url}{path}", params={"pageSize": 100})
            if resp:
                data = resp.get("data", resp.get("Data", resp))
                if isinstance(data, dict):
                    comments_raw = data.get("list", data.get("List", data.get("comments", [])))
                elif isinstance(data, list):
                    comments_raw = data
                else:
                    continue
                return [self._normalize_comment(c) for c in comments_raw if c]
        return []

    # ----- 活动日志获取 -----

    def get_bug_activities(self, bug_id: int) -> list[dict]:
        """获取 Bug 的活动日志（状态变更等）"""
        if self._api_mode == "open_api":
            resp = self._request("POST", f"{self.base_url}/open-api", json_body={
                "Action": "DescribeIssueActivityList",
                "ProjectName": CODING_PROJECT,
                "IssueCode": bug_id,
            })
        else:
            resp = self._request("GET",
                f"{self.base_url}/api/v2/project/{CODING_PROJECT}/issues/{bug_id}/activities")
        # 活动日志是可选的，失败不影响主流程
        return []

    # ----- 通用请求 -----

    def _request(self, method: str, url: str, params: dict = None,
                 json_body: dict = None, retries: int = 2) -> Optional[dict]:
        """带重试的 HTTP 请求"""
        for attempt in range(retries + 1):
            try:
                resp = self.session.request(
                    method, url,
                    params=params,
                    json=json_body,
                    timeout=20,
                )
                if resp.status_code == 200:
                    try:
                        return resp.json()
                    except Exception:
                        log.debug(f"  响应非 JSON: {url}")
                        return None
                elif resp.status_code == 401:
                    log.warning(f"  认证过期 (401): {url}")
                    return None
                elif resp.status_code == 404:
                    log.debug(f"  接口不存在 (404): {url}")
                    return None
                else:
                    log.debug(f"  请求失败 ({resp.status_code}): {url}")
            except requests.exceptions.Timeout:
                log.warning(f"  请求超时 (attempt {attempt + 1}): {url}")
            except Exception as e:
                log.warning(f"  请求异常 (attempt {attempt + 1}): {e}")

            if attempt < retries:
                time.sleep(1 * (attempt + 1))

        return None

    # ----- 数据标准化 -----

    def _normalize_issue(self, raw: dict) -> Optional[dict]:
        """将 API 返回的 issue 数据标准化为统一格式"""
        if not raw:
            return None
        # 兼容不同 API 返回的字段名
        bug_id = raw.get("Code", raw.get("code", raw.get("id", raw.get("IssueCode", 0))))
        title = raw.get("Name", raw.get("name", raw.get("title", "")))
        status = raw.get("StatusName", raw.get("statusName", raw.get("status", "")))
        priority_raw = str(raw.get("Priority", raw.get("priority", "")))
        priority = PRIORITY_MAP.get(priority_raw, priority_raw)

        # 处理人
        assignee_obj = raw.get("Assignee", raw.get("assignee", {}))
        if isinstance(assignee_obj, dict):
            assignee = assignee_obj.get("Name", assignee_obj.get("name",
                       assignee_obj.get("DisplayName", assignee_obj.get("displayName", ""))))
        else:
            assignee = str(assignee_obj) if assignee_obj else ""

        # 标签
        labels_raw = raw.get("Labels", raw.get("labels", []))
        labels = []
        if isinstance(labels_raw, list):
            for lb in labels_raw:
                if isinstance(lb, dict):
                    labels.append(lb.get("Name", lb.get("name", str(lb))))
                else:
                    labels.append(str(lb))

        # 模块
        module = raw.get("Module", raw.get("module", ""))
        if isinstance(module, dict):
            module = module.get("Name", module.get("name", ""))

        return {
            "id": int(bug_id) if bug_id else 0,
            "title": title,
            "status": status,
            "assignee": assignee,
            "priority": priority,
            "labels": labels,
            "module": module,
        }

    def _normalize_issue_detail(self, raw: dict, bug_id: int) -> Optional[dict]:
        """标准化 Bug 详情"""
        if not raw:
            return None
        base = self._normalize_issue(raw) or {}
        base["id"] = base.get("id") or bug_id

        # 描述
        description = raw.get("Description", raw.get("description",
                      raw.get("Content", raw.get("content", ""))))
        # 去除 HTML 标签（简单清理）
        if description:
            description = re.sub(r"<[^>]+>", "", description)
            description = re.sub(r"&nbsp;", " ", description)
            description = re.sub(r"&lt;", "<", description)
            description = re.sub(r"&gt;", ">", description)
            description = re.sub(r"&amp;", "&", description)
            description = description.strip()
        base["description"] = description

        # 额外字段
        base["reporter"] = ""
        reporter = raw.get("Creator", raw.get("creator", raw.get("Reporter", raw.get("reporter", {}))))
        if isinstance(reporter, dict):
            base["reporter"] = reporter.get("Name", reporter.get("name",
                               reporter.get("DisplayName", reporter.get("displayName", ""))))
        elif reporter:
            base["reporter"] = str(reporter)

        # 迭代
        iteration = raw.get("Iteration", raw.get("iteration", {}))
        if isinstance(iteration, dict):
            base["iteration"] = iteration.get("Name", iteration.get("name", "未规划进迭代"))
        else:
            base["iteration"] = str(iteration) if iteration else "未规划进迭代"

        # 截止日期
        deadline = raw.get("DueDate", raw.get("dueDate", raw.get("deadline", "")))
        if isinstance(deadline, (int, float)) and deadline > 0:
            base["deadline"] = datetime.fromtimestamp(deadline / 1000).strftime("%Y/%m/%d")
        else:
            base["deadline"] = str(deadline) if deadline else ""

        # 创建时间
        created = raw.get("CreatedAt", raw.get("createdAt", raw.get("created_at", "")))
        if isinstance(created, (int, float)) and created > 0:
            base["created_at"] = datetime.fromtimestamp(created / 1000).strftime("%Y-%m-%d %H:%M")
        else:
            base["created_at"] = str(created) if created else ""

        # 缺陷类型、测试阶段
        base["bug_type"] = raw.get("DefectType", raw.get("defectType",
                           raw.get("IssueSubType", raw.get("issueSubType", "功能缺陷"))))
        if isinstance(base["bug_type"], dict):
            base["bug_type"] = base["bug_type"].get("Name", base["bug_type"].get("name", "功能缺陷"))

        base["test_phase"] = raw.get("TestPhase", raw.get("testPhase", "SIT"))

        return base

    def _normalize_comment(self, raw: dict) -> dict:
        """标准化评论数据"""
        author = raw.get("Author", raw.get("author", raw.get("Creator", raw.get("creator", {}))))
        if isinstance(author, dict):
            author_name = author.get("Name", author.get("name",
                          author.get("DisplayName", author.get("displayName", "未知"))))
        else:
            author_name = str(author) if author else "未知"

        content = raw.get("Content", raw.get("content", raw.get("Body", raw.get("body", ""))))
        # 去除 HTML 标签
        if content:
            content = re.sub(r"<[^>]+>", "", content).strip()

        created = raw.get("CreatedAt", raw.get("createdAt", raw.get("created_at", "")))
        if isinstance(created, (int, float)) and created > 0:
            created_str = datetime.fromtimestamp(created / 1000).strftime("%Y-%m-%d %H:%M")
        else:
            created_str = str(created) if created else ""

        return {
            "author": author_name,
            "content": content,
            "created_at": created_str,
        }


# ---------------------------------------------------------------------------
# 预采集器
# ---------------------------------------------------------------------------
class Prefetcher:
    """并行预采集 Bug 信息"""

    def __init__(self, client: CodingClient, config: Config, workers: int = 5, force: bool = False):
        self.client = client
        self.config = config
        self.workers = workers
        self.force = force
        self.output_dir = OUTPUT_DIR
        self.results: dict[int, dict] = {}  # bug_id → {status, error}
        self.bugs: list[dict] = []

    def run(self, filter_url: Optional[str] = None, mine: bool = False,
            bug_ids: Optional[list[int]] = None, dry_run: bool = False) -> bool:
        """
        执行预采集主流程:
        1. 获取 Bug 列表
        2. 并行抓取详情 + 评论
        3. 生成 prefetch-summary.json
        """
        start_time = time.time()
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # ---- 获取 Bug 列表 ----
        if bug_ids:
            log.info(f"指定 Bug ID: {bug_ids}")
            self.bugs = [{"id": bid, "title": f"Bug #{bid}", "status": "", "priority": "", "assignee": "", "labels": [], "module": ""} for bid in bug_ids]
        else:
            assignee = self.config.user_id if mine else None
            log.info(f"正在获取 Bug 列表... (assignee={assignee or '全部'})")
            self.bugs = self.client.get_bug_list(filter_url=filter_url, assignee=assignee)

        if not self.bugs:
            log.error("未获取到任何 Bug，请检查筛选条件和认证状态")
            return False

        log.info(f"获取到 {len(self.bugs)} 个 Bug")

        if dry_run:
            log.info("\n===== 空跑模式: 仅列出 Bug 列表 =====")
            for i, bug in enumerate(self.bugs, 1):
                log.info(f"  [{i:2d}] #{bug['id']} [{bug.get('priority', '?')}] {bug['title']}")
            return True

        # ---- 并行抓取详情 + 评论 ----
        log.info(f"\n开始并行抓取 (workers={self.workers})...")
        success_count = 0
        fail_count = 0

        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = {}
            for bug in self.bugs:
                future = executor.submit(self._fetch_single_bug, bug)
                futures[future] = bug["id"]

            for future in as_completed(futures):
                bug_id = futures[future]
                try:
                    result = future.result()
                    self.results[bug_id] = result
                    if result["status"] == "success":
                        success_count += 1
                        log.info(f"  ✓ #{bug_id} {result.get('title', '')[:40]}")
                    elif result["status"] == "skipped":
                        success_count += 1
                        log.info(f"  ⊘ #{bug_id} 已存在，跳过 (使用 --force 强制刷新)")
                    else:
                        fail_count += 1
                        log.warning(f"  ✗ #{bug_id} 失败: {result.get('error', '未知错误')}")
                except Exception as e:
                    fail_count += 1
                    self.results[bug_id] = {"status": "error", "error": str(e)}
                    log.warning(f"  ✗ #{bug_id} 异常: {e}")

        # ---- 生成汇总 ----
        self._generate_summary(filter_url)

        elapsed = time.time() - start_time
        log.info(f"\n===== 预采集完成 =====")
        log.info(f"  总计: {len(self.bugs)} | 成功: {success_count} | 失败: {fail_count}")
        log.info(f"  耗时: {elapsed:.1f}s")
        log.info(f"  输出: {self.output_dir}")

        return fail_count == 0

    def _fetch_single_bug(self, bug: dict) -> dict:
        """抓取单个 Bug 的详情和评论（线程安全）"""
        bug_id = bug["id"]
        bug_dir = self.output_dir / str(bug_id)

        # 检查是否已存在（非 force 模式下跳过）
        metadata_path = bug_dir / "metadata.json"
        if not self.force and metadata_path.exists():
            return {"status": "skipped", "title": bug.get("title", "")}

        bug_dir.mkdir(parents=True, exist_ok=True)

        try:
            # 获取详情
            detail = self.client.get_bug_detail(bug_id)
            if not detail:
                # 使用列表数据作为基础
                detail = bug.copy()
                detail["description"] = ""
                detail["reporter"] = ""
                detail["iteration"] = "未规划进迭代"
                detail["deadline"] = ""
                detail["created_at"] = ""
                detail["bug_type"] = "功能缺陷"
                detail["test_phase"] = "SIT"

            # 获取评论
            comments = self.client.get_bug_comments(bug_id)

            # 识别模板编号
            template = self._extract_template(detail)

            # 保存 detail.txt
            self._save_detail_txt(bug_dir, detail)

            # 保存 comments.txt
            self._save_comments_txt(bug_dir, comments)

            # 保存 metadata.json
            metadata = {
                "id": bug_id,
                "title": detail.get("title", bug.get("title", "")),
                "status": detail.get("status", bug.get("status", "")),
                "assignee": detail.get("assignee", bug.get("assignee", "")),
                "labels": detail.get("labels", bug.get("labels", [])),
                "template": template,
                "module": detail.get("module", bug.get("module", "")),
                "priority": detail.get("priority", bug.get("priority", "")),
                "reporter": detail.get("reporter", ""),
                "iteration": detail.get("iteration", "未规划进迭代"),
                "deadline": detail.get("deadline", ""),
                "created_at": detail.get("created_at", ""),
                "test_phase": detail.get("test_phase", "SIT"),
                "bug_type": detail.get("bug_type", "功能缺陷"),
                "detail_file": "detail.txt",
                "comments_file": "comments.txt",
                "comments_count": len(comments),
            }
            with open(bug_dir / "metadata.json", "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            return {
                "status": "success",
                "title": metadata["title"],
                "template": template,
                "comments_count": len(comments),
            }

        except Exception as e:
            return {"status": "error", "error": str(e), "title": bug.get("title", "")}

    def _extract_template(self, detail: dict) -> str:
        """从 Bug 信息中提取模板编号（T044/T047 等）"""
        text_sources = [
            detail.get("title", ""),
            " ".join(detail.get("labels", [])),
            detail.get("description", ""),
        ]
        combined = " ".join(text_sources)

        # 直接匹配 T+3位数字
        matches = re.findall(r"T\d{3}", combined)
        if matches:
            return "/".join(sorted(set(matches)))

        # 从标签中提取3位数字前缀（如 "049杂项采购报账单" → T049）
        for label in detail.get("labels", []):
            num_match = re.match(r"(\d{3})", label)
            if num_match:
                return f"T{num_match.group(1)}"

        # 关键词匹配
        title = detail.get("title", "")
        if any(kw in title for kw in ["发送校验", "发送", "校验"]):
            return "公共"
        if "查看报账单" in title or "查看" in title:
            return "公共"

        return "公共"

    def _save_detail_txt(self, bug_dir: Path, detail: dict):
        """保存 detail.txt（与现有格式兼容）"""
        lines = [
            f"## Bug #{detail.get('id', '')}: {detail.get('title', '')}",
            "",
            "### 基本信息",
            f"- 状态: {detail.get('status', '')}",
            f"- 处理人: {detail.get('assignee', '')}",
            f"- 优先级: {detail.get('priority', '')}",
            f"- 模块: {detail.get('module', '')}",
            f"- 标签: {', '.join(detail.get('labels', [])) or '无'}",
            f"- 发起人: {detail.get('reporter', '')}",
            f"- 迭代: {detail.get('iteration', '')}",
            f"- 截止日期: {detail.get('deadline', '')}",
            f"- 创建时间: {detail.get('created_at', '')}",
            f"- 测试阶段: {detail.get('test_phase', '')}",
            f"- 缺陷类型: {detail.get('bug_type', '')}",
            f"- 识别模板编号: {self._extract_template(detail)}",
            "",
            "### 描述",
            detail.get("description", "(无描述)"),
            "",
        ]
        with open(bug_dir / "detail.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    def _save_comments_txt(self, bug_dir: Path, comments: list[dict]):
        """保存 comments.txt（与现有格式兼容）"""
        lines = [f"### 评论列表 (共 {len(comments)} 条)", ""]
        if not comments:
            lines.append("(无评论)")
        else:
            for i, c in enumerate(comments, 1):
                lines.append(f"**评论 #{i}** - {c.get('author', '未知')} @ {c.get('created_at', '')}")
                content = c.get("content", "")
                # 每行加 > 前缀
                for line in content.split("\n"):
                    lines.append(f"> {line}")
                lines.append("")
        lines.append("")
        with open(bug_dir / "comments.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    def _generate_summary(self, filter_url: Optional[str]):
        """生成 prefetch-summary.json（与现有格式兼容）"""
        by_priority: dict[str, int] = {}
        by_status: dict[str, int] = {}
        by_module: dict[str, int] = {}
        by_template: dict[str, int] = {}
        bug_entries = []

        for bug in self.bugs:
            bug_id = bug["id"]
            result = self.results.get(bug_id, {})

            # 读取 metadata（如果采集成功）
            meta_path = self.output_dir / str(bug_id) / "metadata.json"
            if meta_path.exists():
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
            else:
                meta = bug

            priority = meta.get("priority", "未知")
            status = meta.get("status", "未知")
            module = meta.get("module", "未知")
            template = meta.get("template", result.get("template", "公共"))
            comments_count = meta.get("comments_count", result.get("comments_count", 0))

            by_priority[priority] = by_priority.get(priority, 0) + 1
            by_status[status] = by_status.get(status, 0) + 1
            by_module[module] = by_module.get(module, 0) + 1
            by_template[template] = by_template.get(template, 0) + 1

            bug_entries.append({
                "id": bug_id,
                "title": meta.get("title", bug.get("title", "")),
                "priority": priority,
                "status": status,
                "template": template,
                "module": module,
                "comments_count": comments_count,
            })

        summary = {
            "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "filter_url": filter_url or "",
            "handler": self.config.user_display_name or self.config.user_id,
            "deadline_cutoff": "",
            "total": len(self.bugs),
            "by_priority": dict(sorted(by_priority.items())),
            "by_status": dict(sorted(by_status.items())),
            "by_module": dict(sorted(by_module.items())),
            "by_template": dict(sorted(by_template.items())),
            "bugs": bug_entries,
        }

        summary_path = self.output_dir / "prefetch-summary.json"
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        log.info(f"  汇总已保存: {summary_path}")


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Phase 1 预采集脚本 — 并行获取 Coding Bug 信息",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从筛选器 URL 抓取
  python3 prefetch.py --filter "https://yldc.coding.yili.com/p/fssc/all/issues?filter=..."

  # 抓取分配给我的 Bug
  python3 prefetch.py --mine

  # 指定并发数 + 强制刷新
  python3 prefetch.py --mine --workers 8 --force

  # 只抓取指定 Bug
  python3 prefetch.py --bugs 5186,5200,5399

  # 空跑模式
  python3 prefetch.py --mine --dry-run

认证配置: ai-spec/skills/code/bug-fix-cycle/coding-bug-ops/config/coding-auth.yaml
输出目录: yili-out/bug-prefetch/
        """,
    )

    # 输入来源（三选一）
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--filter", type=str, help="Coding 筛选器 URL")
    group.add_argument("--mine", action="store_true", help="抓取分配给我的 Bug")
    group.add_argument("--bugs", type=str, help="指定 Bug ID（逗号分隔），如 5186,5200,5399")

    # 可选参数
    parser.add_argument("--workers", type=int, default=5, help="并发线程数 (默认 5)")
    parser.add_argument("--force", action="store_true", help="强制刷新已存在的数据")
    parser.add_argument("--dry-run", action="store_true", help="空跑模式，只列出 Bug 不抓取")
    parser.add_argument("--config", type=str, help="指定认证配置文件路径")
    parser.add_argument("--output", type=str, help="指定输出目录")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细日志")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # 加载配置
    config_path = Path(args.config) if args.config else CONFIG_PATH
    try:
        config = Config(config_path)
    except FileNotFoundError as e:
        log.error(str(e))
        sys.exit(1)

    log.info(f"配置已加载: {config_path}")
    log.info(f"Coding URL: {config.coding_url}")
    log.info(f"用户: {config.user_display_name} ({config.user_id})")

    # 初始化客户端并认证
    client = CodingClient(config)
    if not client.authenticate():
        sys.exit(1)

    # 初始化预采集器
    prefetcher = Prefetcher(
        client=client,
        config=config,
        workers=args.workers,
        force=args.force,
    )

    if args.output:
        prefetcher.output_dir = Path(args.output)

    # 解析 Bug ID 列表
    bug_ids = None
    if args.bugs:
        try:
            bug_ids = [int(x.strip()) for x in args.bugs.split(",") if x.strip()]
        except ValueError:
            log.error(f"Bug ID 格式错误: {args.bugs}，请用逗号分隔数字")
            sys.exit(1)

    # 执行预采集
    success = prefetcher.run(
        filter_url=args.filter,
        mine=args.mine or False,
        bug_ids=bug_ids,
        dry_run=args.dry_run,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
