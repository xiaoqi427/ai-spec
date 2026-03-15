#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FinMind 财务数据获取脚本
路径B: 本地Python脚本 — 使用 akshare 获取A股财务报表数据

使用方式:
    python fetch_financials.py --code 600519 --type income
    python fetch_financials.py --code 600519 --type balance
    python fetch_financials.py --code 600519 --type cashflow
    python fetch_financials.py --code 600519 --type indicators
    python fetch_financials.py --code 600519 --type all
    python fetch_financials.py --code 600519 --type dupont

依赖安装:
    pip install akshare pandas

@author sevenxiao
"""

import argparse
import json
import sys

import pandas as pd


def fetch_income_statement(code: str) -> dict:
    """
    获取利润表数据

    :param code: A股代码
    :return: 利润表核心数据
    """
    try:
        import akshare as ak
    except ImportError:
        return {"error": "请安装 akshare: pip install akshare"}

    try:
        df = ak.stock_financial_report_sina(stock=code, symbol="利润表")
        if df.empty:
            return {"error": f"未获取到 {code} 的利润表数据"}

        # 取最近4期
        df = df.head(4)

        records = []
        for _, row in df.iterrows():
            records.append({
                "report_date": str(row.get("报表日期", "")),
                "revenue": _safe_float(row.get("营业收入", 0)),
                "operating_cost": _safe_float(row.get("营业成本", 0)),
                "gross_profit": _safe_float(row.get("营业利润", 0)),
                "net_profit": _safe_float(row.get("净利润", 0)),
                "net_profit_deducted": _safe_float(row.get("扣除非经常性损益后的净利润", 0)),
            })

        return {
            "code": code,
            "type": "income_statement",
            "periods": len(records),
            "data": records
        }
    except Exception as e:
        return {"error": f"获取利润表失败: {str(e)}"}


def fetch_balance_sheet(code: str) -> dict:
    """
    获取资产负债表数据

    :param code: A股代码
    :return: 资产负债表核心数据
    """
    try:
        import akshare as ak
    except ImportError:
        return {"error": "请安装 akshare: pip install akshare"}

    try:
        df = ak.stock_financial_report_sina(stock=code, symbol="资产负债表")
        if df.empty:
            return {"error": f"未获取到 {code} 的资产负债表数据"}

        df = df.head(4)

        records = []
        for _, row in df.iterrows():
            total_assets = _safe_float(row.get("资产总计", 0))
            total_liabilities = _safe_float(row.get("负债合计", 0))
            equity = _safe_float(row.get("所有者权益(或股东权益)合计", 0))

            records.append({
                "report_date": str(row.get("报表日期", "")),
                "total_assets": total_assets,
                "total_liabilities": total_liabilities,
                "total_equity": equity,
                "debt_ratio": round(total_liabilities / total_assets * 100, 2) if total_assets else 0,
                "accounts_receivable": _safe_float(row.get("应收账款", 0)),
                "inventory": _safe_float(row.get("存货", 0)),
                "goodwill": _safe_float(row.get("商誉", 0)),
                "cash_and_equivalents": _safe_float(row.get("货币资金", 0)),
                "current_assets": _safe_float(row.get("流动资产合计", 0)),
                "current_liabilities": _safe_float(row.get("流动负债合计", 0)),
            })

        return {
            "code": code,
            "type": "balance_sheet",
            "periods": len(records),
            "data": records
        }
    except Exception as e:
        return {"error": f"获取资产负债表失败: {str(e)}"}


def fetch_cashflow_statement(code: str) -> dict:
    """
    获取现金流量表数据

    :param code: A股代码
    :return: 现金流量表核心数据
    """
    try:
        import akshare as ak
    except ImportError:
        return {"error": "请安装 akshare: pip install akshare"}

    try:
        df = ak.stock_financial_report_sina(stock=code, symbol="现金流量表")
        if df.empty:
            return {"error": f"未获取到 {code} 的现金流量表数据"}

        df = df.head(4)

        records = []
        for _, row in df.iterrows():
            ocf = _safe_float(row.get("经营活动产生的现金流量净额", 0))
            icf = _safe_float(row.get("投资活动产生的现金流量净额", 0))
            fcf_val = _safe_float(row.get("融资活动产生的现金流量净额", 0))
            capex = _safe_float(row.get("购建固定资产、无形资产和其他长期资产支付的现金", 0))

            records.append({
                "report_date": str(row.get("报表日期", "")),
                "operating_cashflow": ocf,
                "investing_cashflow": icf,
                "financing_cashflow": fcf_val,
                "capex": capex,
                "free_cashflow": round(ocf - abs(capex), 2) if ocf and capex else 0,
            })

        return {
            "code": code,
            "type": "cashflow_statement",
            "periods": len(records),
            "data": records
        }
    except Exception as e:
        return {"error": f"获取现金流量表失败: {str(e)}"}


def fetch_financial_indicators(code: str) -> dict:
    """
    获取核心财务指标

    :param code: A股代码
    :return: 关键财务比率
    """
    try:
        import akshare as ak
    except ImportError:
        return {"error": "请安装 akshare: pip install akshare"}

    try:
        df = ak.stock_financial_analysis_indicator(symbol=code)
        if df.empty:
            return {"error": f"未获取到 {code} 的财务指标数据"}

        df = df.head(4)

        records = []
        for _, row in df.iterrows():
            records.append({
                "report_date": str(row.get("日期", "")),
                "roe": _safe_float(row.get("净资产收益率(%)", 0)),
                "roa": _safe_float(row.get("总资产利润率(%)", 0)),
                "gross_margin": _safe_float(row.get("销售毛利率(%)", 0)),
                "net_margin": _safe_float(row.get("销售净利率(%)", 0)),
                "current_ratio": _safe_float(row.get("流动比率", 0)),
                "quick_ratio": _safe_float(row.get("速动比率", 0)),
                "debt_to_asset": _safe_float(row.get("资产负债率(%)", 0)),
                "inventory_turnover": _safe_float(row.get("存货周转率(次)", 0)),
                "receivable_turnover": _safe_float(row.get("应收账款周转率(次)", 0)),
                "eps": _safe_float(row.get("基本每股收益", 0)),
            })

        return {
            "code": code,
            "type": "financial_indicators",
            "periods": len(records),
            "data": records
        }
    except Exception as e:
        return {"error": f"获取财务指标失败: {str(e)}"}


def calc_dupont_analysis(code: str) -> dict:
    """
    杜邦分析 — 计算ROE分解

    :param code: A股代码
    :return: 杜邦分析结果
    """
    try:
        import akshare as ak
    except ImportError:
        return {"error": "请安装 akshare: pip install akshare"}

    try:
        # 获取财务指标
        indicators = ak.stock_financial_analysis_indicator(symbol=code)
        if indicators.empty:
            return {"error": "无法获取财务指标"}

        latest = indicators.iloc[0]

        roe = _safe_float(latest.get("净资产收益率(%)", 0))
        net_margin = _safe_float(latest.get("销售净利率(%)", 0))

        # 尝试获取资产周转率和权益乘数
        # 通过 ROE = 净利率 × 资产周转率 × 权益乘数 来推算
        debt_ratio = _safe_float(latest.get("资产负债率(%)", 0))
        equity_multiplier = round(1 / (1 - debt_ratio / 100), 2) if debt_ratio < 100 else 0

        # 资产周转率 = ROE / (净利率 × 权益乘数)
        if net_margin and equity_multiplier:
            asset_turnover = round(roe / (net_margin * equity_multiplier) * 100, 2) / 100
        else:
            asset_turnover = 0

        # 判断杜邦模式
        if net_margin > 15:
            dupont_type = "A型(高利润率驱动)"
        elif asset_turnover > 1.5:
            dupont_type = "B型(高周转驱动)"
        elif equity_multiplier > 3:
            dupont_type = "C型(高杠杆驱动)"
        else:
            dupont_type = "混合型"

        return {
            "code": code,
            "type": "dupont_analysis",
            "report_date": str(latest.get("日期", "")),
            "roe": roe,
            "net_margin": net_margin,
            "asset_turnover": asset_turnover,
            "equity_multiplier": equity_multiplier,
            "debt_ratio": debt_ratio,
            "dupont_type": dupont_type,
            "verification": round(net_margin / 100 * asset_turnover * equity_multiplier * 100, 2),
            "note": "ROE = 净利率 × 资产周转率 × 权益乘数"
        }
    except Exception as e:
        return {"error": f"杜邦分析失败: {str(e)}"}


def _safe_float(val, default=0.0) -> float:
    """安全转换为浮点数"""
    try:
        if pd.isna(val):
            return default
        return round(float(val), 4)
    except (ValueError, TypeError):
        return default


def main():
    """主函数 — 命令行入口"""
    parser = argparse.ArgumentParser(description="FinMind 财务数据获取")
    parser.add_argument("--code", required=True, help="A股代码，如 600519")
    parser.add_argument("--type", required=True,
                        choices=["income", "balance", "cashflow", "indicators", "dupont", "all"],
                        help="数据类型")
    parser.add_argument("--output", default="json", choices=["json", "csv"],
                        help="输出格式")

    args = parser.parse_args()

    results = {}

    if args.type in ("income", "all"):
        results["income"] = fetch_income_statement(args.code)
    if args.type in ("balance", "all"):
        results["balance"] = fetch_balance_sheet(args.code)
    if args.type in ("cashflow", "all"):
        results["cashflow"] = fetch_cashflow_statement(args.code)
    if args.type in ("indicators", "all"):
        results["indicators"] = fetch_financial_indicators(args.code)
    if args.type in ("dupont", "all"):
        results["dupont"] = calc_dupont_analysis(args.code)

    # 单类型直接输出数据
    if args.type != "all" and args.type in results:
        results = results[args.type]

    if args.output == "csv" and isinstance(results, dict) and "data" in results:
        df = pd.DataFrame(results["data"])
        csv_file = f"{args.code}_financials_{args.type}.csv"
        df.to_csv(csv_file, index=False, encoding="utf-8-sig")
        print(f"已保存到 {csv_file}")
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
