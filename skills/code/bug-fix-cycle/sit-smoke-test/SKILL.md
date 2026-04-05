---
name: sit-smoke-test
description: SIT 环境自动化做单验证，支持报账单冒烟测试、场景测试、页面截图。基于 agent-browser、browser-use 和 playwright-e2e-testing 实现。默认优先使用 agent-browser，可独立使用，也可被 bug-fix-pipeline 调用。当用户需要在 SIT 环境验证报账单功能、做冒烟测试、验证 Bug 修复效果时使用。
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*), Bash(browser-use:*), Bash(npx:playwright)
---
# SIT Smoke Test (SIT 环境自动化做单验证)
@author: sevenxiao

## 概述

此 skill 专注于在 **SIT 测试环境** 中进行自动化做单验证，可独立使用也可被 `bug-fix-pipeline` 调用。

核心能力:
1. **`login`** - 登录 SIT 环境
2. **`navigate`** - 根据报账单类型导航到对应页面
3. **`smoke-test`** - 冒烟测试: 页面渲染检查 + 关键操作验证
4. **`scenario-test`** - 场景测试: 新建→填写→保存→提交→验证
5. **`screenshot`** - 关键步骤截图留存证据

## 外部依赖

| 外部 Skill | 安装命令 | 说明 |
|------------|----------|------|
| `agent-browser` | 按项目环境单独安装或配置 | 默认首选。用于打开页面、复现步骤、截图取证和轻量交互验证 |
| `browser-use` | `npx openskills add browser-use/browser-use@browser-use` | 需要复用 Chrome Profile、Cookie 和现有登录态时作为降级方案 |
| `playwright-e2e-testing` | `npx openskills add bobmatnyc/claude-mpm-skills@playwright-e2e-testing` | 需要稳定断言、可重复执行脚本和正式回归时使用 |

安装后执行:
```bash
browser-use doctor           # 验证 browser-use
npx playwright install       # 安装 Playwright 浏览器
```

使用建议:

- `sit-smoke-test` 被 `bug-fix-pipeline` 调用时，默认先走 `agent-browser`
- 需要复用登录态、现有 Chrome Profile、Cookie 或既有 CLI 流程时，再退回 `browser-use`
- 需要稳定回归、断言和可重复执行脚本时使用 `playwright-e2e-testing`
- 上述能力都属于联调/冒烟/E2E 范畴，不属于单元测试依赖

复用的已有 skill:
- `front-end-skills` (`ai-spec/skills/code/front-end-skills/`) - 路由解析脚本和浏览器测试模式

---

## 使用方式

```bash
# 对指定报账单类型做冒烟测试
/skill sit-smoke-test T044

# 指定 SIT 页面 URL 做冒烟测试
/skill sit-smoke-test --url http://pri-fssc-web-sit.digitalyili.com/#/claim/T044

# 验证某个 Bug 修复后的场景
/skill sit-smoke-test --bug 4992

# 对多个报账单类型批量冒烟测试
/skill sit-smoke-test T044 T047 T051

# 执行场景测试（新建→保存→提交）
/skill sit-smoke-test T044 --scenario create-save-submit
```

---

## SIT 测试环境

| 配置项 | 值 |
|--------|-----|
| URL | `http://pri-fssc-web-sit.digitalyili.com` |
| UAT URL | `http://pri-fssc-web-uat.digitalyili.com` |
| 默认账号 | fsscadmin |
| 默认密码 | 2 |
| 已有 Playwright 配置 | `fssc-web/playwright.config.ts` |
| 已有测试目录 | `fssc-web/tests/smoke/` |

---

## 浏览器执行策略

按优先级依次尝试:

### 1. `agent-browser` 默认执行（优先）

适用场景:

- `bug-fix-pipeline` 中的 SIT 页面打开、Bug 复现、关键按钮点击、截图存证
- 不依赖本机真实 Chrome Profile 的标准验证流程
- 如果在 Codex/macOS 下运行，优先使用 `$HOME/.agents/skills/agent-browser/scripts/agent-browser-codex.sh`，不要直接走 `npx -y agent-browser`

Codex/macOS 额外说明:

- 该环境里 `node -p 'process.arch'` 可能是 `arm64`，而 shell 实际跑在 `x86_64/i386`
- `agent-browser` 的 `npx` 包装层按 Node 架构选 native binary，可能因此选错并表现为无输出
- 快速自检:

```bash
AGENT_BROWSER_CODEX_HELPER="${AGENT_BROWSER_CODEX_HELPER:-$HOME/.agents/skills/agent-browser/scripts/agent-browser-codex.sh}"
bash "$AGENT_BROWSER_CODEX_HELPER" doctor
```

- 如果 `~/.agent-browser/<session>.log` 出现 `Failed to bind socket: Operation not permitted`，说明 daemon 被沙箱拦截，应立即提权，不要继续原地重试

典型流程:

```bash
AGENT_BROWSER_CODEX_HELPER="${AGENT_BROWSER_CODEX_HELPER:-$HOME/.agents/skills/agent-browser/scripts/agent-browser-codex.sh}"
bash "$AGENT_BROWSER_CODEX_HELPER" --session sitSmoke open "http://pri-fssc-web-sit.digitalyili.com/#/claim/T044"
bash "$AGENT_BROWSER_CODEX_HELPER" --session sitSmoke wait --load networkidle
bash "$AGENT_BROWSER_CODEX_HELPER" --session sitSmoke snapshot -i
bash "$AGENT_BROWSER_CODEX_HELPER" --session sitSmoke screenshot sit-smoke-T044.png
```

### 2. `browser-use` 复用登录态（降级）

适用场景:

- 必须复用本机 Chrome Profile、Cookie、现有登录态
- 已有脚本、账号或认证资料是基于 `browser-use` 维护的

### 3. Playwright 脚本回归

适用场景:

- 需要把临时验证沉淀成正式回归脚本
- 需要稳定断言、报告和可重复执行能力

## 认证策略

当需要复用真实浏览器登录态时，按优先级依次尝试：

### 公共前置步骤：视口覆写

**所有 `browser-use open` 之后，立即注入 1920x1080 视口**，与 coding-bug-ops 保持一致：

```bash
browser-use eval "
  Object.defineProperty(window, 'innerWidth', {value: 1920, writable: true, configurable: true});
  Object.defineProperty(window, 'innerHeight', {value: 1080, writable: true, configurable: true});
  Object.defineProperty(document.documentElement, 'clientWidth', {value: 1920, writable: true, configurable: true});
  window.dispatchEvent(new Event('resize'));
"
```

### 0. Chrome Debug 模式（最推荐，长期稳定）

直接连接用户正在使用的 Chrome 浏览器实例，继承所有登录状态：

```bash
# 前提: 用户已以 Debug 端口启动 Chrome
# /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

browser-use --connect open "http://pri-fssc-web-sit.digitalyili.com"
# → 执行视口覆写（公共前置步骤）
browser-use state
# 检查是否在登录页 → 如果不是，认证成功
```

优势：无需 Cookie 提取/解密，无需密码存储，只要 Chrome 已登录就能用。

### 1. Cookie 文件导入（优先，最稳定）

```bash
browser-use cookies import config/sit-cookies.json
browser-use open "http://pri-fssc-web-sit.digitalyili.com"
# → 执行视口覆写（公共前置步骤）
browser-use state
# 检查是否在登录页 → 如果不是，认证成功
```

### 1.5 Chrome Cookie 提取（Cookie 文件不存在或过期时）

当 Cookie 文件不存在、或导入后仍在登录页时，**自动从当前 Chrome 提取 SIT Cookie**：

```bash
# 从 Chrome 数据库提取 SIT 域名的 Cookie → 保存到 sit-cookies.json
python3 ai-spec/skills/code/bug-fix-cycle/bug-fix-pipeline/scripts/extract-chrome-cookies.py \
  --domain pri-fssc-web-sit.digitalyili.com \
  --output config/sit-cookies.json

# 提取成功后，走 Cookie 文件导入
browser-use cookies import config/sit-cookies.json
browser-use open "http://pri-fssc-web-sit.digitalyili.com"
# → 执行视口覆写（公共前置步骤）
browser-use state
# 检查是否在登录页 → 如果不是，认证成功
```

### 2. Chrome Profile 复用（降级）

```bash
browser-use --profile "Default" open "http://pri-fssc-web-sit.digitalyili.com"
# → 执行视口覆写（公共前置步骤）
browser-use state
# 检查是否在登录页 → 如果不是，认证成功
```

### 3. 账号密码登录（兜底）

从 `config/sit-auth.yaml` 读取配置:

```bash
browser-use open "http://pri-fssc-web-sit.digitalyili.com"
# → 执行视口覆写（公共前置步骤）
browser-use wait text "登录"
browser-use state

# 输入用户名
browser-use input <username-idx> "fsscadmin"
# 输入密码
browser-use input <password-idx> "2"
# 点击登录
browser-use click <login-btn-idx>

# 验证登录成功
browser-use wait text "首页"
browser-use screenshot sit-login-success.png
```

### 认证验证 + Cookie 导出

```bash
browser-use state
# 检查 URL 是否包含 /login → 未登录
# 检查页面是否有"首页"/"工作台" → 已登录

# 登录成功后立即导出 Cookie（供后续复用）
browser-use cookies export config/sit-cookies.json
```

---

## 核心能力

### login (登录 SIT 环境)

按认证策略顺序尝试登录，确保进入系统主页。

**成功标准**:
- URL 不包含 `/login`
- 页面包含"首页"或"工作台"关键词
- 截图存证

---

### navigate (导航到报账单页面)

**输入**: 报账单模板编号 (如 T044) 或完整 URL

**执行步骤**:

```bash
# 方式1: 通过路由导航
browser-use open "http://pri-fssc-web-sit.digitalyili.com/#/claim/T044"

# 方式2: 通过菜单导航
browser-use state
# 找到"报账管理"菜单
browser-use click <claim-menu-idx>
browser-use state
# 找到对应报账单类型
browser-use click <target-claim-idx>

# 验证导航成功
browser-use wait selector "[class*=detail], [class*=search], [class*=table]"
browser-use state
browser-use screenshot sit-navigate.png
```

**报账单路由映射** (参考 front-end-skills):

| 模板编号 | 预期路由 | 页面类型 |
|----------|---------|---------|
| T001 | `/claim/T001` | 差旅报账 |
| T010 | `/claim/T010` | 采购报账 |
| T044 | `/claim/T044` | 杂项采购 |
| T047 | `/claim/T047` | 费用报账 |
| T049 | `/claim/T049` | 杂项报账 |
| T051 | `/claim/T051` | 税单报账 |
| T060 | `/claim/T060` | 应收报账 |
| T065 | `/claim/T065` | 差旅特殊 |

如果路由不确定，可用路由解析脚本:
```bash
python3 ai-spec/skills/code/front-end-skills/scripts/route-open.py T044
```

---

### smoke-test (冒烟测试)

**目标**: 验证页面基础可用性

**最小检查项**:

| 检查项 | 说明 | 验证方式 |
|--------|------|---------|
| 页面加载 | 页面不是白屏/404/登录页 | `browser-use state` 检查 URL 和内容 |
| 标题区域 | 页面标题或主区域出现 | `browser-use state` 检查标题元素 |
| 查询条件 | 搜索条件区渲染 | 查找 input/select 元素 |
| 数据表格 | 表格或主内容区渲染 | 查找 table/列表元素 |
| 关键按钮 | 新建/查询/导出等按钮可见 | 查找 button 元素 |
| 无报错 | 控制台无明显错误 | `browser-use eval "..."` 检查错误 |

**执行步骤**:

```bash
# 1. 打开页面
browser-use --connect open "<sit-url>/#/claim/T{XXX}"

# 2. 等待加载
browser-use wait selector "[class*=page], [class*=container]"

# 3. 检查页面状态
browser-use state

# 4. 全页截图
browser-use screenshot --full sit-smoke-T{XXX}.png

# 5. 检查是否有明显错误
browser-use eval "
  const errors = [];
  // 检查是否有错误提示
  document.querySelectorAll('[class*=error], [class*=Error], .el-message--error').forEach(el => {
    errors.push(el.innerText.trim());
  });
  // 检查是否白屏
  if (document.body.innerText.trim().length < 50) {
    errors.push('页面可能白屏: 内容过少');
  }
  errors.length > 0 ? JSON.stringify(errors) : '无明显错误';
"

# 6. 检查关键元素是否存在
browser-use eval "
  const checks = {
    hasTitle: !!document.querySelector('h1, h2, [class*=title], [class*=Title]'),
    hasTable: !!document.querySelector('table, [class*=table], [class*=Table]'),
    hasButton: !!document.querySelector('button, [class*=btn], [class*=Button]'),
    hasInput: !!document.querySelector('input, [class*=input], [class*=Input]'),
  };
  JSON.stringify(checks, null, 2);
"

# 7. 尝试点击"查询"按钮
browser-use state
# 找到查询按钮
browser-use click <query-btn-idx>
browser-use wait selector "[class*=table], [class*=list]"
browser-use screenshot sit-smoke-T{XXX}-query.png
```

**输出格式**:
```markdown
## 冒烟测试结果: T{XXX}

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 页面加载 | 通过/失败 | {说明} |
| 标题区域 | 通过/失败 | {说明} |
| 查询条件 | 通过/失败 | {说明} |
| 数据表格 | 通过/失败 | {说明} |
| 关键按钮 | 通过/失败 | {说明} |
| 无报错 | 通过/失败 | {说明} |

截图: `sit-smoke-T{XXX}.png`
```

---

### scenario-test (场景测试)

**目标**: 模拟用户完整做单流程

**常见场景**:

#### 场景1: 新建-保存 (create-save)

```bash
# 1. 点击"新建"按钮
browser-use state
browser-use click <new-btn-idx>
browser-use wait selector "[class*=detail], [class*=form]"
browser-use screenshot sit-scenario-new.png

# 2. 填写必填字段
browser-use state
# 根据页面元素逐个填写
browser-use input <field-idx> "<value>"
browser-use screenshot sit-scenario-fill.png

# 3. 点击"保存"
browser-use state
browser-use click <save-btn-idx>

# 4. 验证保存成功
browser-use wait text "保存成功"
browser-use screenshot sit-scenario-saved.png
```

#### 场景2: 新建-保存-提交 (create-save-submit)

在场景1基础上:
```bash
# 5. 点击"提交"
browser-use state
browser-use click <submit-btn-idx>

# 6. 确认提交
browser-use state
browser-use click <confirm-btn-idx>

# 7. 验证提交成功
browser-use wait text "提交成功"
browser-use screenshot sit-scenario-submitted.png
```

#### 场景3: Bug 验证 (bug-verify)

```bash
# 1. 根据 Bug 描述的复现步骤操作
# 2. 到达 Bug 触发点
# 3. 验证 Bug 是否已修复
# 4. 截图存证
browser-use screenshot sit-bug-verify-{bug-id}.png
```

---

### screenshot (截图)

```bash
# 当前视口截图
browser-use screenshot <filename>.png

# 全页截图
browser-use screenshot --full <filename>.png
```

截图保存在当前工作目录，文件名建议格式:
- `sit-smoke-T{XXX}.png` - 冒烟测试
- `sit-scenario-{action}.png` - 场景测试步骤
- `sit-bug-verify-{bug-id}.png` - Bug 验证

---

## 与 Playwright 集成

对于需要持久化测试脚本的场景，使用 Playwright 编写:

### 已有配置

```
fssc-web/playwright.config.ts     # Playwright 配置
fssc-web/tests/smoke/             # 冒烟测试目录
```

### 编写 Playwright 测试

```typescript
// fssc-web/tests/smoke/t044-smoke.spec.ts
import { test, expect } from '@playwright/test';

test.describe('T044 杂项采购报账单', () => {
  test.beforeEach(async ({ page }) => {
    // 使用 storageState 跳过登录
    await page.goto('/#/claim/T044');
    await page.waitForLoadState('networkidle');
  });

  test('页面加载正常', async ({ page }) => {
    await expect(page.locator('[class*=title]')).toBeVisible();
    await expect(page.locator('table, [class*=table]')).toBeVisible();
  });

  test('查询功能正常', async ({ page }) => {
    await page.getByRole('button', { name: /查询/ }).click();
    await page.waitForLoadState('networkidle');
    await expect(page.locator('table')).toBeVisible();
  });
});
```

### 运行 Playwright 测试

```bash
# 设置 SIT 环境 URL
export PLAYWRIGHT_BASE_URL=http://pri-fssc-web-sit.digitalyili.com

# 运行冒烟测试
cd fssc-web
npx playwright test tests/smoke/t044-smoke.spec.ts

# 查看报告
npx playwright show-report
```

---

## 常见失败类型及处理

| 失败类型 | 现象 | 处理方式 |
|----------|------|---------|
| 登录失效 | 页面跳转到登录页 | 重新执行认证流程 |
| 页面白屏 | 内容区域空白 | 检查路由是否正确，检查控制台错误 |
| 404 | 页面未找到 | 确认路由配置，使用路由解析脚本 |
| 接口报错 | 页面显示错误提示 | 检查后端服务是否正常 |
| 权限不足 | 提示无权限 | 确认测试账号权限配置 |
| 加载超时 | 页面一直 loading | 增加等待时间或检查网络 |

---

## 强制约束

1. **执行优先级**: `agent-browser` → `browser-use` → `playwright-e2e-testing`
2. **认证优先级**: 在进入 `browser-use` 认证分支后，按 Chrome Debug (`--connect`) → Cookie 文件 → Chrome Profile → 账号密码执行
3. **截图存证**: 每个关键步骤必须截图
4. **不猜测路由**: 路由从代码或路由解析脚本推导，不要猜
5. **超时处理**: 页面加载超时默认 60 秒
6. **SIT 环境专用**: 不要在生产环境执行测试
7. **测试数据**: 使用测试账号和测试数据，不要影响正式数据

## 参考

- SIT 页面路由: [references/sit-pages.md](references/sit-pages.md)
- 测试场景模板: [references/test-scenarios.md](references/test-scenarios.md)
- 认证配置模板: [config/sit-auth.yaml.example](config/sit-auth.yaml.example)
- browser-use CLI: `.agents/skills/browser-use/SKILL.md`
- Playwright 指南: `.agents/skills/playwright-e2e-testing/SKILL.md`
- 前端 skill: `ai-spec/skills/code/front-end-skills/SKILL.md`
- 浏览器测试模式: `ai-spec/skills/code/front-end-skills/references/browser-test-patterns.md`
- Playwright 配置: `fssc-web/playwright.config.ts`
