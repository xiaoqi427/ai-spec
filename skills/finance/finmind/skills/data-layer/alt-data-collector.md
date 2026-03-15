# 另类数据采集 (Alternative Data Collector)

> 数据层技能 — 监控新闻、社交媒体、政策公告等非结构化数据

## 功能

采集与投资标的相关的新闻、社交媒体讨论、政策公告等非结构化数据，
进行初步分类和标签化，为情绪分析和事件冲击分析提供素材。

## 数据获取策略

### 路径A: AI 内置工具（主要方式）
```
1. search_web 多维搜索:
   - "{公司名} 最新消息 利好 利空"
   - "{行业} 政策 监管"
   - "{公司名} 雪球 讨论"
   
2. fetch_content 定向抓取:
   - 财联社快讯: https://www.cls.cn/telegraph
   - 雪球讨论: https://xueqiu.com/S/{代码}
   - 东方财富股吧: https://guba.eastmoney.com/list,{代码}.html
```

### 路径B: Python 脚本（批量采集）
```bash
# 采集个股相关新闻
python scripts/fetch_news.py --symbol 600519 --days 7

# 采集行业新闻
python scripts/fetch_news.py --keyword "白酒行业" --days 7

# 采集政策公告
python scripts/fetch_news.py --source policy --days 30
```

## 采集内容分类

| 类别 | 数据源 | 采集内容 | 更新频率 |
|------|--------|---------|---------|
| **公司新闻** | 财联社/新浪财经 | 公告/业绩/人事变动 | 实时 |
| **行业动态** | 第一财经/华尔街见闻 | 行业政策/竞争格局 | 日级 |
| **社交讨论** | 雪球/股吧 | 投资者情绪/热度 | 实时 |
| **政策公告** | 央行/证监会/财政部 | 货币/财政/监管政策 | 事件驱动 |
| **研究报告** | 券商研报摘要 | 评级/目标价 | 周级 |

## 初步标签化

每条数据自动打标签:

```json
{
  "title": "茅台一季度批价稳定...",
  "source": "财联社",
  "timestamp": "2026-03-14T09:30:00+08:00",
  "tags": {
    "sentiment": "positive",
    "category": "业绩",
    "relevance": 0.92,
    "urgency": "normal",
    "reliability": "high"
  }
}
```

## 噪声过滤规则

参考 knowledge/data-analysis.md:
1. 来源可信度: 官方公告 > 主流媒体 > 自媒体 > 股吧评论
2. 多源交叉: 至少2个独立源确认才标注为"high reliability"
3. 去重处理: 同一事件不同渠道的报道合并为一条
4. 时效衰减: 超过7天的新闻降低权重
