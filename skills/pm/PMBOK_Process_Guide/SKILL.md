---
name: pmbok-process-guide
description: 基于《PMBOK 指南》(第7版) 的项目管理标准过程查询与模板生成技能。提供项目管理五大过程组、十大知识领域的标准流程查询，以及 WBS、风险登记册、干系人登记册等核心文档模板的自动生成。当用户需要项目管理过程指导、项目文档模板、过程裁剪建议、项目管理最佳实践时使用。触发词包括："项目管理"、"PMBOK"、"WBS"、"风险登记册"、"干系人分析"、"过程组"、"知识领域"、"项目章程"、"变更控制"、"挣值分析"。
---

# PMBOK 项目管理过程指南

> 基于《PMBOK 指南》(第7版)，提供从启动到收尾的全生命周期项目管理标准过程与模板。
> **核心理念：项目管理是将知识、技能、工具与技术应用于项目活动，以满足项目要求的过程。**

---

## 使用方式

### 1. 过程查询

```bash
# 查询某个过程组的所有过程
/skill pmbok-process-guide query --group <过程组>

# 查询某个知识领域的所有过程
/skill pmbok-process-guide query --area <知识领域>

# 查询特定过程的 ITTO（输入/工具与技术/输出）
/skill pmbok-process-guide itto <过程名称>
```

**示例**:
```bash
/skill pmbok-process-guide query --group "规划"
/skill pmbok-process-guide query --area "风险管理"
/skill pmbok-process-guide itto "识别风险"
```

### 2. 模板生成

```bash
# 生成项目管理文档模板
/skill pmbok-process-guide template <模板类型>

# 批量生成某过程组所需的全部模板
/skill pmbok-process-guide template --group <过程组>

# 生成裁剪后的模板（适配项目规模）
/skill pmbok-process-guide template <模板类型> --scale <大型|中型|小型>
```

**示例**:
```bash
/skill pmbok-process-guide template wbs
/skill pmbok-process-guide template risk-register --scale 中型
/skill pmbok-process-guide template --group "启动"
```

### 3. 过程裁剪

```bash
# 根据项目特征推荐过程裁剪方案
/skill pmbok-process-guide tailor --type <项目类型> --scale <规模> --method <瀑布|敏捷|混合>
```

**示例**:
```bash
/skill pmbok-process-guide tailor --type "IT系统开发" --scale 中型 --method 混合
```

### 4. 过程映射

```bash
# 将业务活动映射到 PMBOK 过程
/skill pmbok-process-guide map --activity <业务活动描述>

# 生成过程间的数据流关系图
/skill pmbok-process-guide dataflow --area <知识领域>
```

**示例**:
```bash
/skill pmbok-process-guide map --activity "我们需要评估项目的可行性并获得管理层批准"
/skill pmbok-process-guide dataflow --area "范围管理"
```

### 参数说明

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| 命令 | ✅ | query / template / tailor / map / itto / dataflow | `query` |
| --group | ❌ | 过程组名称 | `"启动"`, `"规划"`, `"执行"`, `"监控"`, `"收尾"` |
| --area | ❌ | 知识领域名称 | `"范围管理"`, `"风险管理"`, `"进度管理"` |
| --scale | ❌ | 项目规模 | `"大型"`, `"中型"`, `"小型"` |
| --type | ❌ | 项目类型 | `"IT系统开发"`, `"基建工程"`, `"产品研发"` |
| --method | ❌ | 开发方法 | `"瀑布"`, `"敏捷"`, `"混合"` |

---

## 核心知识框架

### 五大过程组

| 过程组 | 核心目的 | 关键过程 |
|--------|----------|----------|
| **启动** | 定义新项目或新阶段，获得授权 | 制定项目章程、识别干系人 |
| **规划** | 确定项目范围，细化目标，制定行动方案 | 制定项目管理计划、WBS、进度、成本、风险等 |
| **执行** | 完成项目管理计划中确定的工作 | 指导与管理项目工作、管理质量 |
| **监控** | 跟踪、审查和调节项目进展与绩效 | 监控项目工作、实施整体变更控制 |
| **收尾** | 完成所有活动，正式关闭项目或阶段 | 结束项目或阶段 |

### 十大知识领域

| 知识领域 | 核心关注点 | 关键工具与技术 |
|----------|-----------|---------------|
| **整合管理** | 统筹协调各要素 | 变更控制、配置管理、项目管理信息系统 |
| **范围管理** | 做且只做所需工作 | WBS、需求跟踪矩阵、范围基准 |
| **进度管理** | 按时完成项目 | 关键路径法(CPM)、甘特图、资源优化 |
| **成本管理** | 在批准预算内完成 | 挣值分析(EVM)、估算技术、储备分析 |
| **质量管理** | 满足项目要求 | 质量审计、统计抽样、控制图 |
| **资源管理** | 有效利用项目资源 | 资源日历、RACI矩阵、团队建设 |
| **沟通管理** | 确保信息及时传递 | 沟通模型、沟通管理计划、报告 |
| **风险管理** | 管理不确定性 | 风险登记册、概率影响矩阵、蒙特卡洛模拟 |
| **采购管理** | 获取外部资源 | 合同类型、招投标、供应商评估 |
| **干系人管理** | 管理干系人期望 | 权力利益方格、干系人参与度评估矩阵 |

---

## 执行流程

每个命令按以下阶段执行：

```
1. 需求识别 → 解析用户查询意图，匹配过程组/知识领域
2. 上下文收集 → 了解项目背景、规模、方法论（信息不足时追问）
3. 过程映射 → 将需求映射到 PMBOK 标准过程
4. 内容生成 → 根据匹配结果生成过程说明/模板/建议
5. 裁剪适配 → 根据项目特征裁剪输出内容
6. 交付输出 → 输出结构化的过程指导或文档模板
```

### 响应级别

| 级别 | 触发条件 | 输出形式 | 篇幅 |
|------|---------|---------|------|
| **快速** | 概念查询、单一过程ITTO | 表格 + 简要说明 | ~200字 |
| **标准** | 知识领域查询、单个模板生成 | 结构化分析 + 模板 | ~500-1000字 |
| **深度** | 完整过程裁剪、数据流分析 | 完整报告 + 多个模板 | 完整报告 |

---

## 模板与工具

### 模板库（templates/）

| 模板 | 用途 | 文件 |
|------|------|------|
| 项目章程 | 启动阶段-正式授权项目 | [templates/project-charter.md](templates/project-charter.md) |
| WBS 工作分解结构 | 规划阶段-范围分解 | [templates/wbs.md](templates/wbs.md) |
| 风险登记册 | 规划阶段-风险记录与跟踪 | [templates/risk-register.md](templates/risk-register.md) |
| 干系人登记册 | 启动阶段-干系人识别与分析 | [templates/stakeholder-register.md](templates/stakeholder-register.md) |
| 变更请求表 | 监控阶段-变更控制 | [templates/change-request.md](templates/change-request.md) |
| 经验教训登记册 | 收尾阶段-知识转移 | [templates/lessons-learned.md](templates/lessons-learned.md) |
| RACI 矩阵 | 规划阶段-责任分配 | [templates/raci-matrix.md](templates/raci-matrix.md) |
| 沟通管理计划 | 规划阶段-沟通规划 | [templates/communication-plan.md](templates/communication-plan.md) |

### 脚本工具（scripts/）

| 脚本 | 用途 | 文件 |
|------|------|------|
| 过程映射引擎 | 将活动映射到PMBOK过程 | [scripts/process-mapper.md](scripts/process-mapper.md) |
| ITTO 速查 | 输入/工具与技术/输出快速检索 | [scripts/itto-lookup.md](scripts/itto-lookup.md) |
| 过程裁剪顾问 | 根据项目特征推荐过程裁剪 | [scripts/tailor-advisor.md](scripts/tailor-advisor.md) |

---

## 应用场景示例

### 场景1：新项目启动

**背景**: 团队要启动一个新的IT系统开发项目，需要标准化的启动文档。

```bash
# 生成项目章程模板
/skill pmbok-process-guide template project-charter

# 生成干系人登记册模板
/skill pmbok-process-guide template stakeholder-register

# 查看启动过程组的完整流程
/skill pmbok-process-guide query --group "启动"
```

### 场景2：风险管理规划

**背景**: 项目进入规划阶段，需要建立风险管理体系。

```bash
# 查看风险管理知识领域的所有过程
/skill pmbok-process-guide query --area "风险管理"

# 生成风险登记册模板
/skill pmbok-process-guide template risk-register --scale 中型

# 查看"识别风险"过程的 ITTO
/skill pmbok-process-guide itto "识别风险"
```

### 场景3：敏捷项目过程裁剪

**背景**: 敏捷项目需要裁剪传统PMBOK过程以适配迭代开发。

```bash
# 获取裁剪建议
/skill pmbok-process-guide tailor --type "产品研发" --scale 小型 --method 敏捷
```

---

## 强制约束

**必须做**：
1. 基于 PMBOK 标准框架回答，确保术语和过程定义准确
2. 根据项目规模和方法论裁剪建议，不要一刀切
3. 模板生成时包含使用说明和填写指引
4. 信息不足时**必须追问**项目背景和上下文
5. 用中文回答，专业术语附英文原文

**不要做**：
1. 不要生造不存在的 PMBOK 过程或知识领域
2. 不要忽略项目规模差异，小项目不需要大型项目的全部过程
3. 不要只给空模板不给填写指导
4. 不要混淆 PMBOK 第6版和第7版的概念差异
5. 不要脱离实际项目场景空谈理论
