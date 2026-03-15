---
name: finmind
description: >
  FinMind 智投系统 — 金融交易全链路分析技能。模拟顶级交易团队的分工协作，采用"三层递进+四智体协同"架构，
  从数据感知→深度研究→决策执行形成完整闭环。融合段永平、查理芒格、瑞·达利欧、张磊、利弗莫尔等投资大师智慧，
  提供价值投资和趋势交易两套分析框架。支持个股深度分析、组合风控、研报生成等功能。
  触发词："分析股票"、"投资分析"、"财务分析"、"趋势分析"、"估值"、"风控"、"智投"、"finmind"。
---

# FinMind 智投系统

> **"投资是认知的变现，系统是纪律的保障。"**
>
> 融合10+本经典投资著作的智慧，构建从数据感知到交易决策的全链路分析系统。

---

## 系统概览

FinMind 不是工具的堆砌，而是模拟一支**顶级交易团队**的分工协作系统：

- **三层架构**: 数据层(感知) → 研究层(分析) → 决策层(执行)
- **四智体协同**: 观察者 → 分析师 → 策略师 → 执行者
- **两套框架**: 价值投资(长线) + 趋势交易(波段)
- **知识底座**: 10+本经典著作的核心思想提炼

### 知识来源

| 编号 | 知识源 | 核心价值 |
|------|--------|---------|
| 1 | 《数据交易：数据解析精要》 | 数据质量评估与标准化方法论 |
| 2 | 《大道》段永平 | 买股票=买公司、三不原则、本分文化 |
| 3 | 康波周期理论 | 50-60年长波周期、资产配置节奏 |
| 4 | 《原则》瑞·达利欧 | 极度透明、系统化决策、全天候策略 |
| 5 | 《从财务分析到经营分析》 | 从数字到业务本质 |
| 6 | 《财务报表分析与股票估值》 | 三表分析、估值模型、安全边际 |
| 7 | 人性的弱点(行为金融学) | 26种认知偏差、反人性交易纪律 |
| 8 | 《价值》张磊 | 长期主义、研究驱动、时间的朋友 |
| 9 | 《股票作手回忆录》利弗莫尔 | 关键位理论、趋势交易、止损纪律 |
| 10 | 《查理芒格》 | 多元思维模型、能力圈、检查清单 |
| 11 | 游子/柚子实战体系 | 强势龙头选股、量价择时、仓位管理 |

---

## 使用方式

### 1. 完整分析（全链路）

```bash
# 用价值投资框架深度分析
/skill finmind analyze <标的代码> --framework value

# 用趋势交易框架分析
/skill finmind analyze <标的代码> --framework trend

# 双框架交叉验证（推荐）
/skill finmind analyze <标的代码> --framework both

# 指定市场
/skill finmind analyze 600519 --framework value --market A
/skill finmind analyze AAPL --framework both --market US
```

**示例**:
```bash
/skill finmind analyze 600519 --framework value
# → 自动执行：行情获取 → 财报解析 → 因子评分 → 估值分析 → 风控检查 → 输出价值评分卡

/skill finmind analyze 比亚迪 --framework both
# → 双框架分析，输出价值评分卡 + 趋势信号卡 + 综合建议
```

### 2. 单技能调用

```bash
# 数据层
/skill finmind fetch <标的代码>                    # 获取行情数据
/skill finmind parse-financials <标的代码>          # 解析财报
/skill finmind collect-news <关键词>               # 采集新闻/舆情

# 研究层
/skill finmind sentiment <标的代码/关键词>          # 情绪分析
/skill finmind score <标的代码>                    # 多因子评分
/skill finmind event-impact <事件描述>              # 事件冲击分析
/skill finmind pattern <标的代码>                   # 技术形态识别
/skill finmind cycle                               # 康波周期当前定位

# 决策层
/skill finmind risk-check <组合描述>               # 风控检查
/skill finmind suggest <标的代码>                   # 组合建议
/skill finmind report <标的代码> --type deep        # 深度研报
/skill finmind report <标的代码> --type brief       # 快速简报
```

### 3. 智能体模式（对话式交互）

```bash
/skill finmind agent observer       # 启动观察者 — 市场监控模式
/skill finmind agent analyst        # 启动分析师 — 深度研究模式
/skill finmind agent strategist     # 启动策略师 — 决策建议模式
/skill finmind agent executor       # 启动执行者 — 风控+报告模式
```

### 4. 知识查询

```bash
/skill finmind wisdom munger        # 查询芒格思维模型
/skill finmind wisdom duan          # 查询段永平投资哲学
/skill finmind wisdom dalio         # 查询达利欧原则
/skill finmind wisdom livermore     # 查询利弗莫尔交易智慧
/skill finmind checklist bias       # 认知偏差自查
/skill finmind checklist munger     # 芒格检查清单
```

### 参数说明

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| 命令 | 是 | analyze/fetch/score/report/agent/wisdom 等 | `analyze` |
| 标的代码 | 视命令 | 股票代码或名称 | `600519`, `AAPL`, `比亚迪` |
| --framework | 否 | 分析框架选择 | `value`, `trend`, `both` |
| --market | 否 | 市场 | `A`(A股), `US`(美股), `HK`(港股) |
| --type | 否 | 报告类型 | `deep`, `brief`, `review` |

---

## 数据来源（路径A+B组合）

### 路径A：AI 内置工具（零配置，实时性强）

| 工具 | 数据类型 | 用途 |
|------|---------|------|
| `search_web` | 实时行情/新闻/政策 | 搜索最新信息 |
| `fetch_content` | 财经网页内容 | 抓取东方财富/雪球/巨潮等结构化页面 |

**覆盖网站**:
- 行情: 东方财富(eastmoney.com)、新浪财经、腾讯财经
- 财报: 巨潮资讯网(cninfo.com.cn)
- 社区: 雪球(xueqiu.com)
- 新闻: 财联社、第一财经、华尔街见闻
- 政策: 央行、证监会、财政部
- 美股: Yahoo Finance, SEC EDGAR

### 路径B：本地 Python 脚本（批量+历史数据）

| 库 | 数据类型 | 安装 |
|----|---------|------|
| `akshare` | A股/港股/美股/基金/期货全量数据 | `pip install akshare` |
| `yfinance` | 美股/全球指数 | `pip install yfinance` |
| `tushare` | A股专业数据(需token) | `pip install tushare` |

**脚本位置**: `scripts/` 目录下提供标准化采集脚本

---

## 架构文档

| 文档 | 内容 |
|------|------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | 三层四智体架构详细设计 |
| [WORKFLOW.md](WORKFLOW.md) | AI 执行工作流（五阶段闭环） |
| [frameworks/value-investment.md](frameworks/value-investment.md) | 价值投资分析五步法 |
| [frameworks/trend-trading.md](frameworks/trend-trading.md) | 趋势交易分析四象限 |

## 知识库

| 文档 | 知识源 |
|------|--------|
| [knowledge/duan-yongping.md](knowledge/duan-yongping.md) | 段永平《大道》 |
| [knowledge/charlie-munger.md](knowledge/charlie-munger.md) | 查理芒格思维模型 |
| [knowledge/ray-dalio.md](knowledge/ray-dalio.md) | 瑞·达利欧《原则》 |
| [knowledge/zhang-lei.md](knowledge/zhang-lei.md) | 张磊《价值》 |
| [knowledge/jesse-livermore.md](knowledge/jesse-livermore.md) | 利弗莫尔交易智慧 |
| [knowledge/kondratieff-cycle.md](knowledge/kondratieff-cycle.md) | 康波周期理论 |
| [knowledge/behavioral-finance.md](knowledge/behavioral-finance.md) | 行为金融学/认知偏差 |
| [knowledge/financial-analysis.md](knowledge/financial-analysis.md) | 财务分析方法论 |
| [knowledge/data-analysis.md](knowledge/data-analysis.md) | 数据分析精要 |

## 技能模块

| 层级 | 技能 | 文档 |
|------|------|------|
| 数据层 | 行情获取 | [skills/data-layer/market-data-fetcher.md](skills/data-layer/market-data-fetcher.md) |
| 数据层 | 基本面解析 | [skills/data-layer/fundamentals-parser.md](skills/data-layer/fundamentals-parser.md) |
| 数据层 | 另类数据采集 | [skills/data-layer/alt-data-collector.md](skills/data-layer/alt-data-collector.md) |
| 研究层 | 情绪分析 | [skills/research-layer/sentiment-analyzer.md](skills/research-layer/sentiment-analyzer.md) |
| 研究层 | 因子评分引擎 | [skills/research-layer/factor-scoring-engine.md](skills/research-layer/factor-scoring-engine.md) |
| 研究层 | 事件冲击分析 | [skills/research-layer/event-impact-analyzer.md](skills/research-layer/event-impact-analyzer.md) |
| 研究层 | 技术形态识别 | [skills/research-layer/technical-pattern-recognizer.md](skills/research-layer/technical-pattern-recognizer.md) |
| 研究层 | 康波周期分析 | [skills/research-layer/kondratieff-cycle-analyzer.md](skills/research-layer/kondratieff-cycle-analyzer.md) |
| 决策层 | 风控守门员 | [skills/decision-layer/risk-guardrail.md](skills/decision-layer/risk-guardrail.md) |
| 决策层 | 组合建议 | [skills/decision-layer/portfolio-suggestion.md](skills/decision-layer/portfolio-suggestion.md) |
| 决策层 | 研报生成器 | [skills/decision-layer/report-generator.md](skills/decision-layer/report-generator.md) |

---

## 强制约束

### 必须做
1. 所有分析必须**标注数据来源和时效性**（数据截至xxxx年xx月xx日）
2. 投资建议必须附带**风险提示**
3. 使用两套框架时必须**分别独立评估**，不可混淆
4. 涉及金额/收益率必须使用**精确数值**，不可模糊表述
5. 认知偏差检查是**强制环节**，不可跳过

### 不要做
1. 不要给出"一定涨/一定跌"等绝对性结论
2. 不要忽略风控检查直接给出买入建议
3. 不要用单一指标做最终决策（必须多维度交叉验证）
4. 不要在数据不足时强行给出评分（应标注"数据不足，建议补充"）
5. 不要遗漏任何一个检查清单项目

### 免责声明
> 本系统仅提供投资分析辅助，不构成投资建议。投资有风险，决策需谨慎。
> 历史数据不代表未来表现，所有分析仅供参考。
