# 深度研报模板

> 完整版深度研究报告，用于 report-generator 技能的 `deep` 模式输出

---

## 📋 {stock_name}（{stock_code}）深度研究报告

**报告日期**: {date}
**分析框架**: {framework}（价值投资/趋势交易/双框架）
**报告版本**: v{version}

---

### 一、投资摘要（Executive Summary）

**核心观点**: {core_thesis}

| 项目 | 内容 |
|------|------|
| 投资评级 | {rating}（强烈推荐/推荐/中性/回避） |
| 目标价格 | {target_price}元（{upside}%上升空间） |
| 当前价格 | {current_price}元 |
| 核心逻辑 | {logic_summary} |
| 主要风险 | {risk_summary} |
| 建议操作 | {action_summary} |

---

### 二、公司概况

**基本信息**:
| 项目 | 内容 |
|------|------|
| 公司全称 | {full_name} |
| 所属行业 | {industry} / {sub_industry} |
| 上市时间 | {ipo_date} |
| 总市值 | {market_cap}亿 |
| 流通市值 | {float_cap}亿 |
| 实控人 | {controller} |

**业务构成**:
| 业务板块 | 营收占比 | 毛利率 | 增速 |
|---------|---------|--------|------|
| {biz_1} | {rev_1}% | {gm_1}% | {growth_1}% |
| {biz_2} | {rev_2}% | {gm_2}% | {growth_2}% |
| {biz_3} | {rev_3}% | {gm_3}% | {growth_3}% |

**竞争格局**:
| 排名 | 公司 | 市占率 | 核心优势 |
|------|------|--------|---------|
| 1 | {comp_1} | {share_1}% | {adv_1} |
| 2 | {comp_2} | {share_2}% | {adv_2} |
| 3 | {comp_3} | {share_3}% | {adv_3} |

---

### 三、投资逻辑详述

#### 3.1 核心逻辑一：{logic_title_1}

{logic_detail_1}

**支撑数据**: {logic_data_1}

#### 3.2 核心逻辑二：{logic_title_2}

{logic_detail_2}

**支撑数据**: {logic_data_2}

#### 3.3 核心逻辑三：{logic_title_3}

{logic_detail_3}

**支撑数据**: {logic_data_3}

---

### 四、财务分析

#### 4.1 三表核心指标

**利润表**:
| 指标 | {year_3}A | {year_2}A | {year_1}A | {year_0}E | {year_p1}E |
|------|----------|----------|----------|----------|-----------|
| 营收(亿) | {rev_y3} | {rev_y2} | {rev_y1} | {rev_y0} | {rev_yp1} |
| 营收增速 | {rev_g3}% | {rev_g2}% | {rev_g1}% | {rev_g0}% | {rev_gp1}% |
| 毛利率 | {gm_y3}% | {gm_y2}% | {gm_y1}% | {gm_y0}% | {gm_yp1}% |
| 净利润(亿) | {np_y3} | {np_y2} | {np_y1} | {np_y0} | {np_yp1} |
| 净利率 | {nm_y3}% | {nm_y2}% | {nm_y1}% | {nm_y0}% | {nm_yp1}% |

**资产负债表关键**:
| 指标 | 最新值 | 同比变化 | 风险提示 |
|------|--------|---------|---------|
| 资产负债率 | {debt_ratio}% | {debt_change} | {debt_risk} |
| 流动比率 | {current_ratio} | {cr_change} | {cr_risk} |
| 商誉/净资产 | {goodwill_ratio}% | {gw_change} | {gw_risk} |

**现金流量表**:
| 指标 | 最新值 | 趋势 | 质量评价 |
|------|--------|------|---------|
| 经营现金流/净利润 | {ocf_np_ratio} | {ocf_trend} | {ocf_quality} |
| 自由现金流(亿) | {fcf} | {fcf_trend} | {fcf_quality} |
| 资本支出(亿) | {capex} | {capex_trend} | {capex_note} |

#### 4.2 杜邦分析

| 指标 | 数值 | 驱动类型 |
|------|------|---------|
| ROE | {roe}% | — |
| = 净利率 | {net_margin}% | {margin_driver} |
| × 总资产周转率 | {asset_turnover}x | {turnover_driver} |
| × 权益乘数 | {equity_multiplier}x | {leverage_driver} |
| **杜邦模式** | — | **{dupont_type}** |

---

### 五、估值分析

#### 5.1 绝对估值 — DCF
| 参数 | 取值 | 依据 |
|------|------|------|
| FCF基期 | {dcf_fcf}亿 | {dcf_basis} |
| 增长率(高增) | {dcf_g1}% | {dcf_g1_basis} |
| 增长率(稳态) | {dcf_g2}% | {dcf_g2_basis} |
| 永续增长率 | {dcf_tg}% | ≤名义GDP |
| WACC | {dcf_wacc}% | {wacc_detail} |
| **内在价值** | **{dcf_value}元** | — |
| **安全边际** | **{dcf_mos}%** | 目标≥30% |

#### 5.2 相对估值
| 方法 | 合理估值 | 当前值 | 历史分位 | 结论 |
|------|---------|--------|---------|------|
| PE(TTM) | {pe_fair}x | {pe_now}x | {pe_pct}% | {pe_verdict} |
| PB(LF) | {pb_fair}x | {pb_now}x | {pb_pct}% | {pb_verdict} |
| EV/EBITDA | {ev_fair}x | {ev_now}x | {ev_pct}% | {ev_verdict} |

**综合估值结论**: {valuation_conclusion}

---

### 六、风险提示

| # | 风险类型 | 风险描述 | 概率 | 影响 |
|---|---------|---------|------|------|
| 1 | {risk_type_1} | {risk_desc_1} | {risk_prob_1} | {risk_impact_1} |
| 2 | {risk_type_2} | {risk_desc_2} | {risk_prob_2} | {risk_impact_2} |
| 3 | {risk_type_3} | {risk_desc_3} | {risk_prob_3} | {risk_impact_3} |
| 4 | {risk_type_4} | {risk_desc_4} | {risk_prob_4} | {risk_impact_4} |

---

### 七、操作建议

| 项目 | 内容 |
|------|------|
| 评级 | {final_rating} |
| 目标价 | {target_price}元 |
| 买入区间 | {buy_range}元 |
| 止损价位 | {stop_loss}元 |
| 目标仓位 | {position}% |
| 持有周期 | {hold_period} |
| 复查时间 | {review_date} |

---

### 八、偏差自查记录

| 检查项 | 是否存在 | 处理措施 |
|--------|---------|---------|
| 确认偏差 | {bias_confirm} | {bias_confirm_action} |
| 锚定效应 | {bias_anchor} | {bias_anchor_action} |
| 过度自信 | {bias_overconfident} | {bias_overconfident_action} |
| 损失厌恶 | {bias_loss_aversion} | {bias_loss_action} |
| 从众心理 | {bias_herding} | {bias_herding_action} |

---

*本报告由 FinMind 智投系统生成，融合多源知识体系。仅供参考，不构成投资建议。*
*生成时间: {timestamp} | 数据截止: {data_cutoff}*
