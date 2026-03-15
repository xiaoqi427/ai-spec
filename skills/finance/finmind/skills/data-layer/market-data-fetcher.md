# 行情数据获取 (Market Data Fetcher)

> 数据层技能 — 负责抓取 OHLCV 数据并标准化

## 功能

获取指定标的的行情数据，包括日K线、分钟K线、实时报价等，并进行数据清洗和标准化。

## 数据获取策略

### 路径A: AI 内置工具（实时/快速）

```
1. search_web 搜索 "{股票代码} 最新行情 实时报价"
2. fetch_content 抓取东方财富个股页面:
   A股: https://quote.eastmoney.com/concept/{代码}.html
   美股: https://finance.yahoo.com/quote/{代码}
3. 解析页面提取: 最新价/涨跌幅/成交量/成交额/换手率/52周高低
```

### 路径B: Python 脚本（历史/批量）

```bash
# A股行情（使用 akshare）
python scripts/fetch_market_data.py --symbol 600519 --period 1y --freq daily

# 美股行情（使用 yfinance）
python scripts/fetch_market_data.py --symbol AAPL --period 1y --freq daily --market US

# 实时行情
python scripts/fetch_market_data.py --symbol 600519 --realtime
```

## 输出格式

```json
{
  "symbol": "600519",
  "name": "贵州茅台",
  "market": "A",
  "data_type": "market",
  "timestamp": "2026-03-15T15:00:00+08:00",
  "realtime": {
    "price": 1856.00,
    "change_pct": 2.3,
    "volume": 25800000,
    "turnover": 4820000000,
    "turnover_rate": 0.38,
    "high_52w": 2050.00,
    "low_52w": 1420.00
  },
  "ohlcv": [
    {"date": "2026-03-15", "open": 1820, "high": 1860, "low": 1815, "close": 1856, "volume": 25800000},
    ...
  ],
  "source": "akshare",
  "quality_score": 0.95
}
```

## 支持市场

| 市场 | 代码格式 | 数据源 | 实时性 |
|------|---------|--------|--------|
| A股 | 600519 / 000001 | AKShare / 东方财富 | T+0(盘中15分钟延迟) |
| 港股 | 00700 | AKShare | T+0 |
| 美股 | AAPL / MSFT | yfinance / Yahoo | T+0 |
| 指数 | 000001(上证) / SPX | AKShare / yfinance | T+0 |
| ETF | 510300 / SPY | AKShare / yfinance | T+0 |
