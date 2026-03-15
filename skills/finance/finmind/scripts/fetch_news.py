#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FinMind 新闻与舆情数据获取脚本
路径B: 本地Python脚本 — 使用 akshare + 网页抓取获取新闻、公告、研报信息

使用方式:
    python fetch_news.py --code 600519 --type news --days 7
    python fetch_news.py --code 600519 --type announcement --days 30
    python fetch_news.py --code 600519 --type research --days 30
    python fetch_news.py --type hot --days 1
    python fetch_news.py --type sentiment

依赖安装:
    pip install akshare pandas

@author sevenxiao
"""

import argparse
import json
from datetime import datetime, timedelta

import pandas as pd


def fetch_stock_news(code: str, days: int = 7) -> dict:
    """
    获取个股新闻资讯

    :param code: 股票代码
    :param days: 最近N天
    :return: 新闻列表
    """
    try:
        import akshare as ak
    except ImportError:
        return {"error": "请安装 akshare: pip install akshare"}

    try:
        df = ak.stock_news_em(symbol=code)
        if df.empty:
            return {"error": f"未获取到 {code} 的新闻数据"}

        # 过滤时间范围
        cutoff = datetime.now() - timedelta(days=days)
        df["发布时间"] = pd.to_datetime(df["发布时间"])
        df = df[df["发布时间"] >= cutoff]

        records = []
        for _, row in df.head(20).iterrows():
            records.append({
                "title": str(row.get("新闻标题", "")),
                "source": str(row.get("新闻来源", "")),
                "time": str(row.get("发布时间", "")),
                "url": str(row.get("新闻链接", "")),
                "content": str(row.get("新闻内容", ""))[:200],  # 截取前200字
            })

        return {
            "code": code,
            "type": "stock_news",
            "days": days,
            "count": len(records),
            "data": records
        }
    except Exception as e:
        return {"error": f"获取新闻失败: {str(e)}"}


def fetch_stock_announcement(code: str, days: int = 30) -> dict:
    """
    获取公司公告

    :param code: 股票代码
    :param days: 最近N天
    :return: 公告列表
    """
    try:
        import akshare as ak
    except ImportError:
        return {"error": "请安装 akshare: pip install akshare"}

    try:
        # 东方财富公告
        df = ak.stock_notice_report(symbol=code)
        if df is None or df.empty:
            return {"code": code, "type": "announcements", "count": 0, "data": []}

        records = []
        for _, row in df.head(15).iterrows():
            records.append({
                "title": str(row.get("公告标题", row.get("标题", ""))),
                "date": str(row.get("公告日期", row.get("日期", ""))),
                "type": str(row.get("公告类型", "")),
            })

        return {
            "code": code,
            "type": "announcements",
            "count": len(records),
            "data": records
        }
    except Exception as e:
        return {"error": f"获取公告失败: {str(e)}"}


def fetch_research_reports(code: str, days: int = 30) -> dict:
    """
    获取券商研报摘要

    :param code: 股票代码
    :param days: 最近N天
    :return: 研报列表
    """
    try:
        import akshare as ak
    except ImportError:
        return {"error": "请安装 akshare: pip install akshare"}

    try:
        df = ak.stock_analyst_detail_em(symbol=code)
        if df is None or df.empty:
            return {"code": code, "type": "research_reports", "count": 0, "data": []}

        records = []
        for _, row in df.head(10).iterrows():
            records.append({
                "title": str(row.get("报告名称", "")),
                "institution": str(row.get("机构名称", "")),
                "analyst": str(row.get("分析师", "")),
                "date": str(row.get("报告日期", "")),
                "rating": str(row.get("最新评级", "")),
                "target_price": str(row.get("目标价", "")),
            })

        return {
            "code": code,
            "type": "research_reports",
            "count": len(records),
            "data": records
        }
    except Exception as e:
        return {"error": f"获取研报失败: {str(e)}"}


def fetch_hot_topics(days: int = 1) -> dict:
    """
    获取市场热点话题

    :param days: 最近N天
    :return: 热点列表
    """
    try:
        import akshare as ak
    except ImportError:
        return {"error": "请安装 akshare: pip install akshare"}

    results = {}

    try:
        # 热门板块
        sector_df = ak.stock_board_concept_name_em()
        if sector_df is not None and not sector_df.empty:
            top_sectors = []
            sorted_df = sector_df.sort_values("涨跌幅", ascending=False).head(10)
            for _, row in sorted_df.iterrows():
                top_sectors.append({
                    "name": str(row.get("板块名称", "")),
                    "change_pct": float(row.get("涨跌幅", 0)),
                    "leader": str(row.get("领涨股票", "")),
                })
            results["hot_sectors"] = top_sectors
    except Exception as e:
        results["hot_sectors_error"] = str(e)

    try:
        # 涨停股
        limit_up_df = ak.stock_zt_pool_em(date=datetime.now().strftime("%Y%m%d"))
        if limit_up_df is not None and not limit_up_df.empty:
            limit_ups = []
            for _, row in limit_up_df.head(10).iterrows():
                limit_ups.append({
                    "code": str(row.get("代码", "")),
                    "name": str(row.get("名称", "")),
                    "reason": str(row.get("涨停原因", "")),
                    "first_time": str(row.get("首次涨停时间", "")),
                })
            results["limit_up_stocks"] = limit_ups
    except Exception as e:
        results["limit_up_error"] = str(e)

    return {
        "type": "hot_topics",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "data": results
    }


def fetch_market_sentiment() -> dict:
    """
    获取市场情绪指标（拼合多源数据）

    :return: 情绪指标汇总
    """
    try:
        import akshare as ak
    except ImportError:
        return {"error": "请安装 akshare: pip install akshare"}

    sentiment = {}

    # 融资融券余额
    try:
        margin_df = ak.stock_margin_sz_sh_total()
        if margin_df is not None and not margin_df.empty:
            latest = margin_df.iloc[-1]
            sentiment["margin_balance"] = {
                "date": str(latest.get("日期", "")),
                "balance": float(latest.get("融资余额", 0)),
                "unit": "亿元"
            }
    except Exception as e:
        sentiment["margin_error"] = str(e)

    # 北向资金
    try:
        north_df = ak.stock_hsgt_north_net_flow_in_em(symbol="北上")
        if north_df is not None and not north_df.empty:
            recent = north_df.tail(5)
            flows = []
            for _, row in recent.iterrows():
                flows.append({
                    "date": str(row.get("日期", "")),
                    "net_flow": float(row.get("当日净流入", 0)),
                })
            sentiment["northbound"] = {
                "recent_5d": flows,
                "total_5d": round(sum(f["net_flow"] for f in flows), 2),
                "unit": "亿元"
            }
    except Exception as e:
        sentiment["northbound_error"] = str(e)

    # 两市成交额
    try:
        vol_df = ak.stock_zh_a_hist(symbol="000001", period="daily",
                                     start_date=(datetime.now() - timedelta(days=10)).strftime("%Y%m%d"),
                                     end_date=datetime.now().strftime("%Y%m%d"))
        if vol_df is not None and not vol_df.empty:
            sentiment["market_volume_proxy"] = {
                "note": "上证指数近期成交额(亿)",
                "latest": float(vol_df.iloc[-1].get("成交额", 0)) / 1e8,
            }
    except Exception as e:
        sentiment["volume_error"] = str(e)

    return {
        "type": "market_sentiment",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "data": sentiment
    }


def main():
    """主函数 — 命令行入口"""
    parser = argparse.ArgumentParser(description="FinMind 新闻与舆情数据获取")
    parser.add_argument("--code", default="", help="股票代码（热点和情绪模式可省略）")
    parser.add_argument("--type", required=True,
                        choices=["news", "announcement", "research", "hot", "sentiment"],
                        help="数据类型: news/announcement/research/hot/sentiment")
    parser.add_argument("--days", type=int, default=7, help="时间范围(天)")

    args = parser.parse_args()

    if args.type == "news":
        if not args.code:
            print(json.dumps({"error": "news模式需要指定--code"}, ensure_ascii=False))
            return
        result = fetch_stock_news(args.code, args.days)
    elif args.type == "announcement":
        if not args.code:
            print(json.dumps({"error": "announcement模式需要指定--code"}, ensure_ascii=False))
            return
        result = fetch_stock_announcement(args.code, args.days)
    elif args.type == "research":
        if not args.code:
            print(json.dumps({"error": "research模式需要指定--code"}, ensure_ascii=False))
            return
        result = fetch_research_reports(args.code, args.days)
    elif args.type == "hot":
        result = fetch_hot_topics(args.days)
    elif args.type == "sentiment":
        result = fetch_market_sentiment()
    else:
        result = {"error": f"不支持的类型: {args.type}"}

    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
