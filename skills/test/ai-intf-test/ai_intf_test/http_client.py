"""HTTP 客户端模块：封装请求发送、认证、重试机制"""
from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional, Tuple

import requests
from requests.auth import HTTPBasicAuth

from .config_loader import AuthConfig, RetryConfig, RoutingConfig, ServerConfig
from .models import TestInput, TestResult, ValidateResult

logger = logging.getLogger(__name__)


class HttpClient:
    """submitValidate 接口 HTTP 客户端

    封装了认证、重试、超时、结果解析等完整功能。
    """

    def __init__(
        self,
        server_config: ServerConfig,
        auth_config: AuthConfig,
        retry_config: RetryConfig,
        url_template: str,
        routing_config: RoutingConfig = None,
    ) -> None:
        self._base_url = server_config.base_url
        self._timeout = (server_config.connect_timeout, server_config.timeout)
        self._auth_config = auth_config
        self._retry_config = retry_config
        self._url_template = url_template
        self._routing_config = routing_config or RoutingConfig()
        self._session = self._create_session()

    @property
    def session(self) -> requests.Session:
        """获取内部 Session 实例（供 LoginHandler 注入 Cookie 使用）"""
        return self._session

    def _create_session(self) -> requests.Session:
        """创建带认证配置的 requests Session"""
        session = requests.Session()

        # 通用请求头
        session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

        # 按认证类型配置
        auth_type = self._auth_config.type.lower()

        if auth_type == "login":
            # login 模式下，Cookie 将由 LoginHandler 在 pipeline 阶段注入
            logger.debug("认证模式为 login，Cookie 将由登录流程注入")

        elif auth_type == "token" and self._auth_config.token:
            session.headers["Authorization"] = f"Bearer {self._auth_config.token}"
            logger.debug("已配置 Bearer Token 认证")

        elif auth_type == "cookie" and self._auth_config.cookie:
            session.headers["Cookie"] = self._auth_config.cookie
            logger.debug("已配置 Cookie 认证")

        elif auth_type == "basic" and self._auth_config.username:
            session.auth = HTTPBasicAuth(
                self._auth_config.username,
                self._auth_config.password,
            )
            logger.debug("已配置 Basic Auth 认证")

        # 自定义头
        if self._auth_config.custom_headers:
            session.headers.update(self._auth_config.custom_headers)
            logger.debug(f"已添加自定义头: {list(self._auth_config.custom_headers.keys())}")

        return session

    def build_url(self, item_id: str) -> str:
        """根据 itemId 构造完整请求 URL

        自动解析 {service_path} 占位符：根据 routing 配置将 itemId
        映射到对应的服务路径（如 /eer、/ptp）
        """
        service_path = self._routing_config.resolve_service_path(item_id)
        return self._url_template.format(
            base_url=self._base_url,
            service_path=service_path,
            item_id=item_id,
        )

    def resolve_service_name(self, item_id: str) -> str:
        """获取 itemId 对应的服务名称（如 eer、ptp、claim）"""
        return self._routing_config.resolve_service_name(item_id)

    def execute(self, test_input: TestInput) -> TestResult:
        """执行单个 submitValidate 请求

        Args:
            test_input: 测试输入数据

        Returns:
            TestResult 包含完整测试结果
        """
        url = self.build_url(test_input.item_id)
        payload = {"claimId": test_input.claim_id}

        result = TestResult(
            claim_id=test_input.claim_id,
            item_id=test_input.item_id,
            url=url,
            service_type=self.resolve_service_name(test_input.item_id),
        )

        response = self._send_with_retry(url, payload)

        if response is None:
            result.error = "所有重试均失败，未获得响应"
            return result

        result.status_code = response.status_code

        try:
            body = response.json()
            result.raw_response = body
            self._parse_response(result, body)
        except Exception as e:
            result.error = f"响应解析失败: {e}"
            logger.error(f"[{test_input.item_id}] claimId={test_input.claim_id} 响应解析失败: {e}")

        return result

    def _send_with_retry(
        self, url: str, payload: dict
    ) -> Optional[requests.Response]:
        """带重试机制的 POST 请求"""
        max_retries = self._retry_config.max_retries
        retry_interval = self._retry_config.retry_interval
        retry_status_codes = set(self._retry_config.retry_on_status_codes)

        last_error = None

        for attempt in range(1, max_retries + 1):
            try:
                start_time = time.time()
                response = self._session.post(
                    url,
                    json=payload,
                    timeout=self._timeout,
                )
                elapsed_ms = int((time.time() - start_time) * 1000)

                logger.debug(
                    f"请求完成 [{attempt}/{max_retries}] {url} "
                    f"status={response.status_code} elapsed={elapsed_ms}ms"
                )

                # 如果状态码在重试列表中且还有重试机会，则重试
                if response.status_code in retry_status_codes and attempt < max_retries:
                    logger.warning(
                        f"HTTP {response.status_code}，{retry_interval}秒后重试 "
                        f"[{attempt}/{max_retries}]"
                    )
                    time.sleep(retry_interval)
                    continue

                return response

            except requests.exceptions.ConnectionError as e:
                last_error = f"连接失败: {e}"
                logger.warning(f"连接失败 [{attempt}/{max_retries}]: {e}")
            except requests.exceptions.Timeout as e:
                last_error = f"请求超时: {e}"
                logger.warning(f"请求超时 [{attempt}/{max_retries}]: {e}")
            except requests.exceptions.RequestException as e:
                last_error = f"请求异常: {e}"
                logger.warning(f"请求异常 [{attempt}/{max_retries}]: {e}")

            if attempt < max_retries:
                logger.info(f"{retry_interval}秒后重试...")
                time.sleep(retry_interval)

        logger.error(f"所有 {max_retries} 次重试均失败: {last_error}")
        return None

    def _parse_response(self, result: TestResult, body: dict):
        """解析接口返回的 JSON 数据

        预期格式：
        {
            "data": {
                "results": [...],
                "pass": true/false,
                ...
            },
            "success": true/false,
            "message": "...",
            "code": 200,
            "traceId": "..."
        }
        """
        result.success = body.get("success", False)
        result.trace_id = body.get("traceId")

        data = body.get("data")
        if data is None:
            # data 为空时，检查是否有错误信息
            error_msg = body.get("error") or body.get("message")
            if not result.success and error_msg:
                result.error = str(error_msg)
            return

        # 解析 pass 字段
        result.passed = data.get("pass", False)

        # 解析校验结果列表
        raw_results = data.get("results", [])
        if raw_results:
            for item in raw_results:
                vr = ValidateResult(
                    name=item.get("name", ""),
                    message=item.get("message", ""),
                    severity=item.get("severity", "UNKNOWN"),
                    args=item.get("args"),
                )
                result.results.append(vr)

    def close(self):
        """关闭 Session"""
        if self._session:
            self._session.close()
            logger.debug("HTTP Session 已关闭")
