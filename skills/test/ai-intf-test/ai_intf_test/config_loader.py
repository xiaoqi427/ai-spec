"""配置加载模块"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import yaml


@dataclass
class ServerConfig:
    base_url: str = "http://localhost:8080"
    timeout: int = 30
    connect_timeout: int = 10


@dataclass
class LoginConfig:
    enabled: bool = False
    url: str = ""
    usernum: str = ""
    password: str = ""


@dataclass
class AuthConfig:
    type: str = "none"  # none / login / token / cookie / basic
    token: str = ""
    cookie: str = ""
    username: str = ""
    password: str = ""
    custom_headers: Dict[str, str] = field(default_factory=dict)


@dataclass
class ExcelColumnsConfig:
    claim_id: str = "claimId"
    item_id: str = "itemId"


@dataclass
class ExcelConfig:
    input_path: str = "./excel/test_input.xlsx"
    sheet_name: str = "Sheet1"
    columns: ExcelColumnsConfig = field(default_factory=ExcelColumnsConfig)


@dataclass
class OutputConfig:
    output_path: str = "./output/test_result_{timestamp}.xlsx"
    output_dir: str = "./output"


@dataclass
class UrlConfig:
    template: str = "{base_url}{service_path}/{item_id}/submitValidate"


@dataclass
class RoutingRuleConfig:
    """单条路由规则"""
    service_path: str = ""
    items: List[str] = field(default_factory=list)


@dataclass
class RoutingConfig:
    """itemId 到 service_path 的路由配置"""
    default_service_path: str = ""
    rules: Dict[str, RoutingRuleConfig] = field(default_factory=dict)

    def resolve_service_path(self, item_id: str) -> str:
        """根据 itemId 解析对应的 service_path

        匹配逻辑：itemId 包含规则中的子串则命中

        Args:
            item_id: 报账单模板ID（如 T001、T045）

        Returns:
            对应的 service_path（如 /eer、/ptp）
        """
        upper_id = item_id.strip().upper()
        for rule_name, rule in self.rules.items():
            for pattern in rule.items:
                if pattern.upper() in upper_id:
                    return rule.service_path
        return self.default_service_path

    def resolve_service_name(self, item_id: str) -> str:
        """根据 itemId 解析服务名称（如 eer、ptp、claim）"""
        upper_id = item_id.strip().upper()
        for rule_name, rule in self.rules.items():
            for pattern in rule.items:
                if pattern.upper() in upper_id:
                    return rule_name
        return "unknown"


@dataclass
class ConcurrencyConfig:
    enabled: bool = False
    max_workers: int = 3
    request_interval: float = 0.5


@dataclass
class RetryConfig:
    max_retries: int = 3
    retry_interval: float = 2.0
    retry_on_status_codes: List[int] = field(default_factory=lambda: [500, 502, 503, 504])


@dataclass
class LogConfig:
    level: str = "INFO"
    log_file: str = "./logs/submit_validate_test.log"
    console_output: bool = True


@dataclass
class AppConfig:
    server: ServerConfig = field(default_factory=ServerConfig)
    login: LoginConfig = field(default_factory=LoginConfig)
    auth: AuthConfig = field(default_factory=AuthConfig)
    excel: ExcelConfig = field(default_factory=ExcelConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
    url: UrlConfig = field(default_factory=UrlConfig)
    routing: RoutingConfig = field(default_factory=RoutingConfig)
    concurrency: ConcurrencyConfig = field(default_factory=ConcurrencyConfig)
    retry: RetryConfig = field(default_factory=RetryConfig)
    log: LogConfig = field(default_factory=LogConfig)


def _build_server_config(data: dict) -> ServerConfig:
    s = data.get("server", {})
    return ServerConfig(
        base_url=s.get("base_url", "http://localhost:8080").rstrip("/"),
        timeout=int(s.get("timeout", 30)),
        connect_timeout=int(s.get("connect_timeout", 10)),
    )


def _build_login_config(data: dict) -> LoginConfig:
    lg = data.get("login", {})
    return LoginConfig(
        enabled=bool(lg.get("enabled", False)),
        url=lg.get("url", "") or "",
        usernum=lg.get("usernum", "") or "",
        password=lg.get("password", "") or "",
    )


def _build_auth_config(data: dict) -> AuthConfig:
    a = data.get("auth", {})
    custom_headers = a.get("custom_headers", {}) or {}
    return AuthConfig(
        type=a.get("type", "none"),
        token=a.get("token", "") or "",
        cookie=a.get("cookie", "") or "",
        username=a.get("username", "") or "",
        password=a.get("password", "") or "",
        custom_headers={k: str(v) for k, v in custom_headers.items()},
    )


def _build_excel_config(data: dict) -> ExcelConfig:
    e = data.get("excel", {})
    cols = e.get("columns", {})
    return ExcelConfig(
        input_path=e.get("input_path", "./excel/test_input.xlsx"),
        sheet_name=e.get("sheet_name", "Sheet1"),
        columns=ExcelColumnsConfig(
            claim_id=cols.get("claim_id", "claimId"),
            item_id=cols.get("item_id", "itemId"),
        ),
    )


def _build_output_config(data: dict) -> OutputConfig:
    o = data.get("output", {})
    return OutputConfig(
        output_path=o.get("output_path", "./output/test_result_{timestamp}.xlsx"),
        output_dir=o.get("output_dir", "./output"),
    )


def _build_url_config(data: dict) -> UrlConfig:
    u = data.get("url", {})
    return UrlConfig(
        template=u.get("template", "{base_url}{service_path}/{item_id}/submitValidate"),
    )


def _build_routing_config(data: dict) -> RoutingConfig:
    r = data.get("routing", {})
    default_path = r.get("default_service_path", "")
    raw_rules = r.get("rules", {})
    rules = {}
    for name, rule_data in raw_rules.items():
        rules[name] = RoutingRuleConfig(
            service_path=rule_data.get("service_path", ""),
            items=rule_data.get("items", []),
        )
    return RoutingConfig(
        default_service_path=default_path,
        rules=rules,
    )


def _build_concurrency_config(data: dict) -> ConcurrencyConfig:
    c = data.get("concurrency", {})
    return ConcurrencyConfig(
        enabled=bool(c.get("enabled", False)),
        max_workers=int(c.get("max_workers", 3)),
        request_interval=float(c.get("request_interval", 0.5)),
    )


def _build_retry_config(data: dict) -> RetryConfig:
    r = data.get("retry", {})
    return RetryConfig(
        max_retries=int(r.get("max_retries", 3)),
        retry_interval=float(r.get("retry_interval", 2.0)),
        retry_on_status_codes=r.get("retry_on_status_codes", [500, 502, 503, 504]),
    )


def _build_log_config(data: dict) -> LogConfig:
    lg = data.get("log", {})
    return LogConfig(
        level=lg.get("level", "INFO"),
        log_file=lg.get("log_file", "./logs/submit_validate_test.log"),
        console_output=bool(lg.get("console_output", True)),
    )


def load_config(path: str) -> AppConfig:
    """从 YAML 文件加载配置并转换为 AppConfig"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"配置文件不存在: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    return AppConfig(
        server=_build_server_config(data),
        login=_build_login_config(data),
        auth=_build_auth_config(data),
        excel=_build_excel_config(data),
        output=_build_output_config(data),
        url=_build_url_config(data),
        routing=_build_routing_config(data),
        concurrency=_build_concurrency_config(data),
        retry=_build_retry_config(data),
        log=_build_log_config(data),
    )
