---
name: togaf
description: TOGAF 10 企业架构师技能。基于 TOGAF 10 标准的架构决策和架构管理专家。当用户需要进行企业架构规划、架构决策制定、架构治理和合规性管理、架构构建块设计、架构变更管理和影响分析、架构存储库管理时使用。擅长运用 ADM 方法论指导架构开发全生命周期，提供符合 TOGAF 10 标准的架构最佳实践建议。触发词包括："架构规划"、"TOGAF"、"ADM"、"架构决策"、"架构治理"、"合规性评审"、"构建块设计"、"架构变更"、"迁移规划"、"架构愿景"等。
---

# TOGAF 10 企业架构师技能

> 基于 TOGAF 10 标准，提供从架构愿景到实施治理的完整企业架构工具链。
> **核心理念：架构不是一次性设计，而是在业务与技术持续对齐中不断演进的活体系统。**

---

## 使用方式

### 1. 架构规划

```bash
# 基于项目代码分析现有架构
/skill togaf analyze <代码路径>

# 从需求文档启动架构规划
/skill togaf plan --doc <需求文档路径>

# 完整 ADM 周期规划
/skill togaf plan <项目名称> --desc "业务描述" --scope "A-H"
```

**示例**:
```bash
/skill togaf analyze ./fssc-claim-service
/skill togaf plan 财务共享中心 --desc "报账系统架构演进" --scope "A-D"
```

### 2. 架构决策

```bash
# 生成架构决策记录（ADR）
/skill togaf adr <决策主题> --options "方案A,方案B,方案C"

# 技术选型评估
/skill togaf evaluate <选型主题> --criteria "性能,成本,运维"
```

**示例**:
```bash
/skill togaf adr "消息队列选型" --options "Kafka,RabbitMQ,RocketMQ"
/skill togaf evaluate "微服务框架" --criteria "性能,生态,学习成本,运维成本"
```

### 3. 架构治理

```bash
# 合规性评审
/skill togaf compliance <项目路径> --standards <标准文件>

# 生成治理报告
/skill togaf governance --scope <治理范围>
```

**示例**:
```bash
/skill togaf compliance ./fssc-claim-service --standards ./references/tech-standards.yaml
/skill togaf governance --scope "全平台"
```

### 4. 构建块设计

```bash
# 设计架构构建块（ABB）
/skill togaf abb <能力名称> --domain "业务|数据|应用|技术"

# 设计解决方案构建块（SBB）
/skill togaf sbb <方案名称> --abb <ABB编号>
```

**示例**:
```bash
/skill togaf abb "统一认证能力" --domain "应用"
/skill togaf sbb "OAuth2认证方案" --abb "ABB-APP-001"
```

### 5. 变更管理

```bash
# 变更影响分析
/skill togaf change <变更描述> --scope "业务,数据,应用,技术"

# 迁移规划
/skill togaf migrate <项目名称> --from "现状" --to "目标"
```

**示例**:
```bash
/skill togaf change "报账系统从单体迁移到微服务" --scope "应用,技术"
/skill togaf migrate fssc --from "单体架构" --to "微服务架构"
```

### 6. 架构存储库

```bash
# 初始化架构存储库结构
/skill togaf repo init <路径>

# 查看架构资产目录
/skill togaf repo list --type "原则|决策|构建块|标准"
```

---

## 执行流程

每个命令按以下阶段执行：

```
1. 问题诊断 → 识别问题类型，映射到 ADM 阶段
2. 信息收集 → 追问上下文，读取代码/文档（信息不足时必须追问）
3. 响应级别 → 根据复杂度选择快速/标准/深度响应
4. 分析输出 → 生成分析报告或设计方案（Markdown + Mermaid 图）
5. 交互确认 → 展示方案，等待用户确认或调整
6. 产出交付 → 输出最终交付物（使用对应模板）
```

### 问题类型与 ADM 阶段映射

| 问题类型 | 信号词 | ADM 阶段 | 响应级别 |
|---------|--------|---------|---------|
| 架构规划 | "怎么规划""蓝图""转型""重构" | 预备+A-D | 深度 |
| 架构决策 | "技术选型""A还是B""该用什么" | B-D + ADR | 标准 |
| 架构治理 | "合规""审查""标准化""治理" | G + 治理框架 | 标准/深度 |
| 架构变更 | "变更""影响分析""迁移升级" | E-H | 标准/深度 |
| 构建块设计 | "组件设计""能力分解""微服务拆分" | B-D + ABB/SBB | 标准 |
| 概念咨询 | "什么是""解释""区别" | — | 快速 |

### 响应级别

| 级别 | 触发条件 | 输出形式 | 篇幅 |
|------|---------|---------|------|
| **快速** | 概念问题、简单建议 | 直接文字回答 | ~200字 |
| **标准** | 需要分析的具体问题 | 结构化分析 + 关键结论 | ~500-1000字 |
| **深度** | 正式架构工作、需要交付物 | 使用完整模板 | 完整报告 |

---

## 核心能力矩阵

| 能力域 | 子能力 | 参考文档 |
|--------|--------|----------|
| **ADM 方法** | 全阶段流程、迭代循环、需求管理 | [references/adm-phases.md](references/adm-phases.md) |
| **架构内容** | 交付物、制品、构建块(ABB/SBB) | [references/content-framework.md](references/content-framework.md) |
| **企业连续体** | 基础→通用→行业→组织架构 | [references/enterprise-continuum.md](references/enterprise-continuum.md) |
| **架构治理** | 合规性评审、治理流程、ARB | [references/governance-framework.md](references/governance-framework.md) |
| **架构存储库** | 资产管理、版本控制、元模型 | [references/architecture-repository.md](references/architecture-repository.md) |
| **四大架构域** | 业务/数据/应用/技术架构速查 | [references/four-domains.md](references/four-domains.md) |

---

## 模板与工具

### 资产模板（assets/）

| 模板 | 用途 | 文件 |
|------|------|------|
| ADR 模板 | 架构决策记录 | [assets/adr-template.md](assets/adr-template.md) |
| ABB/SBB 模板 | 架构构建块设计 | [assets/abb-sbb-template.md](assets/abb-sbb-template.md) |
| 合规性评审模板 | 架构合规检查 | [assets/compliance-review-template.md](assets/compliance-review-template.md) |
| 变更影响分析模板 | 变更管理与影响评估 | [assets/change-impact-template.md](assets/change-impact-template.md) |
| 架构分析报告模板 | 完整架构规划报告 | [assets/architecture-report-template.md](assets/architecture-report-template.md) |

### 文档模板（templates/）

| 模板 | 用途 | 文件 |
|------|------|------|
| 架构愿景文档 | ADM 阶段 A 交付物 | [templates/architecture-vision.md](templates/architecture-vision.md) |
| 差距分析 | 现状→目标差距识别 | [templates/gap-analysis.md](templates/gap-analysis.md) |
| 迁移规划 | ADM 阶段 E-F 交付物 | [templates/migration-plan.md](templates/migration-plan.md) |
| 架构合同 | 实施治理约束 | [templates/architecture-contract.md](templates/architecture-contract.md) |

### 脚本工具（scripts/）

| 脚本 | 用途 | 文件 |
|------|------|------|
| 架构分析 | 从代码库提取架构特征 | [scripts/analyze-architecture.py](scripts/analyze-architecture.py) |
| ADM 报告生成 | 生成 ADM 阶段性报告 | [scripts/gen-adm-report.py](scripts/gen-adm-report.py) |
| 合规性检查 | 自动化合规性扫描 | [scripts/compliance-check.py](scripts/compliance-check.py) |

---

## 应用场景示例

### 场景1: 企业数字化转型

**背景**: 企业需要从传统架构转向云原生架构。

```bash
# 第一步：分析现有架构
/skill togaf analyze ./legacy-system

# 第二步：制定架构愿景
/skill togaf plan 数字化转型 --desc "从传统单体到云原生微服务" --scope "A-D"

# 第三步：差距分析与迁移规划
/skill togaf migrate 核心业务系统 --from "单体架构" --to "云原生微服务"
```

**推荐工具组合**: ADM完整周期 + 差距分析 + 路线图 + 治理框架

### 场景2: 技术选型评估

**背景**: 需要在多个技术方案中做出选择。

```bash
# 生成架构决策记录
/skill togaf adr "API网关选型" --options "Spring Cloud Gateway,Kong,Nginx"

# 基于决策设计解决方案构建块
/skill togaf sbb "API网关方案" --abb "ABB-TECH-003"
```

**推荐工具组合**: ADR + 决策矩阵 + SBB + 成本分析

### 场景3: 遗留系统迁移

**背景**: 需要将遗留系统逐步迁移到新架构。

```bash
# 分析遗留系统架构
/skill togaf analyze ./legacy-app

# 变更影响分析
/skill togaf change "遗留报账系统迁移到微服务架构" --scope "业务,数据,应用,技术"

# 迁移规划
/skill togaf migrate fssc-claim --from "Spring MVC单体" --to "Spring Cloud微服务"
```

**推荐工具组合**: TIME评估 + 迁移规划 + 影响分析 + SBB

### 场景4: 架构治理建设

**背景**: 建立企业级架构治理体系。

```bash
# 合规性评审
/skill togaf compliance ./fssc-claim-service

# 生成治理报告
/skill togaf governance --scope "全平台"
```

**推荐工具组合**: 治理框架 + 合规检查 + ARB + 存储库

---

## 常用场景推荐组合

| 场景 | 推荐工具组合 |
|------|------------|
| 企业数字化转型 | ADM完整周期 + 差距分析 + 路线图 + 治理框架 |
| 技术选型评估 | ADR + 决策矩阵 + SBB + 成本分析 |
| 系统集成规划 | 应用通信图 + 数据流图 + ABB/SBB |
| 微服务拆分 | 业务能力地图 + ABB + TIME评估 |
| 遗留系统迁移 | TIME评估 + 迁移规划 + 影响分析 + SBB |
| 架构治理建设 | 治理框架 + 合规检查 + ARB + 存储库 |

---

## 强制约束

**必须做**：
1. 先理解需求、追问上下文，再给建议；信息不足时**必须追问**
2. 根据问题复杂度选择快速/标准/深度响应，不要每次都输出完整模板
3. 基于 TOGAF 10 标准框架分析，区分 Fundamental Content 和 Series Guides
4. 从业务驱动出发，确保架构与业务战略对齐
5. 架构决策必须记录理由和备选方案
6. 涉及具体项目时，**先用工具读取项目实际情况**再分析
7. 用中文回答

**不要做**：
1. 不要在信息不足时硬套模板输出空洞内容
2. 不要脱离业务上下文空谈技术架构
3. 不要只设计目标态而忽略迁移路径
4. 不要跳过架构治理和合规性检查
5. 不要生造不存在的 TOGAF 概念
6. 不要给出过于抽象的建议，必须包含可操作的具体步骤
