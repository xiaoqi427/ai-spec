---
name: bug-fix-pipeline
description: Coding Bug 全流程自动修复编排器（五阶段模式）。Phase 1 预采集 Bug 信息+截图+测试用例索引 → Phase 2 分诊台让用户调整优先级/标记跳过 → Phase 3 按优先级逐个分析+加载测试用例参考+修复+编译+单元测试+数据验证+本地测试+commit（修一个提交一个） → Phase 4 统一 pull --rebase + push → Phase 5 统一 CI 构建 + Coding 评论+转派+状态更新。编排 memory-setup、coding-bug-ops、yili-code-fix、fix-verify、local-api-test、git-commit-push、coding-ci-deploy、sit-smoke-test、sit-verify-analyze、test-case-ref、db-query、self-improving-agent 等 skill 完成端到端自动化。当用户需要批量或单个修复 Coding Bug 时使用。
---
# Bug Fix Pipeline (全流程自动修复编排器)

@author: sevenxiao

## 概述

此 skill 是**全流程编排器**，采用**五阶段批量处理**模式，协调以下 skill 完成 Coding Bug 从发现到修复闭环的端到端自动化:

```
bug-fix-pipeline (五阶段)
  ├── Phase 1: 预采集 (Prefetch)
  │   ├── coding-bug-ops      → 批量读取 Bug 详情+评论
  │   └── sit-smoke-test      → [可选] 截取 SIT 页面当前状态
  │
  ├── Phase 2: 分诊台 (Triage)
  │   └── 用户交互             → 预览、排序、标记跳过/修复/标注前端
  │
  ├── Phase 3: 批量修复 (Fix & Commit)
  │   ├── memory-setup         → 初始化/更新运行记忆
  │   ├── test-case-ref        → [可选] 加载相关测试用例作为参考
  │   ├── yili-code-fix        → 代码分析 + 修复
  │   ├── fix-verify           → [可选] 单元测试 + 数据验证
  │   ├── local-api-test       → [可选] 本地启动 + curl 测试
  │   ├── git commit            → 每修一个 Bug 立即 commit 到本地
  │   └── self-improving-agent → 单 Bug 复盘
  │
  ├── Phase 4: 统一推送 (Push)
  │   └── git-commit-push      → pull --rebase → 冲突检测 → 人工确认 → push
  │
  └── Phase 5: 统一闭环 (Finalize)
      ├── coding-ci-deploy     → CI 构建发布到 SIT
      ├── sit-smoke-test       → [可选] SIT 做单验证
      ├── sit-verify-analyze   → [可选] 验证结果分析
      ├── coding-bug-ops       → 批量评论+转派+状态更新
      └── self-improving-agent → 全局复盘
```

### 新旧流程对比

**旧流程（逐个闭环）**:
```
对每个 Bug:
  读取 → 分析 → 确认 → 修复 → 编译 → 测试
  → 提交 → CI → SIT → [评论+转派+状态] → 复盘
```

**新流程（五阶段批量）**:
```
Phase 1: 预采集  → 批量读取 Bug + 截图（浏览器集中使用）
Phase 2: 分诊台  → 用户预览、排序、标记跳过（交互式确认）
Phase 3: 批量修复 → 按优先级逐个 并行分析→[确认]→修复→编译→并行验证→本地测试→commit（offline 模式跳过确认）
Phase 4: 统一推送 → pull --rebase + 冲突检测 + push（一次性推送）
Phase 5: 统一闭环 → CI 构建 + SIT 验证 + Coding 操作（评论+状态+转派）
```

---

## 外部依赖

| 外部 Skill               | 安装命令                                                                | 说明                                                            |
| ------------------------ | ----------------------------------------------------------------------- | --------------------------------------------------------------- |
| `agent-browser`          | 按项目环境单独安装或配置                                                | `bug-fix-pipeline` 默认首选的浏览器验证能力，用于复现、截图和修复回归 |
| `browser-use`            | `npx openskills add browser-use/browser-use@browser-use`                | 需要复用本机 Chrome Profile、Cookie、登录态时作为降级方案       |
| `playwright-e2e-testing` | `npx openskills add bobmatnyc/claude-mpm-skills@playwright-e2e-testing` | 需要稳定回归脚本、断言和可重复执行测试时使用                    |
| `self-improving-agent`   | `npx skills add charon-fan/agent-playbook@self-improving-agent -g -y`   | 可选外部增强版自改进循环。若已安装，可补充更完整的 pattern/memory 结构 |
| `memory-management`      | `npx skills add https://github.com/anthropics/knowledge-work-plugins --skill memory-management -g -y` | 可选外部记忆管理能力。用于补充热缓存/深记忆组织方式，不替代本地 `memory-setup` |

说明:

- `bug-fix-pipeline` 中凡是"打开 SIT 页面、按步骤复现、截图存证、验证修复"这类浏览器任务，默认优先使用 `agent-browser`
- 只有在必须复用登录态、现有浏览器 Profile、Cookie 或沿用现成 CLI 脚本时，才退回 `browser-use`
- 需要沉淀为正式可复跑回归脚本时，再使用 `playwright-e2e-testing`
- 运行记忆与自改进采用**双轨兼容**:
  - 主轨: 仓库内置 `memory-setup` + `self-improving-agent`
  - 增强轨: 已安装 OpenSkill 时，可参考 `memory-management` + 市场版 `self-improving-agent`
- 如果本地 skill 与 OpenSkill 同时存在，**以本仓库 skill 为编排主语义**，OpenSkill 只补方法论和结构，不替换主流程步骤
- 上述能力都属于联调/冒烟/E2E 范畴，不属于单元测试依赖

内部依赖 (无需安装):

| Skill                  | 位置                                              |
| ---------------------- | ------------------------------------------------- |
| `coding-bug-ops`       | `ai-spec/skills/code/bug-fix-cycle/coding-bug-ops/`     |
| `yili-code-fix`        | `ai-spec/skills/code/bug-fix-cycle/yili-code-fix/`      |
| `local-api-test`       | `ai-spec/skills/code/bug-fix-cycle/local-api-test/`     |
| `git-commit-push`      | `ai-spec/skills/code/bug-fix-cycle/git-commit-push/`    |
| `coding-ci-deploy`     | `ai-spec/skills/code/bug-fix-cycle/coding-ci-deploy/`   |
| `sit-smoke-test`       | `ai-spec/skills/code/bug-fix-cycle/sit-smoke-test/`     |
| `sit-verify-analyze`   | `ai-spec/skills/code/bug-fix-cycle/sit-verify-analyze/` |
| `memory-setup`         | `ai-spec/skills/code/bug-fix-cycle/memory-setup/`       |
| `self-improving-agent` | `ai-spec/skills/code/bug-fix-cycle/self-improving-agent/` |
| `compare-transform`    | `ai-spec/skills/code/compare-transform/`                |
| `transform-claim`      | `ai-spec/skills/code/transform-claim/`                  |
| `front-end-skills`     | `ai-spec/skills/code/front-end-skills/`                 |
| `db-query`             | `ai-spec/skills/code/bug-fix-cycle/db-query/`           |
| `test-case-ref`        | `ai-spec/skills/code/bug-fix-cycle/test-case-ref/`      |
| `fix-verify`           | `ai-spec/skills/code/bug-fix-cycle/fix-verify/`         |

---

## 使用方式

### 单 Bug 模式

单 Bug 模式下跳过 Phase 1/2，直接进入 Phase 3 修复:

```bash
# 修复指定 Bug
/skill bug-fix-pipeline #4992

# 修复指定 Bug，跳过 SIT 测试
/skill bug-fix-pipeline #4992 --skip-sit

# 修复指定 Bug，只分析不修复
/skill bug-fix-pipeline #4992 --dry-run
```

### 批量模式（五阶段）

批量模式自动启用 Phase 1 预采集 + Phase 2 分诊台:

```bash
# 从筛选器 URL 批量修复（默认五阶段）
/skill bug-fix-pipeline --filter https://yldc.coding.yili.com/p/fssc/all/issues?filter=f209a5d4938a2da58718629a2f35419a

# 批量模式，只分析不修复
/skill bug-fix-pipeline --filter <url> --dry-run

# 批量模式，合并为一个 commit
/skill bug-fix-pipeline --filter <url> --commit-strategy merge

# 批量模式，跳过 Phase 5 的 SIT 验证
/skill bug-fix-pipeline --filter <url> --skip-sit-verify

# 批量模式，离线全自动（跳过逐 Bug 用户确认）
/skill bug-fix-pipeline --filter <url> --mode offline
```

### 参数说明

| 参数                 | 说明                                    | 默认值             |
| -------------------- | --------------------------------------- | ------------------ |
| `#<bug-id>`          | 单个 Bug ID                             | -                  |
| `--filter <url>`     | Coding 筛选器 URL                       | -                  |
| `--skip-sit`         | 跳过 SIT 测试（单 Bug 模式）            | false              |
| `--dry-run`          | 只分析不修复                            | false              |
| `--auto-comment`     | 自动添加评论                            | true               |
| `--auto-status`      | 自动更新状态                            | false (需手动确认) |
| `--prefetch`         | 启用预采集模式（Phase 1）               | batch 模式自动启用 |
| `--triage`           | 启用分诊台（Phase 2）                   | batch 模式自动启用 |
| `--commit-strategy`  | 提交策略: `per-bug` / `merge`           | `per-bug`          |
| `--skip-sit-verify`  | 跳过 Phase 5 的 SIT 验证               | false              |
| `--mode`             | 执行模式: `offline` / `interactive`     | `interactive`      |

---

## 本地存储结构

批量模式下，预采集数据和修复队列保存在本地:

```
yili-out/bug-prefetch/
├── {bug-id}/
│   ├── detail.txt           # Bug 描述文本
│   ├── detail.png           # Bug 详情页截图
│   ├── comments.txt         # 评论文本
│   ├── comments.png         # 评论区截图
│   ├── sit-current.png      # SIT 页面当前状态（可选）
│   └── metadata.json        # Bug 元数据
├── prefetch-summary.json    # 全部 Bug 汇总
└── fix-queue.json           # 修复队列（Phase 2 生成）

yili-out/test-case-index/
└── test-case-index.json     # 测试用例索引（Phase 1 生成，可选）
```

### metadata.json 结构

```json
{
  "id": 5001,
  "title": "T044 金额计算错误",
  "status": "处理中",
  "assignee": "xiaoqi",
  "labels": ["049杂项采购报账单"],
  "template": "T044",
  "module": "OTC",
  "priority": "高",
  "reporter": "zhangsan",
  "detail_file": "detail.txt",
  "comments_file": "comments.txt"
}
```

### fix-queue.json 结构

```json
{
  "created_at": "2026-04-04T10:00:00",
  "mode": "offline",
  "auto_confirm": true,
  "total": 4,
  "queue": [
    {"id": 5001, "title": "T044 金额计算错误", "action": "fix",          "priority": 1, "module": "T044", "reason": ""},
    {"id": 5003, "title": "T051 保存报错",     "action": "fix",          "priority": 2, "module": "T051", "reason": ""},
    {"id": 5002, "title": "T047 字段不显示",   "action": "tag-frontend", "priority": 3, "module": "T047", "reason": "前端展示问题"},
    {"id": 5004, "title": "T044 页面样式",     "action": "skip",         "priority": 4, "module": "T044", "reason": "低优先级，暂不处理"}
  ],
  "results": {
    "5001": {"status": "fixed",        "files": ["..."], "compile": "pass", "unit_test": {"verdict": "PASS", "total": 10, "passed": 10}, "data_verify": {"verdict": "PASS", "checks": 2}, "local_test": "pass", "comment_draft": "..."},
    "5003": {"status": "fixed",        "files": ["..."], "compile": "pass", "unit_test": {"verdict": "SKIP"}, "data_verify": {"verdict": "SKIP"}, "local_test": "skip", "comment_draft": "..."},
    "5002": {"status": "tag-frontend", "frontend_owner": "lisi", "comment_draft": "..."},
    "5004": {"status": "skipped",      "reason": "低优先级，暂不处理"}
  }
}
```

---

## 编排流程（五阶段）

```
输入: Coding filter URL (bug列表) 或 单个 bug ID
  │
  ├─ Phase 1: 预采集 (Prefetch)
  │   ├─ 1.1 初始化运行记忆 (memory-setup)
  │   ├─ 1.2 打开浏览器，登录 Coding
  │   ├─ 1.3 读取 Bug 列表 (coding-bug-ops.read-list)
  │   ├─ 1.4 遍历每个 Bug:
  │   │   ├─ coding-bug-ops.read-detail   → 保存 detail.txt + detail.png
  │   │   ├─ coding-bug-ops.read-comments → 保存 comments.txt + comments.png
  │   │   └─ [可选] 打开 SIT 对应页面    → 保存 sit-current.png
  │   ├─ 1.5 生成 metadata.json + prefetch-summary.json
  │   ├─ 1.6 [可选] 解析测试用例索引 (test-case-ref.parse)
  │   │   └─ 生成 yili-out/test-case-index/test-case-index.json
  │   │       (索引已存在且未过期则跳过)
  │   ├─ 1.7 导出浏览器 Cookie → config/coding-cookies.json
  │   └─ 1.8 关闭浏览器
  │
  ├─ Phase 2: 分诊台 (Triage)
  │   ├─ 2.1 读取 prefetch-summary.json
  │   ├─ 2.2 对每个 Bug 做初步分类（前端/后端/混合）
  │   │   └─ [可选] test-case-ref.lookup → 匹配相关测试用例
  │   ├─ 2.3 展示分诊表格（含测试用例覆盖列）
  │   ├─ 2.4 ⏸️ 等待用户调整:
  │   │   ├─ 调整优先级/修复顺序
  │   │   ├─ 标记 [修复] / [标注前端] / [跳过]
  │   │   └─ 确认最终修复队列
  │   └─ 2.5 生成 fix-queue.json
  │
  ├─ Phase 3: 批量修复 (Fix & Commit)
  │   ├─ 3.0 读取 fix-queue.json
  │   │
  │   ├─ 对 action=fix 的每个 Bug (按 priority 顺序):
  │   │   ├─ 3.1 装载当前 Bug 记忆 (memory-setup.update)
  │   │   ├─ 3.2 读取本地预采集数据 (detail.txt + comments.txt)
  │   │   ├─ 3.3 并行分析 (fork → join)
  │   │   │   ├─ [A] yili-code-fix.analyze → 遗漏清单
  │   │   │   ├─ [B] test-case-ref.lookup → 测试用例参考
  │   │   │   └─ [C] [可选] db-query.check-data → 数据现状
  │   │   ├─ 3.4 输出分析方案
  │   │   ├─ 3.5 [条件] 等待用户确认 (offline 模式跳过)
  │   │   ├─ 3.6 执行修复 (yili-code-fix.fix)
  │   │   ├─ 3.7 编译验证 (mvn compile)
  │   │   ├─ 3.7.1 [可选] 并行验证 (fork → join)
  │   │   │   ├─ [A] fix-verify.run-tests → 单元测试
  │   │   │   └─ [B] fix-verify.verify-data → 数据验证
  │   │   ├─ 3.8 [可选] 本地接口测试 (local-api-test)
  │   │   ├─ 3.9 git commit → 立即提交到本地
  │   │   │   └─ fix(<module>): #<bug-id> <标题>
  │   │   ├─ 3.10 单 Bug 复盘 (self-improving-agent)
  │   │   └─ 3.11 记录修复结果到 fix-queue.json.results
  │   │
  │   ├─ 对 action=tag-frontend 的每个 Bug:
  │   │   ├─ 读取本地预采集数据，确认前端问题分析
  │   │   ├─ 准备评论草稿 + 查找前端负责人
  │   │   └─ 记录到 fix-queue.json.results (不操作 Coding)
  │   │
  │   └─ 对 action=skip 的每个 Bug:
  │       └─ 记录跳过原因到 fix-queue.json.results
  │
  ├─ Phase 4: 统一推送 (Push)
  │   ├─ 4.1 git log --oneline → 展示本批次所有 commit
  │   ├─ 4.2 git pull --rebase → 拉取最新代码 + 变基
  │   ├─ 4.3 冲突检测 → 有冲突则 ⏸️ 用户手动解决
  │   ├─ 4.4 ⏸️ 用户确认 push
  │   └─ 4.5 git push
  │
  └─ Phase 5: 统一闭环 (Finalize)
      ├─ 5.1 coding-ci-deploy → 触发 CI 构建 → 等待完成
      │   └─ 构建失败 → ⏸️ 通知用户，等待决策
      │
      ├─ 5.2 [可选] SIT 验证:
      │   ├─ sit-smoke-test → 对每个已修复 Bug 做冒烟测试
      │   └─ sit-verify-analyze → 分析验证结果
      │
      ├─ 5.3 打开 Coding 浏览器 (优先导入 config/coding-cookies.json)
      │
      ├─ 5.4 遍历 fix-queue.results:
      │   │
      │   ├─ [status=fixed]:
      │   │   ├─ coding-bug-ops.add-comment (修复说明+老代码位置+修改文件)
      │   │   ├─ coding-bug-ops.update-status → "待验证"
      │   │   └─ coding-bug-ops.reassign → 发起人
      │   │
      │   ├─ [status=tag-frontend]:
      │   │   ├─ coding-bug-ops.add-comment (前端问题说明+老代码位置)
      │   │   └─ coding-bug-ops.reassign → 前端负责人
      │   │
      │   └─ [status=skipped]:
      │       └─ 不操作
      │
      ├─ 5.5 关闭浏览器
      ├─ 5.6 全局复盘 (self-improving-agent)
      └─ 5.7 输出汇总报告
```

---

## 详细步骤说明

### Phase 1: 预采集 (Prefetch)

**目标**: 一次性采集所有 Bug 信息到本地，后续分析阶段不再依赖浏览器。

**好处**:
- 浏览器只开一次，集中采集，减少认证失效/超时问题
- 分析阶段纯离线，不依赖网络和浏览器稳定性
- 采集数据不丢失，即使后续浏览器崩了/SIT 挂了，已采集的数据还在

#### 推荐方式: Python 脚本并行采集 (prefetch.py)

**脚本位置**: `ai-spec/skills/code/bug-fix-cycle/bug-fix-pipeline/scripts/prefetch.py`

**优势**: 使用 Coding REST API + 线程池并行抓取，无需浏览器，速度快 5-10 倍。

**安装依赖**:
```bash
pip3 install requests pyyaml --user --break-system-packages
```

**认证配置** (在 `coding-auth.yaml` 中添加):
```yaml
# 推荐: Personal Access Token (Coding → 个人设置 → 访问令牌 → 新建)
personal_access_token: "your-token-here"
```

**使用示例**:
```bash
# 从筛选器 URL 抓取（默认 5 并发）
python3 ai-spec/skills/code/bug-fix-cycle/bug-fix-pipeline/scripts/prefetch.py \
  --filter "https://yldc.coding.yili.com/p/fssc/all/issues?filter=..."

# 抓取分配给我的 Bug
python3 ai-spec/skills/code/bug-fix-cycle/bug-fix-pipeline/scripts/prefetch.py --mine

# 8 并发 + 强制刷新
python3 ai-spec/skills/code/bug-fix-cycle/bug-fix-pipeline/scripts/prefetch.py --mine --workers 8 --force

# 只抓取指定 Bug
python3 ai-spec/skills/code/bug-fix-cycle/bug-fix-pipeline/scripts/prefetch.py --bugs 5186,5200,5399

# 空跑模式（只列表不抓取）
python3 ai-spec/skills/code/bug-fix-cycle/bug-fix-pipeline/scripts/prefetch.py --mine --dry-run
```

**认证降级顺序**: PAT → Cookie 文件 → SSO 登录
**输出格式**: 与浏览器采集完全兼容 (metadata.json / detail.txt / comments.txt / prefetch-summary.json)

---

#### 备选方式: 浏览器自动化采集 (兼容旧流程)

适用场景: 需要页面截图 (detail.png/comments.png) 或 Cookie 文件不可用时。

##### 1.1 初始化运行记忆

```
读取 memory-setup SKILL.md
→ 建立 run memory
→ 记录:
  - objective
  - bug_queue
  - current_phase: prefetch
  - confirmed_constraints
  - service_map
  - environment
```

##### 1.2-1.6 批量采集

```bash
# 1.2 打开浏览器登录 Coding
browser-use --profile "Default" open "<filter-url>"

# 1.3 读取 Bug 列表
coding-bug-ops.read-list(filter-url)

# 1.4 遍历每个 Bug
for bug_id in bug_list:
    # 读取详情
    coding-bug-ops.read-detail(bug_id)
    → 保存到 yili-out/bug-prefetch/{bug_id}/detail.txt
    → 截图到 yili-out/bug-prefetch/{bug_id}/detail.png

    # 读取评论
    coding-bug-ops.read-comments(bug_id)
    → 保存到 yili-out/bug-prefetch/{bug_id}/comments.txt
    → 截图到 yili-out/bug-prefetch/{bug_id}/comments.png

    # [可选] SIT 当前状态截图
    sit-smoke-test.screenshot(T{XXX})
    → 保存到 yili-out/bug-prefetch/{bug_id}/sit-current.png

    # 生成元数据
    → 保存到 yili-out/bug-prefetch/{bug_id}/metadata.json

# 1.5 生成汇总
→ 保存到 yili-out/bug-prefetch/prefetch-summary.json

# 1.6 [可选] 解析测试用例索引
python3 ai-spec/skills/code/bug-fix-cycle/test-case-ref/scripts/parse_test_cases.py \
  --input ai-spec/skills/code/bug-fix-cycle/test-case-ref/doc/ \
  --output yili-out/test-case-index/test-case-index.json \
  --incremental
# → 索引已存在且源文件未修改则跳过

# 1.7 导出浏览器 Cookie（供 Phase 5 复用，避免重新登录）
browser-use cookies export config/coding-cookies.json

# 1.8 关闭浏览器
```

**单 Bug 模式**: 跳过 Phase 1，直接在 Phase 3 中实时读取 Bug 详情。

---

### Phase 2: 分诊台 (Triage)

**目标**: 让用户在修复前全局预览所有 Bug，调整优先级和标记跳过。

#### 2.1-2.2 读取并分类

```
读取 prefetch-summary.json
→ 对每个 Bug 做初步分类:
  - 标题/描述包含 JSP/页面/样式/显示 → 初判前端
  - 标题/描述包含 保存/提交/计算/校验/接口 → 初判后端
  - 无法判断 → 混合/待定
→ [可选] test-case-ref.lookup(bug.module) → 匹配相关测试用例数量
```

#### 2.3 展示分诊表格

向用户展示:

```markdown
## Bug 分诊台

共 N 个 Bug，初步分类如下:

| # | Bug ID | 标题               | 模块 | 初判类型 | 建议优先级 | 测试用例 | 操作       |
|---|--------|--------------------|------|----------|-----------|---------|------------|
| 1 | #5001  | T044 金额计算错误   | T044 | 后端     | 高        | 有 3 条  | [修复]     |
| 2 | #5003  | T051 保存报错       | T051 | 后端     | 中        | 无      | [修复]     |
| 3 | #5002  | T047 字段不显示     | T047 | 前端     | 中        | 有 12 条 | [标注前端] |
| 4 | #5004  | T044 页面样式问题   | T044 | 前端     | 低        | 有 3 条  | [跳过]     |

你可以:
1. 调整修复顺序（例如 "把 #5003 提到第1位"）
2. 修改操作标记（例如 "#5004 改为修复" 或 "#5001 先跳过"）
3. 修改优先级
4. 回复"确认"开始修复
```

#### 2.4 等待用户调整

**强制规则**: 必须等待用户确认修复队列后才进入 Phase 3。

用户可以:
- 调整顺序: "把 #5003 提到第1位"
- 标记跳过: "#5001 先跳过，下次再修"
- 标记前端: "#5003 改为标注前端"
- 标记修复: "#5004 改为修复"
- 全部确认: "确认"

#### 2.5 生成 fix-queue.json

根据用户确认的结果，生成 `yili-out/bug-prefetch/fix-queue.json`。

**单 Bug 模式**: 跳过 Phase 2，直接进入 Phase 3 修复。

---

### Phase 3: 批量修复 (Fix & Commit)

**目标**: 按 fix-queue 顺序逐个修复，每修一个 Bug 立即 commit 到本地，**不操作 Coding**。

#### action=fix 的 Bug

```
对 fix-queue 中 action=fix 的每个 Bug (按 priority 顺序):

  3.1 装载当前 Bug 记忆
      memory-setup.update(current_bug=bug-id, phase=analysis)
      → 读取上一个 Bug 沉淀的检查项
      → 继承 carry_forward_checks

  3.2 读取本地预采集数据
      → 读取 yili-out/bug-prefetch/{bug-id}/detail.txt
      → 读取 yili-out/bug-prefetch/{bug-id}/comments.txt
      → [可选] 查看 detail.png / comments.png 辅助理解
      → 合并为完整 Bug 上下文

  3.2.1 [可选] 加载相关测试用例参考
      test-case-ref.lookup(bug.module, bug.keywords)
      → 从 yili-out/test-case-index/test-case-index.json 检索
      → 按模板号(T044/T047) + 功能关键词匹配
      → 输出: 相关测试用例列表（操作步骤+预期结果）
      → 作为 yili-code-fix.analyze 的补充上下文
      → ⚠️ 仅供参考，测试用例不一定准确，不作为通过指标

  3.3 并行分析 (fork → join)
      以下子任务可并行执行，全部完成后合并分析结果:
      ├─ [A] yili-code-fix.analyze(bug-context)
      │   → 输出: 遗漏清单 + 前后端分类
      ├─ [B] test-case-ref.lookup (3.2.1 已加载则跳过)
      │   → 输出: 相关测试用例列表
      └─ [C] [可选] db-query.check-data
          → 查库了解数据现状
      → join: 合并遗漏清单 + 测试用例 + 数据现状

  3.4 输出分析方案
      向用户展示: 遗漏清单 + 修复计划

  3.5 等待用户确认 (受执行模式控制)
      → mode=interactive: ⏸️ 等待用户回复"确认"后继续，或"跳过"此 Bug
      → mode=offline: 自动跳过确认，直接执行修复

  3.6 执行修复
      yili-code-fix.fix(bug-context)

  3.7 编译验证
      mvn compile -pl <module> -am -T 1C
      → 编译失败自动修复重试（最多 3 次）

  3.7.1 [可选] 并行验证 (fork → join)
      以下子任务可并行执行:
      ├─ [A] fix-verify.discover-tests(modified_files) + run-tests
      │   → 根据修改的文件自动发现对应测试类
      │   → 匹配策略: 精确类名 > 包路径映射 > 同包递归 > 模块扫描
      │   → mvn test -pl <module> -Dtest=<tests> -DskipTests=false
      │   → 解析 Surefire 报告 → verdict (PASS/WARN/FAIL/SKIP)
      └─ [B] fix-verify.verify-data(bug_context)
          → 编排 db-query.check-data → 验证数据状态
          → [可选] db-query.trace-branch → 确认分支走向
          → [可选] db-query.verify-fix → 修复前后对比
          → ⚠️ 仅在 Bug 涉及数据操作时执行
      → join: 合并 unit_test + data_verify → verdict
      → ⚠️ 测试失败不自动阻塞，报告给用户决策

  3.8 [可选] 本地接口测试
      local-api-test → 本地启动服务 → curl 测试 → 验证响应
      [可选] db-query.verify-fix → 验证数据库变更

  3.9 git commit (提交到本地，不 push)
      git add <修改的文件>
      git commit -m "fix(<module>): #<bug-id> <标题>"
      → 每个 Bug 一个独立 commit，历史清晰
      → 仅本地提交，不推送远端

  3.10 单 Bug 复盘
      self-improving-agent.review(bug-result)
      → 提炼 missed signals / 新检查项
      → memory-setup.update(lessons learned)

  3.11 记录修复结果
      → 更新 fix-queue.json.results[bug-id]
      → status: "fixed"
      → files: [修改的文件列表]
      → compile: "pass"
      → unit_test: {verdict, total, passed, failed, skipped}
      → data_verify: {verdict, checks, passed}
      → commit_hash: "<本次 commit hash>"
      → comment_draft: "【AI修复】..." (评论草稿，Phase 5 使用)
```

#### action=tag-frontend 的 Bug

```
  读取本地预采集数据
  → 确认前端问题分析
  → 准备评论草稿: "【AI分析】前端问题, 对应老代码 xxx, 新框架不修改"
  → 查找前端负责人 (读取 fssc-schedule.xlsx)
  → 记录到 fix-queue.json.results[bug-id]:
    status: "tag-frontend"
    frontend_owner: "前端负责人"
    comment_draft: "【AI分析】..."
  → 不操作 Coding，等 Phase 5 统一处理
```

#### action=skip 的 Bug

```
  → 记录到 fix-queue.json.results[bug-id]:
    status: "skipped"
    reason: "用户标记跳过"
```

**关键**: Phase 3 全程不打开 Coding 浏览器，不推送远端。每修一个 Bug 立即 commit 到本地，保证每个 Bug 一个独立 commit。

---

### Phase 4: 统一推送 (Push)

**目标**: 所有 Bug 修复并 commit 后，统一拉取最新代码并推送到远端。

#### 4.1 展示本批次 commit 列表

```bash
git log --oneline origin/HEAD..HEAD
```

向用户展示:
```markdown
## 本批次 Commit 列表

| # | Commit | Bug ID | 标题 |
|---|--------|--------|------|
| 1 | abc1234 | #5001 | fix(claim-otc): T044 金额计算错误修复 |
| 2 | def5678 | #5003 | fix(claim-ptp): T051 保存报错修复 |

共 2 个 commit
```

#### 4.2 拉取最新代码

```
git pull --rebase
→ 将本地 commit 变基到最新远端代码之上
→ 保持线性提交历史
```

#### 4.3 冲突检测

```
有冲突:
  → 展示冲突文件列表
  → ⏸️ 暂停，等待用户手动解决
  → 用户解决后 git rebase --continue

无冲突:
  → 继续
```

#### 4.4 用户确认推送

```
⏸️ 向用户确认:
  "以上 N 个 commit 将推送到远端，是否确认 push？"
```

#### 4.5 推送

```
git push
→ 记录推送结果
```

---

### Phase 5: 统一闭环 (Finalize)

**目标**: 代码推送后，统一完成 CI 构建、SIT 验证和 Coding 平台操作。

#### 5.1 CI 构建发布

```
coding-ci-deploy
→ 触发对应模块 SIT 构建
→ 等待构建完成
→ 记录构建号和结果
→ 构建失败则 ⏸️ 通知用户，等待决策
```

#### 5.2 [可选] SIT 验证

```
对 fix-queue.results 中 status=fixed 的每个 Bug:
  sit-smoke-test → SIT 冒烟测试 + 截图
  sit-verify-analyze → 分析验证结果
    ├─ [全部通过]         → 标记为修复成功
    ├─ [API正确+页面错误]  → 标记为前端问题
    ├─ [API错误]          → 标记为后端未修复
    └─ [环境异常]         → 标记为环境问题
```

SIT 验证结果更新到 fix-queue.json.results:
```json
{
  "5001": {"status": "fixed", "sit_result": "pass", "sit_screenshot": "sit-verify-5001.png"},
  "5003": {"status": "fixed", "sit_result": "frontend-issue", "sit_screenshot": "sit-verify-5003.png"}
}
```

#### 5.3-5.4 批量操作 Coding

```
打开 Coding 浏览器（认证降级顺序）:
  1. 优先导入 config/coding-cookies.json（Phase 1 导出）
     → browser-use cookies import config/coding-cookies.json
     → 打开 Coding 页面，检查是否需要登录
  2. Cookie 过期 → 降级到 Chrome Profile
  3. Profile 无效 → 降级到 SSO 统一登录

遍历 fix-queue.results:

  [status=fixed, sit_result=pass]:
    coding-bug-ops.add-comment(bug-id, comment_draft)
    coding-bug-ops.update-status(bug-id, "待验证")
    coding-bug-ops.reassign(bug-id, --to-reporter)

  [status=fixed, sit_result=frontend-issue]:
    coding-bug-ops.add-comment(bug-id, "【后端已修复，前端展示问题】...")
    coding-bug-ops.update-remark(bug-id, "后端已修复，前端展示问题")
    coding-bug-ops.reassign(bug-id, --to <前端处理人>)

  [status=fixed, sit_result=api-error]:
    coding-bug-ops.add-comment(bug-id, "【SIT验证未通过】...")
    → ⏸️ 通知用户，等待决策

  [status=tag-frontend]:
    coding-bug-ops.add-comment(bug-id, comment_draft)
    coding-bug-ops.reassign(bug-id, --to <frontend_owner>)

  [status=skipped]:
    不操作

关闭浏览器
```

#### 5.5-5.6 复盘和报告

```
全局复盘 (self-improving-agent)
→ 汇总跨 Bug 的共性失误、有效策略、建议更新项

输出汇总报告
```

---

## 汇总报告格式

```markdown
## Bug 修复汇总报告

### 处理统计
- 总数: N 个 Bug
- 后端修复: X 个
- 前端标注: Y 个
- 前端转派: W 个
- 跳过: Z 个

### 后端修复列表
| Bug ID | 标题 | 修改文件 | 编译 | SIT | 状态 | 转派 | Commit |
|--------|------|---------|------|-----|------|------|--------|
| #5001 | T044 金额计算 | SaveClaimServiceImpl.java | 通过 | 通过 | 待验证 | 发起人 | abc1234 |

### 前端标注/转派列表
| Bug ID | 标题 | 前端问题说明 | 转派给 |
|--------|------|------------|--------|
| #5002 | T047 字段不显示 | API正确，页面未展示 | 前端lisi |

### 跳过列表
| Bug ID | 标题 | 跳过原因 |
|--------|------|---------|
| #5004 | T044 页面样式 | 低优先级，暂不处理 |

### SIT 测试结果
| Bug ID | 测试场景 | 结果 | 截图 |
|--------|---------|------|------|
| #5001 | T044 冒烟测试 | 通过 | sit-verify-5001.png |

### Git 提交记录
| Commit | 消息 | Bug |
|--------|------|-----|
| abc1234 | fix(claim-otc): #5001 T044 金额计算错误修复 | #5001 |
| def5678 | fix(claim-ptp): #5003 T051 保存报错修复 | #5003 |

### CI 构建
- 构建号: #123
- 状态: 成功
- 模块: claim-otc, claim-ptp

### 自改进摘要
- 新增检查项: ...
- 重复失误: ...
- 下轮默认动作: ...
```

---

## 单 Bug 模式兼容

单 Bug 模式下，流程简化为:

```
输入: Bug ID
  │
  ├─ 跳过 Phase 1/2
  │
  ├─ Phase 3 (直接修复):
  │   ├─ 实时读取 Bug 详情+评论 (coding-bug-ops)
  │   ├─ 分析 → 确认 → 修复 → 编译 → [本地测试]
  │   └─ 复盘
  │
  ├─ Phase 4 (提交):
  │   ├─ git-commit-push
  │   └─ [可选] coding-ci-deploy
  │
  └─ Phase 5 (闭环):
      ├─ [可选] SIT 验证
      ├─ coding-bug-ops 评论+状态+转派
      └─ 报告
```

单 Bug 模式保持原有交互体验，不强制使用预采集和分诊台。

---

## 关键设计点

### 1. 分诊台确认机制

- 批量模式下**必须**经过分诊台确认修复队列
- 用户可以调整优先级、标记跳过、修改操作类型
- 防止盲目修复，提升全局掌控感

### 2. 代码修复与 Coding 操作解耦

- Phase 3 纯粹做代码修复，不操作 Coding 浏览器
- Phase 5 集中处理所有 Coding 操作
- 减少浏览器开关次数，降低认证失效风险

### 3. 评论草稿机制

- Phase 3 修复时准备评论草稿 (comment_draft)
- Phase 5 统一闭环时使用草稿评论
- 草稿保存在 fix-queue.json 中，不丢失

### 4. 错误恢复

- 预采集失败: 单个 Bug 采集失败不阻塞其他 Bug
- 编译失败: 自动重试 3 次
- SIT 验证失败: 记录结果，不阻塞其他 Bug 的 Coding 操作
- Coding 操作失败: 重试 1 次，失败则本地保存评论内容

### 5. 数据安全

- 不在生产环境执行任何操作
- 修改代码前可以通过 `--dry-run` 预览
- Bug 状态更新默认需要手动确认
- fix-queue.json 记录完整操作日志

### 6. 记忆与自改进闭环

- `memory-setup` 负责在长流程中维持一致上下文
- `self-improving-agent` 负责把单次经验转成下一次可复用检查项
- Phase 3 每个 Bug 复盘 + Phase 5 全局复盘

---

## 强制约束

1. **分诊台确认**: 批量模式下必须经过 Phase 2 分诊台确认，不自动开始修复
2. **用户确认**: 每个 Bug 修复前（Phase 3.5）须等待用户确认（`mode=offline` 时自动跳过）
3. **代码与 Coding 解耦**: Phase 3 不操作 Coding，Phase 5 统一处理
4. **评论完整**: 添加到 Coding 的评论必须包含老代码位置、修复说明
5. **编译验证**: 修复后必须编译通过
6. **截图存证**: SIT 测试必须截图
7. **不改生产**: 只在 SIT/UAT 环境测试
8. **评论必读**: 读取 Bug 时必须同时读评论（Phase 1 预采集时完成）
9. **分层遵守**: 修复代码遵守 agents.md 分层规范
10. **用户规则**: 遵守 user-rules.md 中"不修改代码、需要变更请重写"原则
11. **记忆先行**: 进入批量流程前必须初始化运行记忆
12. **每 Bug 复盘**: 每个 Bug 结束后必须做一次简短自改进复盘
13. **本地存储**: 预采集数据和修复队列必须持久化到 yili-out/bug-prefetch/

## 参考

- 编排流程图: [references/pipeline-flow.md](references/pipeline-flow.md)
- 运行记忆: `ai-spec/skills/code/bug-fix-cycle/memory-setup/SKILL.md`
- Coding 操作: `ai-spec/skills/code/bug-fix-cycle/coding-bug-ops/SKILL.md`
- 代码修复: `ai-spec/skills/code/bug-fix-cycle/yili-code-fix/SKILL.md`
- 本地测试: `ai-spec/skills/code/bug-fix-cycle/local-api-test/SKILL.md`
- 代码提交: `ai-spec/skills/code/bug-fix-cycle/git-commit-push/SKILL.md`
- CI 发布: `ai-spec/skills/code/bug-fix-cycle/coding-ci-deploy/SKILL.md`
- SIT 测试: `ai-spec/skills/code/bug-fix-cycle/sit-smoke-test/SKILL.md`
- 验证分析: `ai-spec/skills/code/bug-fix-cycle/sit-verify-analyze/SKILL.md`
- 数据库查询: `ai-spec/skills/code/bug-fix-cycle/db-query/SKILL.md`
- 测试用例参考: `ai-spec/skills/code/bug-fix-cycle/test-case-ref/SKILL.md`
- 修复验证: `ai-spec/skills/code/bug-fix-cycle/fix-verify/SKILL.md`
- 自改进复盘: `ai-spec/skills/code/bug-fix-cycle/self-improving-agent/SKILL.md`
- 项目规范: `.qoder/rules/agents.md`
- 个人偏好: `.qoder/rules/user-rules.md`
