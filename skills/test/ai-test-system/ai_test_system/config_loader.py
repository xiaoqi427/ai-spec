from dataclasses import dataclass
from typing import Optional


@dataclass
class ExcelConfig:
    input_path: str
    sheet_name: str
    case_id_column: str
    description_column: str
    system_url_column: str
    extra_context_column: str
    output_image_column: str


@dataclass
class ScreenshotConfig:
    browser: str
    driver_path: str
    window_width: int
    window_height: int
    timeout_seconds: int


@dataclass
class LoginConfig:
    enabled: bool
    login_url: str
    username: str
    password: str
    username_selector: str
    password_selector: str
    submit_selector: str
    wait_after_login: int


@dataclass
class VisionModelConfig:
    provider: str
    endpoint: str
    api_key: Optional[str] = None


@dataclass
class MarkConfig:
    input_color: str
    output_color: str
    line_width: int


@dataclass
class LogConfig:
    level: str
    log_file: str


@dataclass
class AppConfig:
    excel: ExcelConfig
    screenshot: ScreenshotConfig
    login: LoginConfig
    vision_model: VisionModelConfig
    mark: MarkConfig
    log: LogConfig


def _build_excel_config(data: dict) -> ExcelConfig:
    excel = data.get("excel", {})
    return ExcelConfig(
        input_path=excel.get("input_path", "./test_cases.xlsx"),
        sheet_name=excel.get("sheet_name", "Sheet1"),
        case_id_column=excel.get("case_id_column", "CaseID"),
        description_column=excel.get("description_column", "Description"),
        system_url_column=excel.get("system_url_column", "SystemURL"),
        extra_context_column=excel.get("extra_context_column", "ExtraContext"),
        output_image_column=excel.get("output_image_column", "ScreenshotPath"),
    )


def _build_screenshot_config(data: dict) -> ScreenshotConfig:
    screenshot = data.get("screenshot", {})
    return ScreenshotConfig(
        browser=screenshot.get("browser", "chrome"),
        driver_path=screenshot.get("driver_path", "./drivers/chromedriver"),
        window_width=int(screenshot.get("window_width", 1920)),
        window_height=int(screenshot.get("window_height", 1080)),
        timeout_seconds=int(screenshot.get("timeout_seconds", 20)),
    )


def _build_login_config(data: dict) -> LoginConfig:
    login = data.get("login", {})
    return LoginConfig(
        enabled=bool(login.get("enabled", False)),
        login_url=login.get("login_url", ""),
        username=login.get("username", ""),
        password=login.get("password", ""),
        username_selector=login.get("username_selector", "input[name='username']"),
        password_selector=login.get("password_selector", "input[name='password']"),
        submit_selector=login.get("submit_selector", "button[type='submit']"),
        wait_after_login=int(login.get("wait_after_login", 3)),
    )


def _build_vision_model_config(data: dict) -> VisionModelConfig:
    vm = data.get("vision_model", {})
    return VisionModelConfig(
        provider=vm.get("provider", "aliyun_open_source"),
        endpoint=vm.get("endpoint", "http://localhost:8000/predict"),
        api_key=vm.get("api_key") or None,
    )


def _build_mark_config(data: dict) -> MarkConfig:
    mark = data.get("mark", {})
    return MarkConfig(
        input_color=mark.get("input_color", "red"),
        output_color=mark.get("output_color", "green"),
        line_width=int(mark.get("line_width", 3)),
    )


def _build_log_config(data: dict) -> LogConfig:
    log = data.get("log", {})
    return LogConfig(
        level=log.get("level", "INFO"),
        log_file=log.get("log_file", "./logs/ai_test_system.log"),
    )


def load_config(path: str) -> AppConfig:
    """从 YAML 文件加载配置并转换为 AppConfig。"""

    import os

    import yaml

    if not os.path.exists(path):
        raise FileNotFoundError(f"配置文件不存在: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    excel_cfg = _build_excel_config(data)
    screenshot_cfg = _build_screenshot_config(data)
    login_cfg = _build_login_config(data)
    vm_cfg = _build_vision_model_config(data)
    mark_cfg = _build_mark_config(data)
    log_cfg = _build_log_config(data)

    return AppConfig(
        excel=excel_cfg,
        screenshot=screenshot_cfg,
        login=login_cfg,
        vision_model=vm_cfg,
        mark=mark_cfg,
        log=log_cfg,
    )
