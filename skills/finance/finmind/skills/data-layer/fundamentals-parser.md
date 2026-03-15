# 基本面数据解析 (Fundamentals Parser)

> 数据层技能 — 解析财报数据，提取关键财务指标

## 功能

获取上市公司的财务报表数据，进行三表分析，提取关键指标并进行评级。

## 数据获取策略

### 路径A: AI 内置工具
```
1. search_web 搜索 "{公司名称} 最新财报 财务数据"
2. fetch_content 抓取:
   - 雪球个股财务页: https://xueqiu.com/snowman/S/{代码}/detail#/GSLRB
   - 东方财富财务: https://emweb.securities.eastmoney.com/PC_HSF10/FinanceAnalysis/Index?type=soft&code={代码}
3. 解析关键指标
```

### 路径B: Python 脚本
```bash
# 获取A股财务数据
python scripts/fetch_financials.py --symbol 600519

# 获取美股财务数据
python scripts/fetch_financials.py --symbol AAPL --market US

# 获取指定年份
python scripts/fetch_financials.py --symbol 600519 --years 3
```

## 解析内容

### 提取指标清单

| 类别 | 指标 | 用途 |
|------|------|------|
| **盈利** | ROE/ROA/ROIC/毛利率/净利率 | 框架A Step3 盈利能力评估 |
| **成长** | 营收增速/净利增速/FCF增速 | 框架A Step3 成长性评估 |
| **安全** | 资产负债率/流动比率/有息负债率 | 框架A Step3 安全性评估 |
| **现金流** | OCF/净利润比/自由现金流 | 框架A Step3 盈利质量 |
| **估值** | PE/PB/PS/PEG/EV/EBITDA | 框架A Step4 估值分析 |
| **杜邦** | 净利率×周转率×杠杆 | 框架A Step3 ROE拆解 |

### 杜邦分析自动拆解
```
输入: ROE
输出:
  ROE = 净利率 × 资产周转率 × 权益乘数
  
  判断:
    高净利率驱动 → 好生意（如茅台型）
    高周转率驱动 → 好管理（如沃尔玛型）
    高杠杆驱动 → 需警惕（如银行型）
```

## 输出格式

```json
{
  "symbol": "600519",
  "name": "贵州茅台",
  "data_type": "fundamental",
  "report_period": "2025Q3",
  "profitability": {
    "roe": 32.1,
    "roa": 25.6,
    "gross_margin": 91.5,
    "net_margin": 51.3,
    "ocf_to_net_income": 1.15
  },
  "growth": {
    "revenue_yoy": 15.8,
    "net_income_yoy": 18.2,
    "fcf_yoy": 20.1
  },
  "safety": {
    "debt_ratio": 18.5,
    "current_ratio": 3.8,
    "interest_bearing_debt_ratio": 0
  },
  "valuation": {
    "pe_ttm": 28.5,
    "pb": 9.2,
    "ps": 14.6,
    "peg": 1.57
  },
  "dupont": {
    "net_margin": 51.3,
    "asset_turnover": 0.50,
    "equity_multiplier": 1.26,
    "driver": "高净利率型"
  },
  "source": "akshare",
  "quality_score": 0.92
}
```
