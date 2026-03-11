"""主入口：命令行启动 submitValidate 批量测试"""
from __future__ import annotations

import argparse
import logging
import os
import sys


def setup_logging(level: str, log_file: str, console_output: bool = True):
    """配置日志系统"""
    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    handlers = []

    # 文件 Handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    handlers.append(file_handler)

    # 控制台 Handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s",
                datefmt="%H:%M:%S",
            )
        )
        # 控制台默认只输出 WARNING 以上级别，避免干扰测试进度输出
        console_handler.setLevel(logging.WARNING)
        handlers.append(console_handler)

    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        handlers=handlers,
    )


def main():
    parser = argparse.ArgumentParser(
        description="submitValidate 接口批量测试工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 使用默认配置文件运行
  python -m ai_intf_test.main

  # 指定配置文件
  python -m ai_intf_test.main --config config/config.yaml

  # 直接指定输入 Excel（覆盖配置文件中的设置）
  python -m ai_intf_test.main --input ./excel/my_test.xlsx

  # 指定服务器地址（覆盖配置文件中的设置）
  python -m ai_intf_test.main --base-url http://10.60.137.24:8080

  # 指定登录用户名和密码
  python -m ai_intf_test.main --usernum fsscadmin --password 2
        """,
    )

    parser.add_argument(
        "--config", "-c",
        type=str,
        default="config/config.yaml",
        help="配置文件路径（默认: config/config.yaml）",
    )
    parser.add_argument(
        "--input", "-i",
        type=str,
        default=None,
        help="输入 Excel 文件路径（覆盖配置文件中的 excel.input_path）",
    )
    parser.add_argument(
        "--base-url", "-u",
        type=str,
        default=None,
        help="目标服务器地址（覆盖配置文件中的 server.base_url）",
    )
    parser.add_argument(
        "--token", "-t",
        type=str,
        default=None,
        help="Bearer Token（覆盖配置文件中的 auth.token）",
    )
    parser.add_argument(
        "--concurrent",
        action="store_true",
        default=None,
        help="启用并发模式",
    )
    parser.add_argument(
        "--workers", "-w",
        type=int,
        default=None,
        help="并发工作线程数",
    )
    parser.add_argument(
        "--usernum",
        type=str,
        default=None,
        help="登录用户名（覆盖配置文件中的 login.usernum）",
    )
    parser.add_argument(
        "--password", "-p",
        type=str,
        default=None,
        help="登录密码（覆盖配置文件中的 login.password）",
    )
    parser.add_argument(
        "--login-url",
        type=str,
        default=None,
        help="登录接口 URL（覆盖配置文件中的 login.url）",
    )

    args = parser.parse_args()

    # 加载配置
    from .config_loader import load_config
    config = load_config(args.config)

    # 命令行参数覆盖
    if args.input:
        config.excel.input_path = args.input
    if args.base_url:
        config.server.base_url = args.base_url.rstrip("/")
    if args.token:
        config.auth.type = "token"
        config.auth.token = args.token
    if args.concurrent:
        config.concurrency.enabled = True
    if args.workers:
        config.concurrency.max_workers = args.workers
        config.concurrency.enabled = True
    if args.usernum:
        config.login.usernum = args.usernum
        config.login.enabled = True
        config.auth.type = "login"
    if args.password:
        config.login.password = args.password
    if args.login_url:
        config.login.url = args.login_url
        config.login.enabled = True
        config.auth.type = "login"

    # 初始化日志
    setup_logging(
        level=config.log.level,
        log_file=config.log.log_file,
        console_output=config.log.console_output,
    )

    # 运行测试
    from .pipeline import TestPipeline
    pipeline = TestPipeline(config)
    pipeline.run()


if __name__ == "__main__":
    main()
