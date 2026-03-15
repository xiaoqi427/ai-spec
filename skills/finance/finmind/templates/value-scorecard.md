# 价值评分卡模板

> 框架A"价值投资五步法"的标准化输出模板

---

## 📊 价值投资评分卡

### 基本信息
| 项目 | 内容 |
|------|------|
| **标的** | {stock_name}（{stock_code}） |
| **行业** | {industry} |
| **分析日期** | {date} |
| **分析师智体** | Analyst → Strategist |
| **数据时效** | 截至 {data_date} |

---

### 五步评分总览

| 步骤 | 维度 | 得分(1-10) | 权重 | 加权分 |
|------|------|-----------|------|--------|
| Step1 | 能力圈匹配度 | {s1_score} | 15% | {s1_weighted} |
| Step2 | 商业模式质量 | {s2_score} | 25% | {s2_weighted} |
| Step3 | 财务健康度 | {s3_score} | 25% | {s3_weighted} |
| Step4 | 估值安全边际 | {s4_score} | 25% | {s4_weighted} |
| Step5 | 检查清单通过率 | {s5_score} | 10% | {s5_weighted} |
| **总计** | — | — | 100% | **{total_score}/10** |

---

### Step 1：能力圈评估

**是否在能力圈内**: {in_circle} (是/否/边缘)

| 检查项 | 评估 |
|--------|------|
| 能否用一句话说清商业模式 | {biz_one_sentence} |
| 是否理解主要收入来源 | {understand_revenue} |
| 是否了解行业竞争格局 | {understand_competition} |
| 是否知道核心风险在哪 | {understand_risk} |
| 段永平"不懂不做"检验 | {duan_test} |

**能力圈判定**: {circle_verdict}

---

### Step 2：商业模式 — 护城河五维度

| 维度 | 得分(1-10) | 关键证据 |
|------|-----------|---------|
| 品牌溢价 | {moat_brand} | {brand_evidence} |
| 转换成本 | {moat_switch} | {switch_evidence} |
| 网络效应 | {moat_network} | {network_evidence} |
| 成本优势 | {moat_cost} | {cost_evidence} |
| 牌照/专利壁垒 | {moat_license} | {license_evidence} |
| **综合护城河** | **{moat_avg}** | — |

**张磊"动态护城河"评估**: {zhang_lei_moat}
- 护城河是否在加宽？{moat_widening}
- 管理层是否持续投入？{mgmt_reinvest}

---

### Step 3：财务健康 — 杜邦拆解

**三表速览**:
| 指标 | 最新值 | 3年趋势 | 行业均值 | 评级 |
|------|--------|---------|---------|------|
| ROE | {roe}% | {roe_trend} | {roe_industry}% | {roe_grade} |
| 净利率 | {net_margin}% | {margin_trend} | {margin_industry}% | {margin_grade} |
| 总资产周转率 | {asset_turnover} | {turnover_trend} | {turnover_industry} | {turnover_grade} |
| 权益乘数 | {equity_multiplier} | {leverage_trend} | {leverage_industry} | {leverage_grade} |
| 经营现金流/净利润 | {ocf_ratio} | {ocf_trend} | ≥1.0 | {ocf_grade} |
| 资产负债率 | {debt_ratio}% | {debt_trend} | {debt_industry}% | {debt_grade} |
| 自由现金流(亿) | {fcf} | {fcf_trend} | — | {fcf_grade} |

**杜邦模式判定**: {dupont_type}
- A型(高利润率): 利润率驱动型 → 关注定价权
- B型(高周转): 周转率驱动型 → 关注运营效率
- C型(高杠杆): 杠杆驱动型 → 关注债务风险

**财务红旗检查**:
- [ ] 应收账款增速 > 营收增速？{ar_flag}
- [ ] 存货异常堆积？{inventory_flag}
- [ ] 经营现金流持续 < 净利润？{ocf_flag}
- [ ] 商誉占净资产 > 30%？{goodwill_flag}
- [ ] 频繁更换审计机构？{audit_flag}

---

### Step 4：估值安全边际

**绝对估值 — DCF**:
| 参数 | 取值 | 说明 |
|------|------|------|
| 自由现金流(基期) | {fcf_base}亿 | {fcf_source} |
| 增长率(前5年) | {growth_5y}% | {growth_basis} |
| 增长率(后5年) | {growth_10y}% | 逐步回归 |
| 永续增长率 | {terminal_growth}% | ≤GDP增速 |
| WACC | {wacc}% | {wacc_calc} |
| **DCF内在价值** | **{dcf_value}元** | — |
| 当前股价 | {current_price}元 | — |
| **安全边际** | **{margin_of_safety}%** | 目标≥30% |

**相对估值**:
| 方法 | 估值(元) | 当前比率 | 历史分位 |
|------|---------|---------|---------|
| PE | {pe_value} | {pe_current}x | {pe_percentile}% |
| PB | {pb_value} | {pb_current}x | {pb_percentile}% |
| PS | {ps_value} | {ps_current}x | {ps_percentile}% |
| EV/EBITDA | {ev_value} | {ev_current}x | {ev_percentile}% |
| PEG | — | {peg_current} | — |

**段永平"老巴出价法"**: 
- 合理价格: {fair_price}元
- "打折"目标价: {discount_price}元（7折）
- 当前安全边际足够？{safety_enough}

---

### Step 5：芒格检查清单 (25项精选)

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | 我能说清这家公司靠什么赚钱吗？ | {c1} |
| 2 | 如果有100亿，能复制它的生意吗？ | {c2} |
| 3 | 管理层是否诚信且有能力？ | {c3} |
| 4 | 十年后这家公司还会存在吗？ | {c4} |
| 5 | 买入理由能否用三句话说清？ | {c5} |
| ... | (完整25项见 checklists/munger-checklist.md) | ... |

**通过率**: {pass_rate}% ({passed}/{total})
- ≥80%: 强烈推荐深度研究
- 60-80%: 值得关注，需补充研究
- <60%: 建议放弃

---

### 综合结论

**评级**: {final_rating} (强烈推荐 / 推荐 / 观望 / 回避)

**核心逻辑**(3句话):
1. {logic_1}
2. {logic_2}
3. {logic_3}

**关键风险**:
1. {risk_1}
2. {risk_2}
3. {risk_3}

**建议操作**:
- 目标仓位: {target_position}%
- 买入区间: {buy_range}元
- 止损价位: {stop_loss}元
- 持有周期: {hold_period}

---

### 知识融合声明

本评分卡融合以下投资智慧:
- 段永平《大道》: 能力圈 + "不懂不做" + 老巴出价法
- 查理芒格: 25项检查清单 + 多元思维模型
- 张磊《价值》: 动态护城河 + 长坡厚雪
- 瑞·达利欧《原则》: 极度透明 + 风险平价思维
- 财务分析方法论: 杜邦拆解 + DCF估值

*⚠️ 本评分卡仅为分析工具，不构成投资建议。投资有风险，入市需谨慎。*
