# 交易计划模板

> 单笔交易的完整执行计划，由 Executor 智体输出

---

## 📝 交易执行计划

### 基本信息
| 项目 | 内容 |
|------|------|
| **标的** | {stock_name}（{stock_code}） |
| **计划编号** | PLAN-{plan_id} |
| **生成日期** | {date} |
| **有效期** | {valid_until} |
| **分析框架** | {framework} |
| **信号来源** | {signal_source} |

---

### 一、交易方向与理由

**方向**: {direction}（做多/做空/观望）

**核心理由（3句话）**:
1. {reason_1}
2. {reason_2}
3. {reason_3}

**反面论证（避免确认偏差）**:
- 看空理由1: {bear_1}
- 看空理由2: {bear_2}
- 反驳: {rebuttal}

---

### 二、入场策略

| 项目 | 内容 |
|------|------|
| 入场方式 | {entry_method}（限价/市价/突破触发） |
| 入场价格 | {entry_price}元 |
| 触发条件 | {entry_trigger} |
| 确认信号 | {confirm_signal} |
| 取消条件 | {cancel_condition} |

**入场检查清单**:
- [ ] 大盘环境是否配合？{market_ok}
- [ ] 板块是否联动？{sector_ok}
- [ ] 量能是否达标？{volume_ok}
- [ ] 情绪是否适中？{sentiment_ok}
- [ ] 是否避开财报/政策窗口？{event_ok}

---

### 三、仓位管理

**账户信息**:
| 项目 | 数值 |
|------|------|
| 总资金 | {total_capital}万元 |
| 可用资金 | {available_capital}万元 |
| 当前持仓数 | {current_positions}只 |
| 单只最大仓位 | {max_single_pos}% |

**分批建仓计划（金字塔法）**:
| 批次 | 仓位比例 | 金额(万) | 股数 | 触发条件 |
|------|---------|---------|------|---------|
| 第一批(试探) | {b1_pct}% | {b1_amt} | {b1_shares} | {b1_trigger} |
| 第二批(确认) | {b2_pct}% | {b2_amt} | {b2_shares} | {b2_trigger} |
| 第三批(追加) | {b3_pct}% | {b3_amt} | {b3_shares} | {b3_trigger} |
| **合计** | **{total_pct}%** | **{total_amt}** | **{total_shares}** | — |

---

### 四、止损计划

| 止损类型 | 触发价 | 亏损幅度 | 亏损金额(万) | 执行方式 |
|---------|--------|---------|------------|---------|
| 初始止损 | {stop_1}元 | -{s1_pct}% | {s1_amt} | 跌破即卖 |
| 时间止损 | — | — | — | 持有{time_days}天未达预期 |
| 事件止损 | — | — | — | {event_stop_condition} |

**利弗莫尔铁律**: 
- 到价即执行，不找借口
- 单笔亏损不超过总资金的{max_loss_pct}%
- 连续止损{consecutive_stops}次后强制停手{cool_days}天

---

### 五、止盈计划

| 阶段 | 目标价 | 涨幅 | 操作 | 剩余仓位 |
|------|--------|------|------|---------|
| 止盈1 | {tp1_price}元 | +{tp1_pct}% | 卖出{tp1_sell}% | {tp1_remain}% |
| 止盈2 | {tp2_price}元 | +{tp2_pct}% | 卖出{tp2_sell}% | {tp2_remain}% |
| 止盈3 | {tp3_price}元 | +{tp3_pct}% | 清仓 | 0% |
| 移动止盈 | 最高价回撤{trail}% | — | 全部卖出 | 0% |

---

### 六、盈亏比分析

| 项目 | 数值 |
|------|------|
| 入场价 | {entry}元 |
| 止损价 | {stop}元 |
| 目标价(加权) | {target_avg}元 |
| 下行空间 | {downside}% |
| 上行空间 | {upside}% |
| **盈亏比** | **{rr_ratio}:1** |
| 胜率估计 | {win_rate}% |
| 期望值 | {expected_value} |

**交易纪律**:
- 盈亏比 < 2:1 → 不开仓
- 盈亏比 2:1~3:1 → 半仓
- 盈亏比 > 3:1 → 标准仓位

---

### 七、执行日志（交易后填写）

| 时间 | 操作 | 价格 | 数量 | 仓位变化 | 备注 |
|------|------|------|------|---------|------|
| {exec_time_1} | {exec_action_1} | {exec_price_1} | {exec_qty_1} | {pos_change_1} | {exec_note_1} |
| {exec_time_2} | {exec_action_2} | {exec_price_2} | {exec_qty_2} | {pos_change_2} | {exec_note_2} |

---

### 八、计划确认

- [ ] 我已仔细审阅本交易计划
- [ ] 我接受最大亏损{max_loss}万元（{max_loss_pct}%）
- [ ] 我承诺严格执行止损纪律
- [ ] 我已检查认知偏差（无确认偏差/过度自信）
- [ ] 我理解此计划不构成投资建议

---

*本计划由 FinMind Executor 智体生成。计划失效条件: 超过有效期 / 基本面重大变化 / 市场环境剧变*
