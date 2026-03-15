#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FinMind 行情数据获取脚本
路径B: 本地Python脚本 — 使用 akshare(A股) + yfinance(美股/港股)

使用方式:
    python fetch_market_data.py --code 600519 --market A --period daily --days 120
    python fetch_market_data.py --code AAPL --market US --period daily --days 60
    python fetch_market_data.py --code 00700 --market HK --period daily --days 90

依赖安装:
    pip install akshare yfinance pandas

@author sevenxiao
"""

import argparse
import json
import sys
from datetime import datetime, timedelta

import pandas as pd


def fetch_a_share(code: str, period: str = "daily", days: int = 120) -> dict:
    """
    获取A股行情数据 (使用 AKShare)

    :param code: 股票代码，如 600519、000858
    :param period: 周期 daily/weekly/monthly
    :param days: 获取最近N天数据
    :return: 标准化行情数据字典
    """
    try:
        import akshare as ak
    except ImportError:
        return {"error": "请安装 akshare: pip install akshare"}

    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")

    try:
        # 根据周期选择接口
        if period == "daily":
            df = ak.stock_zh_a_hist(
                symbol=code,
                period="daily",
                start_date=start_date,
                end_date=end_date,
                adjust="qfq"  # 前复权
            )
        elif period == "weekly":
            df = ak.stock_zh_a_hist(
                symbol=code,
                period="weekly",
                start_date=start_date,
                end_date=end_date,
                adjust="qfq"
            )
        elif period == "monthly":
            df = ak.stock_zh_a_hist(
                symbol=code,
                period="monthly",
                start_date=start_date,
                end_date=end_date,
                adjust="qfq"
            )
        else:
            return {"error": f"不支持的周期: {period}"}

        # 标准化列名
        column_map = {
            "日期": "date",
            "开盘": "open",
            "收盘": "close",
            "最高": "high",
            "最低": "low",
            "成交量": "volume",
            "成交额": "amount",
            "振幅": "amplitude",
            "涨跌幅": "change_pct",
            "涨跌额": "change_amt",
            "换手率": "turnover_rate"
        }
        df = df.rename(columns=column_map)
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

        # 计算技术指标
        df = _calc_technical_indicators(df)

        return {
            "code": code,
            "market": "A",
            "period": period,
            "count": len(df),
            "latest": {
                "date": df.iloc[-1]["date"],
                "close": float(df.iloc[-1]["close"]),
                "change_pct": float(df.iloc[-1].get("change_pct", 0)),
                "volume": int(df.iloc[-1]["volume"]),
            },
            "data": df.to_dict(orient="records")
        }
    except Exception as e:
        return {"error": f"获取A股数据失败: {str(e)}"}


def fetch_us_hk_share(code: str, market: str = "US", period: str = "daily", days: int = 120) -> dict:
    """
    获取美股/港股行情数据 (使用 yfinance)

    :param code: 股票代码，美股如 AAPL，港股如 0700.HK
    :param market: 市场 US/HK
    :param period: 周期 daily/weekly/monthly
    :param days: 获取最近N天数据
    :return: 标准化行情数据字典
    """
    try:
        import yfinance as yf
    except ImportError:
        return {"error": "请安装 yfinance: pip install yfinance"}

    # 港股代码转换
    ticker = code
    if market == "HK":
        ticker = f"{code.zfill(4)}.HK"

    try:
        stock = yf.Ticker(ticker)
        interval_map = {"daily": "1d", "weekly": "1wk", "monthly": "1mo"}
        interval = interval_map.get(period, "1d")

        df = stock.history(period=f"{days}d", interval=interval)

        if df.empty:
            return {"error": f"未获取到 {ticker} 的数据"}

        # 标准化
        df = df.reset_index()
        df = df.rename(columns={
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        })
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
        df["amount"] = df["open"] * df["volume"]  # 近似成交额
        df["change_pct"] = df["close"].pct_change() * 100

        # 只保留需要的列
        cols = ["date", "open", "high", "low", "close", "volume", "amount", "change_pct"]
        df = df[[c for c in cols if c in df.columns]]

        # 计算技术指标
        df = _calc_technical_indicators(df)

        return {
            "code": code,
            "market": market,
            "period": period,
            "count": len(df),
            "latest": {
                "date": df.iloc[-1]["date"],
                "close": float(df.iloc[-1]["close"]),
                "change_pct": float(df.iloc[-1].get("change_pct", 0)),
                "volume": int(df.iloc[-1]["volume"]),
            },
            "data": df.to_dict(orient="records")
        }
    except Exception as e:
        return {"error": f"获取{market}数据失败: {str(e)}"}


def _calc_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    计算基础技术指标

    :param df: 包含 OHLCV 的 DataFrame
    :return: 增加了技术指标列的 DataFrame
    """
    if "close" not in df.columns:
        return df

    # 均线
    df["ma5"] = df["close"].rolling(5).mean().round(2)
    df["ma10"] = df["close"].rolling(10).mean().round(2)
    df["ma20"] = df["close"].rolling(20).mean().round(2)
    df["ma60"] = df["close"].rolling(60).mean().round(2)

    # 布林带
    df["boll_mid"] = df["ma20"]
    std20 = df["close"].rolling(20).std()
    df["boll_upper"] = (df["boll_mid"] + 2 * std20).round(2)
    df["boll_lower"] = (df["boll_mid"] - 2 * std20).round(2)

    # 成交量均线
    if "volume" in df.columns:
        df["vol_ma5"] = df["volume"].rolling(5).mean().round(0)
        df["vol_ma20"] = df["volume"].rolling(20).mean().round(0)

    # ATR(14)
    if all(c in df.columns for c in ["high", "low", "close"]):
        prev_close = df["close"].shift(1)
        tr = pd.concat([
            df["high"] - df["low"],
            (df["high"] - prev_close).abs(),
            (df["low"] - prev_close).abs()
        ], axis=1).max(axis=1)
        df["atr14"] = tr.rolling(14).mean().round(2)

    return df


def fetch_index_data(index_code: str = "000300", days: int = 30) -> dict:
    """
    获取指数行情数据（沪深300、上证指数等）

    :param index_code: 指数代码 000300(沪深300) / 000001(上证指数) / 399006(创业板指)
    :param days: 天数
    :return: 标准化数据
    """
    try:
        import akshare as ak
    except ImportError:
        return {"error": "请安装 akshare: pip install akshare"}

    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")

    try:
        df = ak.stock_zh_index_daily(symbol=f"sh{index_code}")
        df = df[df["date"] >= start_date]

        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
        df["change_pct"] = df["close"].pct_change() * 100

        return {
            "code": index_code,
            "market": "INDEX",
            "count": len(df),
            "latest": {
                "date": df.iloc[-1]["date"],
                "close": float(df.iloc[-1]["close"]),
                "change_pct": float(df.iloc[-1].get("change_pct", 0)),
            },
            "data": df.to_dict(orient="records")
        }
    except Exception as e:
        return {"error": f"获取指数数据失败: {str(e)}"}


def main():
    """主函数 — 命令行入口"""
    parser = argparse.ArgumentParser(description="FinMind 行情数据获取")
    parser.add_argument("--code", required=True, help="股票/指数代码")
    parser.add_argument("--market", default="A", choices=["A", "US", "HK", "INDEX"],
                        help="市场: A(A股)/US(美股)/HK(港股)/INDEX(指数)")
    parser.add_argument("--period", default="daily", choices=["daily", "weekly", "monthly"],
                        help="周期: daily/weekly/monthly")
    parser.add_argument("--days", type=int, default=120, help="获取最近N天数据")
    parser.add_argument("--output", default="json", choices=["json", "csv"],
                        help="输出格式: json/csv")

    args = parser.parse_args()

    # 根据市场分发
    if args.market == "A":
        result = fetch_a_share(args.code, args.period, args.days)
    elif args.market in ("US", "HK"):
        result = fetch_us_hk_share(args.code, args.market, args.period, args.days)
    elif args.market == "INDEX":
        result = fetch_index_data(args.code, args.days)
    else:
        result = {"error": f"不支持的市场: {args.market}"}

    # 输出
    if args.output == "csv" and "data" in result:
        df = pd.DataFrame(result["data"])
        csv_file = f"{args.code}_{args.market}_{args.period}.csv"
        df.to_csv(csv_file, index=False, encoding="utf-8-sig")
        print(f"已保存到 {csv_file}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
