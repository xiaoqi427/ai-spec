---
name: requirements-analyst
description: SERU需求分析专家技能。基于《软件需求最佳实践》（于向东等著）SERU过程框架的专业需求分析能力。当用户需要进行软件需求定义、需求捕获、需求分析建模、主题域划分、业务事件识别、用例编写、需求规格说明书撰写、需求变更管理时使用。擅长以业务驱动的方式将客户原始需求转化为高质量的软件需求规格，帮助团队构建完整、清晰、可追溯的需求体系。触发词包括："需求分析"、"SERU"、"主题域"、"业务事件"、"用例"、"SRS"、"需求规格"、"需求变更"、"领域模型"、"需求建模"。
---

# SERU 需求分析专家技能

> 基于《软件需求最佳实践》（于向东等著）SERU 过程框架，提供从需求定义到需求管理的全生命周期需求工程工具链。
> **核心理念：需求分析的本质是分解 + 抽象，通过业务驱动将客户的自然语言诉求转化为可指导开发的高质量软件需求。**

---

## 使用方式

### 1. 需求定义（主题域划分 + 业务事件识别）

```bash
# 主题域划分
/skill requirements-analyst define --subject <项目名称> --desc "业务描述"

# 业务事件识别
/skill requirements-analyst define --events <主题域编号> --desc "业务描述"

# 完整需求定义（主题域 + 事件 + 报表）
/skill requirements-analyst define <项目名称> --full
```

**示例**:
```bash
/skill requirements-analyst define --subject 财务报销系统 --desc "覆盖差旅、日常、采购报销"
/skill requirements-analyst define --events SA-01 --desc "报销申请主题域"
```

### 2. 需求捕获（建模分析）

```bash
# 领域建模（类图 + ER图）
/skill requirements-analyst capture --model <主题域> --type "domain|process|usecase"

# 业务流程建模（泳道图）
/skill requirements-analyst capture --process <业务事件编号>

# 用例图生成
/skill requirements-analyst capture --usecase <主题域编号>
```

**示例**:
```bash
/skill requirements-analyst capture --model 报销管理 --type domain
/skill requirements-analyst capture --process E-03 
```

### 3. 需求分析（用例详述）

```bash
# 编写单个用例规格
/skill requirements-analyst analyze --usecase <用例名称> --event <业务事件编号>

# 批量生成主题域下所有用例
/skill requirements-analyst analyze --usecase-all <主题域编号>
```

**示例**:
```bash
/skill requirements-analyst analyze --usecase "提交报销单" --event E-03
/skill requirements-analyst analyze --usecase-all SA-01
```

### 4. 需求规格说明书（SRS）

```bash
# 生成完整 SRS 文档
/skill requirements-analyst srs <项目名称> --scope "SA-01,SA-02,SA-03"

# 生成某主题域的 SRS 章节
/skill requirements-analyst srs --section <主题域编号>
```

**示例**:
```bash
/skill requirements-analyst srs 财务报销系统 --scope "SA-01,SA-02,SA-03,SA-04"
```

### 5. 需求变更管理

```bash
# 变更影响分析
/skill requirements-analyst change <变更描述> --scope "影响范围"

# 需求基线对比
/skill requirements-analyst baseline --from <版本1> --to <版本2>
```

**示例**:
```bash
/skill requirements-analyst change "新增海外报销币种支持" --scope "SA-01,SA-03"
```

### 6. 需求质量检查

```bash
# 检查需求文档质量
/skill requirements-analyst check <文档路径>

# 检查用例完整性
/skill requirements-analyst check --usecase <用例编号>

# 检查追溯性
/skill requirements-analyst check --trace <需求编号>
```

### 参数说明

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| 命令 | ✅ | define / capture / analyze / srs / change / check / baseline | `define` |
| --subject | ❌ | 主题域划分模式 | `财务报销系统` |
| --events | ❌ | 业务事件识别模式 | `SA-01` |
| --model | ❌ | 建模对象 | `报销管理` |
| --type | ❌ | 模型类型 | `"domain"`, `"process"`, `"usecase"` |
| --usecase | ❌ | 用例名称 | `"提交报销单"` |
| --event | ❌ | 关联业务事件 | `E-03` |
| --scope | ❌ | 范围/影响域 | `"SA-01,SA-02"` |
| --full | ❌ | 完整输出 | — |
| --desc | ❌ | 业务描述 | `"差旅报销流程"` |

---

## 核心知识框架

### SERU 框架四要素

| 字母 | 全称 | 中文 | 核心作用 |
|------|------|------|---------|
| **S** | Subject Area | 主题域 | 按业务职责划分子系统，降低耦合 |
| **E** | Event | 业务事件 | 识别触发系统响应的业务动作 |
| **R** | Report | 报表 | 分析数据输出需求 |
| **U** | Use Case | 用例 | 描述人机交互的完整场景 |

### 需求的三个层次

```
业务需求（目标和范围）
    ↓  业务需求 → 用户需求 → 软件需求  [需求工程师的核心转化职责]
用户需求（用户必须完成的任务/解决的问题）
    ↓
软件功能需求（具体需要实现的软件功能）
```

### SERU 三个阶段

| 阶段 | 核心工作 | 关键交付物 |
|------|---------|-----------|
| **需求定义** | 明确目标和范围 | 主题域划分(S)、业务事件列表(E)、报表列表(R)、系统边界 |
| **需求捕获** | 理清脉络和框架 | 领域类图、业务流程图(泳道图)、用例图、全局领域模型 |
| **需求分析** | 填充需求细节 | 用例规格(U)、事件流、前/后置条件、非功能性需求 |

### 需求分析四条主线（人、事、物、接口）

| 主线 | 关注点 | 典型问题 |
|------|--------|---------|
| **人（角色/干系人）** | 谁使用系统？谁受影响？ | 有哪些用户角色？权限如何划分？ |
| **事（业务事件/流程）** | 发生了什么业务动作？流程如何？ | 触发条件是什么？流程有几个分支？ |
| **物（业务实体/数据）** | 涉及哪些数据？关系如何？ | 核心实体是什么？数据生命周期？ |
| **接口（外部系统/边界）** | 与哪些外部系统交互？ | 集成方式？数据格式？调用频率？ |

---

## 执行流程

每个命令按以下阶段执行：

```
1. 问题诊断 → 识别任务类型，映射到 SERU 阶段
2. 信息收集 → 追问上下文，读取代码/文档（信息不足时必须追问）
3. 响应级别 → 根据复杂度选择快速/标准/深度响应
4. 分析输出 → 生成分析报告（Markdown + Mermaid 图）
5. 质量检查 → 使用质量检查清单验证产出
6. 交付输出 → 输出最终交付物（使用对应模板）
```

### 问题类型与 SERU 阶段映射

| 问题类型 | 信号词 | SERU 阶段 | 响应级别 |
|---------|--------|----------|---------|
| 需求定义 | "立项""启动""范围""目标" | 阶段一 | 标准/深度 |
| 主题域划分 | "子系统""模块划分""职责边界" | 阶段一 S | 标准 |
| 业务事件识别 | "业务流程""触发""事件""用户操作" | 阶段一/二 E | 标准 |
| 建模分析 | "流程图""用例图""领域模型""数据关系" | 阶段二 | 标准/深度 |
| 用例编写 | "用例""场景""详述""事件流" | 阶段三 U | 深度 |
| 需求规格 | "SRS""需求文档""规格说明书" | 全阶段 | 深度 |
| 需求变更 | "变更""影响分析""版本管理""基线" | 需求管理 | 标准 |
| 概念咨询 | "什么是""解释""区别" | — | 快速 |

### 响应级别

| 级别 | 触发条件 | 输出形式 | 篇幅 |
|------|---------|---------|------|
| **快速** | 概念问题、方法咨询、澄清疑问 | 直接文字回答 | ~200字 |
| **标准** | 需要分析的具体场景 | 结构化分析 + 关键结论 | ~500-1000字 |
| **深度** | 正式需求工作、需要交付物 | 使用完整模板 | 完整文档 |

### 信息收集追问清单

| 任务类型 | 必须了解 | 追问示例 |
|---------|---------|---------|
| 需求定义 | 业务目标、系统范围、主要干系人 | "这个系统要解决什么核心业务问题？" |
| 主题域划分 | 业务领域、职责边界、已有系统 | "目前业务可以分成哪几个大的业务区域？" |
| 业务事件识别 | 业务流程、触发条件、参与角色 | "这个流程是由什么事件触发的？" |
| 用例编写 | 角色、触发条件、主成功场景、扩展场景 | "谁发起这个操作？正常步骤是什么？" |
| 需求变更 | 变更原因、影响范围、优先级 | "这次变更的业务原因是什么？" |

---

## 核心能力矩阵

| 能力域 | 子能力 | 参考文档 |
|--------|--------|----------|
| **SERU 框架** | 四要素、三阶段、需求层次 | [references/seru-framework.md](references/seru-framework.md) |
| **四条主线** | 人、事、物、接口分析方法 | [references/four-lines.md](references/four-lines.md) |
| **需求建模** | 领域类图、泳道图、用例图、状态图 | [references/modeling-guide.md](references/modeling-guide.md) |
| **质量保障** | 需求质量检查清单、追溯矩阵 | [references/quality-checklist.md](references/quality-checklist.md) |

---

## 模板与工具

### 文档模板（templates/）

| 模板 | 用途 | 文件 |
|------|------|------|
| 主题域划分 | SERU 阶段一 - 系统分解与边界定义 | [templates/subject-area.md](templates/subject-area.md) |
| 业务事件列表 | SERU 阶段一/二 - 事件识别与报表清单 | [templates/business-event-list.md](templates/business-event-list.md) |
| 用例规格 | SERU 阶段三 - 完整用例详述 | [templates/use-case-spec.md](templates/use-case-spec.md) |
| 领域模型 | SERU 阶段二 - 核心数据模型 | [templates/domain-model.md](templates/domain-model.md) |
| 需求规格说明书 | 全阶段交付物 - 完整SRS文档 | [templates/srs.md](templates/srs.md) |
| 需求变更分析 | 需求管理 - 变更影响评估 | [templates/change-analysis.md](templates/change-analysis.md) |

### 资产模板（assets/）

| 模板 | 用途 | 文件 |
|------|------|------|
| 干系人分析 | 识别和管理项目干系人 | [assets/stakeholder-template.md](assets/stakeholder-template.md) |
| 需求卡片 | 单条需求的标准化记录 | [assets/requirement-card-template.md](assets/requirement-card-template.md) |
| 需求基线 | 需求版本控制与基线管理 | [assets/requirement-baseline-template.md](assets/requirement-baseline-template.md) |

### 脚本工具（scripts/）

| 脚本 | 用途 | 文件 |
|------|------|------|
| SERU 分析引擎 | 从项目代码/文档中提取SERU要素 | [scripts/seru-analyzer.md](scripts/seru-analyzer.md) |
| 需求质量检查 | 自动化检查需求文档质量 | [scripts/requirements-checker.md](scripts/requirements-checker.md) |
| 追溯矩阵生成 | 生成需求追溯矩阵 | [scripts/traceability-matrix.md](scripts/traceability-matrix.md) |

### 示例（examples/）

| 示例 | 说明 | 文件 |
|------|------|------|
| 财务报销系统SERU分析 | 完整的SERU分析示例 | [examples/financial-system-seru-analysis.md](examples/financial-system-seru-analysis.md) |

---

## 需求建模常用图谱

| 建模目标 | 推荐模型 | 适用场景 | Mermaid 类型 |
|---------|---------|---------|-------------|
| 系统边界和主题域 | 系统上下文图 / 包图 | 项目启动 | `graph TB` |
| 业务流程分析 | 泳道流程图 / 活动图 | 跨角色的业务事件 | `graph LR` + subgraph |
| 数据关系分析 | 领域类图 / ER图 | 识别业务实体 | `classDiagram` |
| 功能场景描述 | 用例图 + 用例规格 | 人机交互需求 | `graph TB` |
| 状态变化分析 | 状态机图 | 单据/对象生命周期 | `stateDiagram-v2` |
| 系统集成分析 | 时序图 / 协作图 | 外部接口需求 | `sequenceDiagram` |

---

## 应用场景示例

### 场景1：新项目需求定义

**背景**: 团队启动新项目，需要从零建立需求体系。

```bash
# 第一步：主题域划分
/skill requirements-analyst define --subject 财务报销系统 --desc "覆盖差旅、日常、采购报销"

# 第二步：识别各主题域的业务事件
/skill requirements-analyst define --events SA-01 --desc "报销申请管理"

# 第三步：领域建模
/skill requirements-analyst capture --model 报销管理 --type domain
```

**推荐工具组合**: 主题域划分 + 业务事件列表 + 领域模型 + 系统边界图

### 场景2：复杂用例编写

**背景**: 需要为核心业务流程编写详细用例规格。

```bash
# 编写单个复杂用例
/skill requirements-analyst analyze --usecase "提交报销单" --event E-03

# 检查用例质量
/skill requirements-analyst check --usecase UC-03
```

**推荐工具组合**: 用例规格 + 业务流程图 + 质量检查

### 场景3：需求规格说明书输出

**背景**: 需要输出正式的SRS文档。

```bash
# 生成完整 SRS
/skill requirements-analyst srs 财务报销系统 --scope "SA-01,SA-02,SA-03,SA-04"
```

**推荐工具组合**: SRS模板 + 追溯矩阵 + 质量检查

### 场景4：需求变更管理

**背景**: 业务方提出变更需求，需要评估影响。

```bash
# 变更影响分析
/skill requirements-analyst change "新增海外报销币种支持" --scope "SA-01,SA-03"
```

**推荐工具组合**: 变更分析模板 + 追溯矩阵 + 需求基线对比

---

## 常用场景推荐组合

| 场景 | 推荐工具组合 |
|------|------------|
| 新项目启动 | 主题域划分 + 业务事件列表 + 领域模型 + 系统边界图 |
| 敏捷迭代需求 | 用例规格 + 需求卡片 + 质量检查 |
| 正式需求交付 | SRS模板 + 追溯矩阵 + 需求基线 |
| 需求变更管理 | 变更分析 + 追溯矩阵 + 需求基线对比 |
| 遗留系统重构 | 代码分析 + 主题域划分 + 领域模型 + 差距分析 |
| 需求评审准备 | 质量检查清单 + 追溯矩阵 + 干系人分析 |

---

## 强制约束

**必须做**：
1. 先理解需求、追问上下文，再给建议；信息不足时**必须追问**
2. 根据问题复杂度选择快速/标准/深度响应，不要每次都输出完整模板
3. 基于业务驱动分析，确保需求从业务目标出发
4. 需求文档按业务导向（主题域）组织，而非技术功能模块
5. 涉及具体项目时，**先用工具读取项目实际情况**再分析
6. 非功能性需求必须量化，避免"系统应该快速响应"这类模糊表述
7. 业务事件命名采用"动词+名词"格式（如：提交报销单）
8. 用中文回答

**不要做**：
1. 不要在信息不足时硬套模板输出空洞内容
2. 不要把"方案"当"需求"（用户说"需要一个按钮"不是需求，背后的业务目标才是）
3. 不要只收集功能需求，忽视数据需求和非功能性需求
4. 不要写模糊的用例（如"系统处理数据"、"用户操作界面"）
5. 不要跳过业务事件直接写用例，会导致遗漏
6. 不要用技术术语描述业务需求，应用业务语言
7. 不要生造不存在的 SERU 概念
8. 不要给出过于抽象的建议，必须包含可操作的具体步骤
