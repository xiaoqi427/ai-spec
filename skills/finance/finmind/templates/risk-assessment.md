# 风险评估模板

> 风控守门员（Risk Guardrail）技能的标准化输出

---

## 🛡️ 风险评估报告

### 基本信息
| 项目 | 内容 |
|------|------|
| **评估对象** | {stock_name}（{stock_code}） |
| **评估日期** | {date} |
| **触发场景** | {trigger}（新建仓/加仓/持仓复查/市场异动） |
| **风险等级** | {risk_level}（低/中/高/极高） |
| **是否通过** | {pass_or_block}（通过/拦截/需人工确认） |

---

### 一、仓位风险检查

| 检查项 | 当前值 | 阈值 | 状态 |
|--------|--------|------|------|
| 单只股票仓位 | {single_pos}% | ≤{single_max}% | {single_status} |
| 单行业仓位 | {sector_pos}% | ≤{sector_max}% | {sector_status} |
| 单市场仓位 | {market_pos}% | ≤{market_max}% | {market_status} |
| 总仓位占比 | {total_pos}% | ≤{total_max}% | {total_status} |
| 现金储备 | {cash_pct}% | ≥{cash_min}% | {cash_status} |

**仓位评估**: {position_verdict}

---

### 二、止损合规检查

| 检查项 | 当前值 | 要求 | 状态 |
|--------|--------|------|------|
| 是否设置止损 | {has_stoploss} | 必须 | {sl_status} |
| 止损幅度 | {sl_pct}% | 5-15% | {sl_range_status} |
| 单笔最大亏损/总资金 | {max_loss_pct}% | ≤2% | {max_loss_status} |
| 本周累计亏损 | {week_loss}% | ≤5% | {week_status} |
| 本月累计亏损 | {month_loss}% | ≤10% | {month_status} |

**止损评估**: {stoploss_verdict}

**熔断机制**:
| 级别 | 触发条件 | 操作 | 当前状态 |
|------|---------|------|---------|
| 一级 | 单日亏损≥3% | 当日不再开新仓 | {fuse_1} |
| 二级 | 周亏损≥5% | 本周减仓至50% | {fuse_2} |
| 三级 | 月亏损≥10% | 全部清仓，冷静30天 | {fuse_3} |

---

### 三、波动率风险检查

| 指标 | 当前值 | 阈值 | 信号 |
|------|--------|------|------|
| 个股20日波动率 | {stock_vol}% | 预警>{vol_warn}% | {stock_vol_status} |
| 大盘VIX/隐含波动率 | {vix} | 预警>{vix_warn} | {vix_status} |
| ATR(14)/价格 | {atr_ratio}% | — | {atr_status} |
| 涨跌幅(当日) | {day_change}% | 预警>|{day_warn}|% | {day_status} |
| 连续涨跌天数 | {consecutive_days}天 | 预警>{consec_warn} | {consec_status} |

**波动率评估**: {volatility_verdict}

---

### 四、认知偏差检查

| 偏差类型 | 风险信号 | 检测结果 | 处理建议 |
|---------|---------|---------|---------|
| 确认偏差 | 只看利好信息 | {bias_confirm} | {confirm_advice} |
| 锚定效应 | 紧盯买入价不放 | {bias_anchor} | {anchor_advice} |
| 过度自信 | 仓位过大/不设止损 | {bias_overconfident} | {overconfident_advice} |
| 损失厌恶 | 亏损不愿止损 | {bias_loss} | {loss_advice} |
| 沉没成本 | 因已亏损而加仓 | {bias_sunk} | {sunk_advice} |
| 从众心理 | 跟风热门股 | {bias_herding} | {herding_advice} |
| 近因偏差 | 过度看重近期事件 | {bias_recency} | {recency_advice} |

**偏差评估**: {bias_verdict}
**偏差得分**: {bias_score}/100（≥70分通过）

---

### 五、特殊风险扫描

| 风险类型 | 是否存在 | 详情 |
|---------|---------|------|
| 即将发布财报 | {earnings_risk} | {earnings_detail} |
| 重大政策变化 | {policy_risk} | {policy_detail} |
| 大股东减持 | {insider_risk} | {insider_detail} |
| 解禁期临近 | {lockup_risk} | {lockup_detail} |
| 退市风险警示 | {delist_risk} | {delist_detail} |
| 关联交易异常 | {related_risk} | {related_detail} |
| 审计意见非标 | {audit_risk} | {audit_detail} |

---

### 六、综合风险评分

| 维度 | 得分(0-100) | 权重 | 加权分 |
|------|-----------|------|--------|
| 仓位合规 | {pos_score} | 25% | {pos_weighted} |
| 止损合规 | {sl_score} | 25% | {sl_weighted} |
| 波动率风险 | {vol_score} | 20% | {vol_weighted} |
| 认知偏差 | {bias_score} | 20% | {bias_weighted} |
| 特殊风险 | {special_score} | 10% | {special_weighted} |
| **总分** | — | 100% | **{total_risk_score}/100** |

**风险等级判定**:
- 80-100分: 低风险 → 正常交易
- 60-79分: 中风险 → 降低仓位
- 40-59分: 高风险 → 仅允许减仓
- <40分: 极高风险 → **拦截交易**

**最终判定**: {final_verdict}

---

### 七、处理建议

{action_recommendations}

**达利欧"痛苦+反思=进步"提醒**:
> 如果本次被拦截，请回顾触发原因，记录在交易日志中，避免重复犯错。

---

*本评估由 FinMind Risk Guardrail 自动生成。风控检查为强制流程，不可跳过。*
