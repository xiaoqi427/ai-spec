#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FinMind 宏观经济数据获取脚本
路径B: 本地Python脚本 — 使用 akshare 获取宏观经济指标，支撑康波周期分析

使用方式:
    python fetch_macro_data.py --type gdp
    python fetch_macro_data.py --type cpi
    python fetch_macro_data.py --type pmi
    python fetch_macro_data.py --type money_supply
    python fetch_macro_data.py --type social_finance
    python fetch_macro_data.py --type bond_yield
    python fetch_macro_data.py --type all
    python fetch_macro_data.py --type us_treasury

依赖安装:
    pip install akshare pandas

@author sevenxiao
"""

import argparse
import json
from datetime import datetime

import pandas as pd


def fetch_gdp_data() -> dict:
    """
    获取中国GDP数据

    :return: GDP季度数据
    """
    try:
        import akshare as ak
    except ImportError:
        return {"error": "请安装 akshare: pip install akshare"}

    try:
        df = ak.macro_china_gdp()
        if df.empty:
            return {"error": "未获取到GDP数据"}

        records = []
        for _, row in df.head(8).iterrows():
            records.append({
                "quarter": str(row.get("季度", "")),
                "gdp": _safe_float(row.get("国内生产总值-绝对值", row.get("国内生产总值-累计值", 0))),
                "gdp_yoy": _safe_float(row.get("国内生产总值-同比增长", 0)),
                "primary_yoy": _safe_float(row.get("第一产业-同比增长", 0)),
                "secondary_yoy": _safe_float(row.get("第二产业-同比增长", 0)),
                "tertiary_yoy": _safe_float(row.get("第三产业-同比增长", 0)),
            })

        return {
            "type": "gdp",
            "unit": "亿元",
            "periods": len(records),
            "data": records
        }
    except Exception as e:
        return {"error": f"获取GDP数据失败: {str(e)}"}


def fetch_cpi_data() -> dict:
    """
    获取CPI数据

    :return: CPI月度数据
    """
    try:
        import akshare as ak
    except ImportError:
        return {"error": "请安装 akshare: pip install akshare"}

    try:
        df = ak.macro_china_cpi()
        if df.empty:
            return {"error": "未获取到CPI数据"}

        records = []
        for _, row in df.head(12).iterrows():
            records.append({
                "month": str(row.get("月份", row.get("日期", ""))),
                "cpi_yoy": _safe_float(row.get("全国-同比", row.get("今值", 0))),
                "cpi_mom": _safe_float(row.get("全国-环比", 0)),
            })

        return {
            "type": "cpi",
            "unit": "%",
            "periods": len(records),
            "data": records
        }
    except Exception as e:
        return {"error": f"获取CPI数据失败: {str(e)}"}


def fetch_pmi_data() -> dict:
    """
    获取PMI数据

    :return: PMI月度数据
    """
    try:
        import akshare as ak
    except ImportError:
        return {"error": "请安装 akshare: pip install akshare"}

    try:
        df = ak.macro_china_pmi()
        if df.empty:
            return {"error": "未获取到PMI数据"}

        records = []
        for _, row in df.head(12).iterrows():
            records.append({
                "month": str(row.get("月份", row.get("日期", ""))),
                "pmi_manufacturing": _safe_float(row.get("制造业-指数", row.get("制造业PMI", 0))),
                "pmi_non_manufacturing": _safe_float(row.get("非制造业-指数", row.get("非制造业PMI", 0))),
            })

        return {
            "type": "pmi",
            "threshold": 50,
            "note": ">50扩张, <50收缩",
            "periods": len(records),
            "data": records
        }
    except Exception as e:
        return {"error": f"获取PMI数据失败: {str(e)}"}


def fetch_money_supply() -> dict:
    """
    获取货币供应量数据(M0/M1/M2)

    :return: 货币供应月度数据
    """
    try:
        import akshare as ak
    except ImportError:
        return {"error": "请安装 akshare: pip install akshare"}

    try:
        df = ak.macro_china_money_supply()
        if df.empty:
            return {"error": "未获取到货币供应数据"}

        records = []
        for _, row in df.head(12).iterrows():
            records.append({
                "month": str(row.get("月份", "")),
                "m0": _safe_float(row.get("M0-数量", 0)),
                "m0_yoy": _safe_float(row.get("M0-同比", 0)),
                "m1": _safe_float(row.get("M1-数量", 0)),
                "m1_yoy": _safe_float(row.get("M1-同比", 0)),
                "m2": _safe_float(row.get("M2-数量", 0)),
                "m2_yoy": _safe_float(row.get("M2-同比", 0)),
            })

        return {
            "type": "money_supply",
            "unit": "亿元 / %",
            "periods": len(records),
            "data": records,
            "analysis_hint": "M1-M2剪刀差: M1增速>M2→资金活化(利好股市); M1<M2→资金沉淀(利空)"
        }
    except Exception as e:
        return {"error": f"获取货币供应数据失败: {str(e)}"}


def fetch_social_finance() -> dict:
    """
    获取社会融资规模数据

    :return: 社融月度数据
    """
    try:
        import akshare as ak
    except ImportError:
        return {"error": "请安装 akshare: pip install akshare"}

    try:
        df = ak.macro_china_shrzgm()
        if df.empty:
            return {"error": "未获取到社融数据"}

        records = []
        for _, row in df.head(12).iterrows():
            records.append({
                "month": str(row.get("月份", row.get("日期", ""))),
                "total": _safe_float(row.get("社会融资规模增量", row.get("当月", 0))),
                "rmb_loan": _safe_float(row.get("人民币贷款", 0)),
            })

        return {
            "type": "social_finance",
            "unit": "亿元",
            "periods": len(records),
            "data": records,
            "analysis_hint": "社融是经济领先指标，社融增速拐点通常领先GDP拐点1-2个季度"
        }
    except Exception as e:
        return {"error": f"获取社融数据失败: {str(e)}"}


def fetch_bond_yield() -> dict:
    """
    获取国债收益率数据

    :return: 国债收益率
    """
    try:
        import akshare as ak
    except ImportError:
        return {"error": "请安装 akshare: pip install akshare"}

    try:
        df = ak.bond_china_yield(start_date="2024-01-01")
        if df.empty:
            return {"error": "未获取到国债收益率数据"}

        # 筛选10年期
        df_10y = df[df["曲线名称"].str.contains("10年", na=False)].tail(30)

        records = []
        for _, row in df_10y.iterrows():
            records.append({
                "date": str(row.get("日期", "")),
                "yield_10y": _safe_float(row.get("收益率", 0)),
            })

        return {
            "type": "bond_yield",
            "unit": "%",
            "periods": len(records),
            "data": records,
            "analysis_hint": "10Y国债收益率下行→宽松周期(利好成长股); 上行→紧缩周期(利好价值股)"
        }
    except Exception as e:
        return {"error": f"获取国债收益率失败: {str(e)}"}


def fetch_us_treasury_yield() -> dict:
    """
    获取美国国债收益率

    :return: 美国10Y国债收益率
    """
    try:
        import akshare as ak
    except ImportError:
        return {"error": "请安装 akshare: pip install akshare"}

    try:
        df = ak.bond_investing_global(
            country="美国",
            index_name="美国10年期国债",
            period="每日",
            start_date="20240101",
            end_date=datetime.now().strftime("%Y%m%d")
        )
        if df.empty:
            return {"error": "未获取到美国国债数据"}

        records = []
        for _, row in df.tail(30).iterrows():
            records.append({
                "date": str(row.get("日期", "")),
                "yield_10y": _safe_float(row.get("收盘", 0)),
                "change": _safe_float(row.get("涨跌幅", 0)),
            })

        return {
            "type": "us_treasury",
            "unit": "%",
            "periods": len(records),
            "data": records,
            "analysis_hint": "中美利差影响北向资金流动和人民币汇率"
        }
    except Exception as e:
        return {"error": f"获取美国国债数据失败: {str(e)}"}


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
    parser = argparse.ArgumentParser(description="FinMind 宏观经济数据获取")
    parser.add_argument("--type", required=True,
                        choices=["gdp", "cpi", "pmi", "money_supply",
                                 "social_finance", "bond_yield", "us_treasury", "all"],
                        help="数据类型")

    args = parser.parse_args()

    results = {}

    fetch_map = {
        "gdp": ("gdp", fetch_gdp_data),
        "cpi": ("cpi", fetch_cpi_data),
        "pmi": ("pmi", fetch_pmi_data),
        "money_supply": ("money_supply", fetch_money_supply),
        "social_finance": ("social_finance", fetch_social_finance),
        "bond_yield": ("bond_yield", fetch_bond_yield),
        "us_treasury": ("us_treasury", fetch_us_treasury_yield),
    }

    if args.type == "all":
        for key, (name, func) in fetch_map.items():
            print(f"正在获取 {name}...", flush=True)
            results[name] = func()
    elif args.type in fetch_map:
        name, func = fetch_map[args.type]
        results = func()
    else:
        results = {"error": f"不支持的类型: {args.type}"}

    print(json.dumps(results, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
