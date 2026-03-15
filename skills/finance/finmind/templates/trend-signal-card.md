# 趋势信号卡模板

> 框架B"趋势交易四象限"的标准化输出模板

---

## 📈 趋势交易信号卡

### 基本信息
| 项目 | 内容 |
|------|------|
| **标的** | {stock_name}（{stock_code}） |
| **市场** | {market}（A股/港股/美股） |
| **分析日期** | {date} |
| **信号类型** | {signal_type}（买入/卖出/观望/加仓/减仓） |
| **信号强度** | {signal_strength}（强/中/弱） |

---

### 四象限总览

| 象限 | 维度 | 信号 | 权重 | 得分(1-10) |
|------|------|------|------|-----------|
| Q1 | 宏观周期定位 | {q1_signal} | 20% | {q1_score} |
| Q2 | 市场情绪温度 | {q2_signal} | 20% | {q2_score} |
| Q3 | 技术形态识别 | {q3_signal} | 35% | {q3_score} |
| Q4 | 交易计划生成 | {q4_signal} | 25% | {q4_score} |
| **综合** | — | **{overall_signal}** | 100% | **{total}/10** |

---

### Q1：宏观周期定位

**康波周期**:
| 周期 | 当前阶段 | 持续时间 | 对应策略 |
|------|---------|---------|---------|
| 康德拉季耶夫(50-60年) | {kond_phase} | {kond_duration} | {kond_strategy} |
| 朱格拉(7-11年) | {juglar_phase} | {juglar_duration} | {juglar_strategy} |
| 基钦(3-5年) | {kitchin_phase} | {kitchin_duration} | {kitchin_strategy} |

**宏观指标**:
| 指标 | 当前值 | 趋势 | 信号 |
|------|--------|------|------|
| GDP增速 | {gdp_growth}% | {gdp_trend} | {gdp_signal} |
| CPI | {cpi}% | {cpi_trend} | {cpi_signal} |
| M2增速 | {m2_growth}% | {m2_trend} | {m2_signal} |
| 10Y国债收益率 | {bond_yield}% | {bond_trend} | {bond_signal} |
| 社融增速 | {social_finance}% | {sf_trend} | {sf_signal} |
| PMI | {pmi} | {pmi_trend} | {pmi_signal} |

**周期结论**: {cycle_conclusion}
- 大类资产建议: {asset_allocation}

---

### Q2：市场情绪温度

**情绪指标**:
| 指标 | 当前值 | 区间 | 信号 |
|------|--------|------|------|
| 恐贪指数 | {fear_greed}/100 | {fg_zone} | {fg_signal} |
| 融资余额变化 | {margin_change}% | {margin_zone} | {margin_signal} |
| 北向资金(5日) | {northbound}亿 | {nb_zone} | {nb_signal} |
| 成交量/MA20 | {vol_ratio} | {vol_zone} | {vol_signal} |
| 涨跌停比 | {limit_ratio} | {lr_zone} | {lr_signal} |
| 新闻情绪 | {news_sentiment} | -1~+1 | {ns_signal} |

**情绪温度计**: {emotion_temperature}
```
极度恐惧 ◀━━━━━●━━━━━▶ 极度贪婪
   0    20   40   60   80   100
                {emotion_marker}
```

**达利欧"极度透明"检查**:
- 市场主流叙事: {main_narrative}
- 叙事是否过度一致？{narrative_consensus}
- 反向思考: {contrarian_view}

---

### Q3：技术形态识别

**趋势判断**:
| 时间框架 | 趋势方向 | 强度 | 关键均线 |
|---------|---------|------|---------|
| 周线 | {weekly_trend} | {w_strength} | {w_ma} |
| 日线 | {daily_trend} | {d_strength} | {d_ma} |
| 60分钟 | {h1_trend} | {h1_strength} | {h1_ma} |

**形态识别**:
| 形态 | 类型 | 可靠度 | 目标位 |
|------|------|--------|-------|
| {pattern_1} | {type_1} | {reliability_1} | {target_1} |
| {pattern_2} | {type_2} | {reliability_2} | {target_2} |

**量价关系**:
| 检查项 | 结果 |
|--------|------|
| 量价齐升？ | {vol_price_up} |
| 放量突破？ | {vol_breakout} |
| 缩量回踩？ | {vol_pullback} |
| 量能背离？ | {vol_divergence} |

**游子/柚子体系检查**:
| 法则 | 满足 | 说明 |
|------|------|------|
| 选股法则 — 强势股 | {youzi_strong} | 近20日涨幅排名 |
| 选股法则 — 题材热度 | {youzi_theme} | 板块资金流向 |
| 择时 — 突破买入 | {youzi_breakout} | 新高+放量 |
| 择时 — 回踩买入 | {youzi_pullback} | 缩量回踩支撑 |
| 择时 — 首阴反包 | {youzi_firstyin} | 首根阴线次日反包 |
| 止损纪律 | {youzi_stoploss} | 破位即走 |

---

### Q4：交易计划

**入场计划**:
| 项目 | 内容 |
|------|------|
| **方向** | {direction}（做多/做空/观望） |
| **入场价** | {entry_price}元 |
| **入场条件** | {entry_condition} |
| **入场方式** | {entry_method}（突破/回踩/首阴反包） |

**仓位管理 — 金字塔加仓法**:
| 批次 | 仓位 | 触发价 | 累计仓位 |
|------|------|--------|---------|
| 首仓(试探) | {pos_1}% | {trigger_1}元 | {cum_1}% |
| 二次加仓 | {pos_2}% | {trigger_2}元 | {cum_2}% |
| 三次加仓 | {pos_3}% | {trigger_3}元 | {cum_3}% |
| **最大仓位** | — | — | **{max_pos}%** |

**止损/止盈**:
| 类型 | 价格 | 幅度 | 条件 |
|------|------|------|------|
| 硬止损 | {hard_stop}元 | -{stop_pct}% | 跌破即执行 |
| 移动止盈 | {trail_stop} | {trail_pct}% | 从最高点回撤 |
| 目标止盈1 | {target_1}元 | +{t1_pct}% | 减仓1/3 |
| 目标止盈2 | {target_2}元 | +{t2_pct}% | 减仓1/3 |
| 目标止盈3 | {target_3}元 | +{t3_pct}% | 清仓 |

**利弗莫尔纪律提醒**:
- ⚠️ "市场永远不会错，只有观点会出错"
- ⚠️ 止损不犹豫，到价即执行
- ⚠️ 永远不要加仓一个亏损的头寸

---

### 风险评估

| 风险项 | 等级 | 说明 |
|--------|------|------|
| 单笔最大亏损 | {max_loss}元 | 占总资金{loss_pct}% |
| 黑天鹅风险 | {black_swan} | {swan_desc} |
| 流动性风险 | {liquidity} | {liq_desc} |
| 政策风险 | {policy_risk} | {policy_desc} |

---

### 综合信号

**操作建议**: {final_action}（买入/卖出/持有/观望）
**信心等级**: {confidence}%
**时间窗口**: {time_window}

**一句话总结**: {one_line_summary}

---

### 知识融合声明

本信号卡融合以下交易智慧:
- 利弗莫尔《股票作手回忆录》: 关键位理论 + 止损纪律
- 康波周期理论: 三层嵌套周期定位
- 游子/柚子实战体系: 选股+择时+仓位管理
- 行为金融学: 情绪温度计 + 反人性检查
- 瑞·达利欧《原则》: 极度透明 + 反叙事思维

*⚠️ 本信号卡仅为分析工具，不构成投资建议。投资有风险，入市需谨慎。*
