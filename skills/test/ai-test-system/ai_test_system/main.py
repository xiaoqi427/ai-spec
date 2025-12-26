import argparse

from .config_loader import load_config
from .pipeline import AiTestPipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Test System")
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="配置文件路径",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    pipeline = AiTestPipeline(config)
    pipeline.run_all_cases()


if __name__ == "__main__":
    main()
