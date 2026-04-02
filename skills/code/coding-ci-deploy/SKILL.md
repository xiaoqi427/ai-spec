---
name: coding-ci-deploy
description: 在 Coding CI/CD 平台触发 SIT 环境构建部署。代码提交后，通过 Coding 构建计划页面触发对应模块的 SIT 构建，等待构建完成并截图确认。当用户需要发布代码到 SIT 环境时使用。
allowed-tools: Bash(browser-use:*)
---
# Coding CI Deploy (CI 发布部署)
@author: sevenxiao

## 概述

代码提交后，在 Coding CI/CD 平台触发 SIT 环境构建部署，等待构建完成并截图确认。

**流程**: 登录 Coding → 打开 CI 页面 → sit 标签 → 搜索构建计划 → 触发构建 → 等待完成 → 截图

## 外部依赖

| 外部 Skill | 安装命令 | 说明 |
|------------|----------|------|
| `browser-use` | `npx openskills add browser-use/browser-use@browser-use` | 浏览器自动化 CLI |

---

## 使用方式

```bash
# 发布 config 模块到 SIT
/skill coding-ci-deploy config

# 发布 claim-base 模块到 SIT
/skill coding-ci-deploy claim-base

# 发布前端到 SIT
/skill coding-ci-deploy web
```

---

## Coding CI 页面信息

**CI 构建计划页面**: `https://yldc.coding.yili.com/p/fssc/ci/job`

页面结构：
```
┌──────────────────────────────────────────┐
│  构建计划                                │
│                                          │
│  [我的星标] [系统来源] [全部] [未分组]     │
│  [测试分组] [sit] [uat] [公共] [更多]     │
│                                          │
│  触发者: 所有人触发的  计划来源: 自定义    │
│  🔍 搜索...                              │
│                                          │
│  ┌─────────────┐  ┌─────────────┐        │
│  │ fssc-xxx-sit│  │ fssc-yyy-sit│  ...   │
│  │ ✅ 构建成功  │  │ ✅ 构建成功  │        │
│  │ 张三 手动触发│  │ 李四 手动触发│        │
│  │ #100 ◇ abc │  │ #50  ◇ def │        │
│  │ ▶ 📷 🔄    │  │ ▶ 📷 🔄    │        │
│  └─────────────┘  └─────────────┘        │
└──────────────────────────────────────────┘
```

---

## 模块 → 构建计划映射

| 模块简称 | 搜索关键字 | 构建计划名称（实测） |
|----------|-----------|---------------------|
| `config` | `config` | `fssc-config-servcie-sit` |
| `web` | `web` | `fssc-web-sit` |
| `claim-base` | `claim-base` | `fssc-claim-base-servcie-sit` |
| `claim-ptp` | `claim-ptp` | `fssc-claim-ptp-servcie-sit` |
| `claim-tr` | `claim-tr` | `fssc-claim-tr-servcie-sit` |
| `claim-rtr` | `claim-rtr` | `fssc-claim-rtr-servcie-sit` |
| `claim-eer` | `claim-eer` | `fssc-claim-eer-servcie-sit` |
| `claim-fa` | `claim-fa` | `fssc-claim-fa-servcie-sit` |
| `claim-otc` | `claim-otc` | `fssc-claim-otc-servcie-sit` |
| `gateway` | `gateway` | `fssc-gateway-servcie-sit` |
| `pi` | `pi` | `fssc-pi-servcie-sit` |
| `integration` | `integration` | `fssc-integration-servcie-sit` |
| `fund` | `fund` | `fssc-fund-servcie-sit` |
| `image` | `image` | `fssc-image-servcie-sit` |

> **注意**: 构建计划名称中 service 拼写为 `servcie`（历史原因），搜索时用模块关键字即可。

---

## 发布流程（5 步）

### Step 1: 登录 Coding（复用 coding-bug-ops 认证策略）

```bash
# 优先使用 Chrome Profile
browser-use --profile "Default" open "https://yldc.coding.yili.com/p/fssc/ci/job"

# 视口覆写（防止移动端拦截）
browser-use eval "
  Object.defineProperty(window, 'innerWidth', {value: 1920, writable: true, configurable: true});
  Object.defineProperty(window, 'innerHeight', {value: 1080, writable: true, configurable: true});
  Object.defineProperty(document.documentElement, 'clientWidth', {value: 1920, writable: true, configurable: true});
  window.dispatchEvent(new Event('resize'));
"
browser-use eval "location.reload()"
```

如果被重定向到登录页 → 使用 SSO 统一登录：
```bash
# 参考 coding-bug-ops 的 SSO 登录流程
# sso_username / sso_password 从 config/coding-auth.yaml 读取
```

---

### Step 2: 选择 sit 标签

```bash
# 等待页面加载
browser-use wait text "构建计划"

# 获取页面状态
browser-use state

# 找到 "sit" 标签并点击
browser-use click <sit-tab-idx>

# 等待列表刷新
browser-use wait text "sit"
```

---

### Step 3: 搜索对应的构建计划

```bash
# 找到搜索框
browser-use state

# 在搜索框中输入模块关键字
browser-use click <search-input-idx>
browser-use input <search-input-idx> "<模块关键字>"

# 等待搜索结果
browser-use wait selector "[class*=job], [class*=Job], [class*=plan]"

# 截图确认找到了正确的构建计划
browser-use screenshot ci-search-result.png
browser-use state
```

---

### Step 4: 触发构建

```bash
# 在搜索结果中找到对应构建计划的 ▶ 播放按钮
browser-use state

# 点击播放/触发按钮
browser-use click <play-btn-idx>

# 可能弹出确认对话框，点击确认
browser-use state
browser-use click <confirm-btn-idx>

# 等待构建开始
browser-use wait text "构建中"
browser-use screenshot ci-building.png
```

---

### Step 5: 等待构建完成 + 截图

```bash
# 持续检查构建状态（每 30 秒检查一次，最多等 10 分钟）
# 构建通常耗时 2-7 分钟

browser-use eval "
  // 检查构建状态
  const statusEl = document.querySelector('[class*=status], [class*=Status]');
  statusEl ? statusEl.innerText : '状态未知';
"

# 构建完成后截图
browser-use screenshot ci-build-result.png

# 提取构建结果信息
browser-use eval "document.body.innerText.slice(0, 5000)"
```

**判断结果**:
- `构建成功` ✅ → 部署完成，可以进行 SIT 测试
- `构建失败` ❌ → 截图 + 提取错误日志，报告给用户

**构建完成输出格式**:
```markdown
## CI 构建结果

- **构建计划**: fssc-config-servcie-sit
- **构建状态**: ✅ 构建成功
- **触发人**: 肖祺-xiaoqi1-IBM
- **耗时**: 5 分钟 30 秒
- **构建号**: #XXX
- **Commit**: <commit-hash>
- **截图**: [构建结果截图](ci-build-result.png)
```

---

## 认证策略

复用 `coding-bug-ops` 的认证策略和配置文件：
- 配置文件: `ai-spec/skills/code/coding-bug-ops/config/coding-auth.yaml`
- 优先级: Chrome Profile → Cookie → SSO 统一登录
- 视口覆写: 每次打开页面后必须执行

---

## 强制约束

1. **视口覆写**: 每次打开 Coding 页面后必须执行视口覆写
2. **确认构建计划**: 触发前截图确认找到的是正确的构建计划
3. **等待完成**: 不要触发后就结束，必须等构建完成并截图
4. **构建失败处理**: 失败时提取错误日志，不要忽略
5. **不重复触发**: 如果已有正在进行的构建，不要重复触发
6. **认证复用**: 使用 coding-bug-ops 的认证配置，不要重复配置
