---
name: bug-fix-pipeline
description: Coding Bug 全流程自动修复编排器。从 Coding 平台读取 Bug 列表 → 分析老新代码 → 判断前后端 → 修复后端 → SIT 验证 → 更新 Bug 状态。编排 coding-bug-ops、yili-code-fix、sit-smoke-test 三个 skill 完成端到端自动化。当用户需要批量或单个修复 Coding Bug 时使用。
---
# Bug Fix Pipeline (全流程自动修复编排器)

@author: sevenxiao

## 概述

此 skill 是**全流程编排器**，协调以下 7 个 skill 完成 Coding Bug 从发现到修复闭环的端到端自动化:

```
bug-fix-pipeline
  ├── coding-bug-ops      → 读/写 Coding Bug (描述+评论+转派+备注)
  ├── yili-code-fix       → 代码分析 + 修复
  ├── local-api-test      → 本地启动 + curl 测试接口
  ├── git-commit-push     → 代码提交 (pull→冲突检测→人工确认→push)
  ├── coding-ci-deploy    → CI 构建发布到 SIT
  ├── sit-smoke-test      → SIT 环境做单验证
  └── sit-verify-analyze  → SIT 验证后分析 + 路由决策
```

## 外部依赖


| 外部 Skill               | 安装命令                                                                | 说明                                                            |
| ------------------------ | ----------------------------------------------------------------------- | --------------------------------------------------------------- |
| `agent-browser`          | 按项目环境单独安装或配置                                                | `bug-fix-pipeline` 默认首选的浏览器验证能力，用于复现、截图和修复回归 |
| `browser-use`            | `npx openskills add browser-use/browser-use@browser-use`                | 需要复用本机 Chrome Profile、Cookie、登录态时作为降级方案       |
| `playwright-e2e-testing` | `npx openskills add bobmatnyc/claude-mpm-skills@playwright-e2e-testing` | 需要稳定回归脚本、断言和可重复执行测试时使用                    |

说明:

- `bug-fix-pipeline` 中凡是“打开 SIT 页面、按步骤复现、截图存证、验证修复”这类浏览器任务，默认优先使用 `agent-browser`
- 只有在必须复用登录态、现有浏览器 Profile、Cookie 或沿用现成 CLI 脚本时，才退回 `browser-use`
- 需要沉淀为正式可复跑回归脚本时，再使用 `playwright-e2e-testing`
- 上述能力都属于联调/冒烟/E2E 范畴，不属于单元测试依赖

内部依赖 (无需安装):


| Skill                | 位置                                      |
| -------------------- | ----------------------------------------- |
| `coding-bug-ops`     | `ai-spec/skills/code/coding-bug-ops/`     |
| `yili-code-fix`      | `ai-spec/skills/code/yili-code-fix/`      |
| `local-api-test`     | `ai-spec/skills/code/local-api-test/`     |
| `git-commit-push`    | `ai-spec/skills/code/git-commit-push/`    |
| `coding-ci-deploy`   | `ai-spec/skills/code/coding-ci-deploy/`   |
| `sit-smoke-test`     | `ai-spec/skills/code/sit-smoke-test/`     |
| `sit-verify-analyze` | `ai-spec/skills/code/sit-verify-analyze/` |
| `compare-transform`  | `ai-spec/skills/code/compare-transform/`  |
| `transform-claim`    | `ai-spec/skills/code/transform-claim/`    |
| `front-end-skills`   | `ai-spec/skills/code/front-end-skills/`   |

---

## 使用方式

### 单 Bug 模式

```bash
# 修复指定 Bug
/skill bug-fix-pipeline #4992

# 修复指定 Bug，跳过 SIT 测试
/skill bug-fix-pipeline #4992 --skip-sit

# 修复指定 Bug，只分析不修复
/skill bug-fix-pipeline #4992 --dry-run
```

### 批量模式

```bash
# 从筛选器 URL 批量修复
/skill bug-fix-pipeline --filter https://yldc.coding.yili.com/p/fssc/all/issues?filter=f209a5d4938a2da58718629a2f35419a

# 批量模式，只分析不修复
/skill bug-fix-pipeline --filter <url> --dry-run
```

### 参数说明


| 参数             | 说明              | 默认值             |
| ---------------- | ----------------- | ------------------ |
| `#<bug-id>`      | 单个 Bug ID       | -                  |
| `--filter <url>` | Coding 筛选器 URL | -                  |
| `--skip-sit`     | 跳过 SIT 测试     | false              |
| `--dry-run`      | 只分析不修复      | false              |
| `--auto-comment` | 自动添加评论      | true               |
| `--auto-status`  | 自动更新状态      | false (需手动确认) |

---

## 编排流程

```
输入: Coding filter URL (bug列表) 或 单个 bug ID
  │
  ├─ Step 1: 获取 Bug 列表
  │   ├─ 单 Bug: coding-bug-ops.read-detail + read-comments
  │   └─ 批量: coding-bug-ops.read-list → 逐个 read-detail + read-comments
  │
  ├─ Step 2: 遍历每个 Bug
  │   │
  │   ├─ 2.1 读取 Bug 完整上下文
  │   │   ├─ coding-bug-ops.read-detail   → 标题、描述、字段
  │   │   └─ coding-bug-ops.read-comments → 所有评论 (关键!)
  │   │
  │   ├─ 2.2 分析 Bug
  │   │   └─ yili-code-fix.analyze → 对比老新代码, 输出遗漏清单
  │   │
  │   ├─ 2.3 输出分析方案
  │   │   └─ 展示: 遗漏清单 + 前后端分类 + 修复计划
  │   │
  │   ├─ 2.4 ⏸️ 等待用户确认
  │   │   └─ 用户回复"确认"后继续
  │   │
  │   ├─ 2.5 执行修复/标注
  │   │   │
  │   │   ├─ [前端 Bug]
  │   │   │   ├─ coding-bug-ops.add-comment
  │   │   │   │   "【AI分析】前端问题, 对应老代码 xxx, 新框架不修改"
  │   │   │   ├─ coding-bug-ops.reassign → 从排期表查找前端负责人并转派
  │   │   │   │   (读取 fssc-schedule.xlsx "FSSC系统功能整体排期" sheet)
  │   │   │   └─ 跳到 Step 2.11 记录结果，继续下一个 Bug
  │   │   │
  │   │   └─ [后端 Bug]
  │   │       ├─ yili-code-fix.fix       → 修复代码
  │   │       └─ mvn compile             → 编译验证
  │   │
  │   ├─ 2.6 本地接口测试
  │   │   └─ local-api-test → 本地启动服务 → curl 登录 → curl 测试接口 → 验证响应
  │   │
  │   ├─ 2.7 ⏸️ 提交代码（人工确认）
  │   │   └─ git-commit-push → pull更新 → 冲突检测 → 展示diff → 用户确认 → push
  │   │
  │   ├─ 2.8 CI 构建发布
  │   │   └─ coding-ci-deploy → 触发对应模块 SIT 构建 → 等待完成 → 截图
  │   │
  │   ├─ 2.9 SIT 验证
  │   │   └─ sit-smoke-test   → SIT 做单验证 + API 数据验证
  │   │
  │   ├─ 2.10 验证结果分析与路由
  │   │   └─ sit-verify-analyze → 分析原因, 路由到:
  │   │       │
  │   │       ├─ [全部通过] → 修复成功闭环
  │   │       │   ├─ coding-bug-ops.add-comment (修复说明)
  │   │       │   ├─ coding-bug-ops.update-status → "待验证"
  │   │       │   └─ coding-bug-ops.reassign → 发起人
  │   │       │
  │   │       ├─ [API正确 + 页面错误] → 前端问题
  │   │       │   ├─ coding-bug-ops.add-comment (后端OK, 前端问题)
  │   │       │   ├─ coding-bug-ops.update-remark (备注)
  │   │       │   └─ coding-bug-ops.reassign → 前端处理人
  │   │       │
  │   │       ├─ [API错误] → 后端未修复
  │   │       │   ├─ coding-bug-ops.add-comment (未修复分析)
  │   │       │   └─ 回到 Step 2.2 重新分析修复
  │   │       │
  │   │       └─ [环境异常] → ⏸️ 等待人工排查
  │   │
  │   └─ 2.11 记录处理结果
  │
  └─ Step 3: 输出汇总报告
      ├─ 修复了哪些 Bug（后端）+ 修改文件列表
      ├─ 标注了哪些 Bug（前端）+ 老代码位置
      ├─ 转派了哪些 Bug（前端问题）+ 转派给谁
      ├─ 重新修复了哪些 Bug（后端未修复）
      ├─ Git 提交记录 + commit hash
      ├─ CI 构建结果 + 构建号
      ├─ SIT 测试结果 + 截图路径
      └─ 未处理的 Bug 及原因
```

---

## 详细步骤说明

### Step 1: 获取 Bug 列表

**单 Bug 模式**:

```
读取 coding-bug-ops SKILL.md
→ coding-bug-ops.read-detail(bug-id)
→ coding-bug-ops.read-comments(bug-id)
→ 组装完整 Bug 上下文
```

**批量模式**:

```
读取 coding-bug-ops SKILL.md
→ coding-bug-ops.read-list(filter-url)
→ 获取 Bug 列表 [{id, title, status, assignee}, ...]
→ 过滤: 只处理状态为"待处理"/"处理中"的 Bug
→ 对每个 Bug 执行 Step 2
```

### Step 2: 遍历处理每个 Bug

#### 2.1 读取完整上下文

```
coding-bug-ops.read-detail(bug-id) → 标题、描述、状态、标签
coding-bug-ops.read-comments(bug-id) → 所有评论
→ 合并为完整的 Bug 上下文文档
```

**重要**: 不能只看描述，评论中经常有关键信息!

#### 2.2 分析 Bug

```
读取 yili-code-fix SKILL.md
→ yili-code-fix.analyze(bug-context)
→ 输出: 遗漏清单 + 前后端分类
```

#### 2.3 输出分析方案

向用户展示:

```markdown
## Bug #{id}: {title}

### 分析结果
- 模板编号: T{XXX}
- 问题类型: 后端 / 前端 / 混合

### 遗漏清单
| 编号 | 位置 | 描述 | 类型 |
|------|------|------|------|
| 1 | ... | ... | 后端 |
| 2 | ... | ... | 前端 |

### 修复计划
- 后端: 修改 {文件}, 补充 {逻辑}
- 前端: 标注 "前端问题, 不修改"

请回复"确认"开始修复，或提出修改意见。
```

#### 2.4 等待用户确认

**强制规则**: 每个 Bug 修复前**必须等待用户确认**，不自动执行修复。

用户可以:

- 回复"确认" → 执行修复
- 回复"跳过" → 跳过此 Bug
- 提出修改意见 → 调整方案后重新确认

#### 2.5 执行修复/标注

**前端 Bug**: 添加评论 + 转派前端

```
coding-bug-ops.add-comment(bug-id, "【AI分析】前端问题...")
→ 从排期表查找前端负责人:
  1. 使用 xlsx skill 读取 ai-spec/skills/code/coding-bug-ops/references/fssc-schedule.xlsx
  2. 读取 "FSSC系统功能整体排期" sheet
  3. 用 Bug 模块关键词匹配，找到前端负责人
  4. 如果找不到，⏸️ 询问用户指定
coding-bug-ops.reassign(bug-id, --to <前端负责人>)
→ 跳过后续的修复/测试/提交步骤，直接记录结果
```

**后端 Bug**: 修复 + 编译 + 测试 + 评论

```
yili-code-fix.fix(bug-context)
→ mvn compile -pl <module> -am
→ [如果 --skip-sit 未设置] sit-smoke-test(T{XXX})
→ coding-bug-ops.add-comment(bug-id, "【AI修复】...")
→ [如果 --auto-status] coding-bug-ops.update-status(bug-id, "已修复")
```

**SIT 测试结果处理** (由 sit-verify-analyze 执行):


| 结果       | 判定条件            | 后续动作                                   |
| ---------- | ------------------- | ------------------------------------------ |
| 全部通过   | API 正确 + 页面正确 | 状态→待验证，转派→发起人                 |
| 前端问题   | API 正确 + 页面错误 | 评论+备注+转派→前端，继续下一个 Bug       |
| 后端未修复 | API 返回错误        | 评论+回到 Step 2.2 重新修复（最多重试1次） |
| 环境问题   | 接口异常/超时       | 评论+暂停等待人工                          |

### Step 3: 输出汇总报告

```markdown
## Bug 修复汇总报告

### 处理统计
- 总数: N 个 Bug
- 后端修复: X 个
- 前端标注: Y 个
- 前端转派: W 个
- 重新修复: V 个
- 跳过: Z 个

### 后端修复列表（已闭环）
| Bug ID | 标题 | 修改文件 | 编译 | SIT | 状态 | 转派 |
|--------|------|---------|------|-----|------|------|
| #4992 | xxx | SaveClaimServiceImpl.java | 通过 | 通过 | 待验证 | 发起人 |

### 前端转派列表
| Bug ID | 标题 | 前端问题说明 | 转派给 |
|--------|------|------------|--------|
| #4686 | 修改人不同步 | API正确，页面未展示 | 前端xxx |

### 前端标注列表（分析阶段识别）
| Bug ID | 标题 | 老代码位置 |
|--------|------|-----------|
| #4991 | yyy | WebRoot/.../T044.jsp L50 |

### 后端重新修复列表
| Bug ID | 标题 | 重试次数 | 结果 |
|--------|------|---------|------|
| #4990 | zzz | 1 | 二次修复通过 |

### SIT 测试结果
| Bug ID | 测试场景 | 结果 | 截图 |
|--------|---------|------|------|
| #4992 | T044 冒烟测试 | 通过 | sit-smoke-T044.png |

### 未处理
| Bug ID | 标题 | 原因 |
|--------|------|------|
| #4990 | zzz | 用户选择跳过 |
```

---

## 关键设计点

### 1. 确认机制

- 每个 Bug 修复前**必须**输出分析方案并等待用户确认
- 防止 AI 误修改代码
- 用户可以随时调整修复方案

### 2. 错误恢复

- SIT 测试失败不阻塞后续 Bug 处理
- 编译失败自动重试 3 次
- 浏览器操作失败有降级策略

### 3. 数据安全

- 不在生产环境执行任何操作
- 修改代码前可以通过 `--dry-run` 预览
- Bug 状态更新默认需要手动确认

### 4. 可追溯性

- 每个修复都有对应的老代码行号
- SIT 测试截图留存
- Coding 评论记录完整修复过程
- 汇总报告可作为交付物

---

## 强制约束

1. **用户确认**: 修复代码前必须等待用户确认，绝不自动修复
2. **评论完整**: 添加到 Coding 的评论必须包含老代码位置、修复说明
3. **编译验证**: 修复后必须编译通过
4. **截图存证**: SIT 测试必须截图
5. **不改生产**: 只在 SIT/UAT 环境测试
6. **评论必读**: 读取 Bug 时必须同时读评论
7. **分层遵守**: 修复代码遵守 agents.md 分层规范
8. **用户规则**: 遵守 user-rules.md 中"不修改代码、需要变更请重写"原则

## 参考

- 编排流程图: [references/pipeline-flow.md](references/pipeline-flow.md)
- Coding 操作: `ai-spec/skills/code/coding-bug-ops/SKILL.md`
- 代码修复: `ai-spec/skills/code/yili-code-fix/SKILL.md`
- 本地测试: `ai-spec/skills/code/local-api-test/SKILL.md`
- 代码提交: `ai-spec/skills/code/git-commit-push/SKILL.md`
- CI 发布: `ai-spec/skills/code/coding-ci-deploy/SKILL.md`
- SIT 测试: `ai-spec/skills/code/sit-smoke-test/SKILL.md`
- 验证分析: `ai-spec/skills/code/sit-verify-analyze/SKILL.md`
- 项目规范: `.qoder/rules/agents.md`
- 个人偏好: `.qoder/rules/user-rules.md`
