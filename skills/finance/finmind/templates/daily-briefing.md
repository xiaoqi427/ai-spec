# 每日简报模板

> 每日市场快报，用于 report-generator 技能的 `daily` 模式输出

---

## 📰 FinMind 每日市场简报

**日期**: {date} {weekday}
**生成时间**: {timestamp}

---

### 一、大盘概况

| 指数 | 收盘 | 涨跌幅 | 成交额(亿) | 信号 |
|------|------|--------|-----------|------|
| 上证指数 | {sh_close} | {sh_change}% | {sh_volume} | {sh_signal} |
| 深证成指 | {sz_close} | {sz_change}% | {sz_volume} | {sz_signal} |
| 创业板指 | {cy_close} | {cy_change}% | {cy_volume} | {cy_signal} |
| 科创50 | {kc_close} | {kc_change}% | {kc_volume} | {kc_signal} |
| 恒生指数 | {hs_close} | {hs_change}% | — | {hs_signal} |
| 标普500 | {sp_close} | {sp_change}% | — | {sp_signal} |

**两市合计**: 成交{total_volume}亿元 | 上涨{up_count}家 | 下跌{down_count}家 | 涨停{limit_up}家 | 跌停{limit_down}家

---

### 二、情绪温度

| 指标 | 数值 | 昨日 | 变化 | 区间 |
|------|------|------|------|------|
| 恐贪指数 | {fg_today}/100 | {fg_yesterday} | {fg_change} | {fg_zone} |
| 融资余额 | {margin_bal}亿 | {margin_yesterday} | {margin_change} | — |
| 北向资金 | {north_net}亿 | {north_yesterday} | — | {north_signal} |

**情绪判断**: {emotion_verdict}

---

### 三、板块热点

**涨幅前5**:
| 排名 | 板块 | 涨幅 | 领涨股 | 逻辑 |
|------|------|------|--------|------|
| 1 | {top1_sector} | +{top1_pct}% | {top1_leader} | {top1_logic} |
| 2 | {top2_sector} | +{top2_pct}% | {top2_leader} | {top2_logic} |
| 3 | {top3_sector} | +{top3_pct}% | {top3_leader} | {top3_logic} |
| 4 | {top4_sector} | +{top4_pct}% | {top4_leader} | {top4_logic} |
| 5 | {top5_sector} | +{top5_pct}% | {top5_leader} | {top5_logic} |

**跌幅前3**:
| 排名 | 板块 | 跌幅 | 原因 |
|------|------|------|------|
| 1 | {bot1_sector} | {bot1_pct}% | {bot1_reason} |
| 2 | {bot2_sector} | {bot2_pct}% | {bot2_reason} |
| 3 | {bot3_sector} | {bot3_pct}% | {bot3_reason} |

---

### 四、重要新闻/事件

| 时间 | 事件 | 影响范围 | 重要性 | 简评 |
|------|------|---------|--------|------|
| {news_1_time} | {news_1} | {news_1_scope} | {news_1_level} | {news_1_comment} |
| {news_2_time} | {news_2} | {news_2_scope} | {news_2_level} | {news_2_comment} |
| {news_3_time} | {news_3} | {news_3_scope} | {news_3_level} | {news_3_comment} |

---

### 五、持仓跟踪

| 标的 | 今日涨跌 | 持仓盈亏 | 需要关注 | 操作建议 |
|------|---------|---------|---------|---------|
| {w1_name} | {w1_change}% | {w1_pnl}% | {w1_alert} | {w1_action} |
| {w2_name} | {w2_change}% | {w2_pnl}% | {w2_alert} | {w2_action} |
| {w3_name} | {w3_change}% | {w3_pnl}% | {w3_alert} | {w3_action} |

---

### 六、明日关注

**重要事件**:
- {tomorrow_event_1}
- {tomorrow_event_2}

**技术位提醒**:
- {tech_alert_1}
- {tech_alert_2}

**操作提醒**:
- {action_alert_1}
- {action_alert_2}

---

### 七、每日智慧

> "{daily_wisdom}"
> —— {wisdom_author}

---

*本简报由 FinMind Observer 智体自动生成。数据来源: AKShare + 网络公开信息。*
*⚠️ 仅供参考，不构成投资建议。*
