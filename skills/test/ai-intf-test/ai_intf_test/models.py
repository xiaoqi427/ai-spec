"""数据模型定义"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class TestInput:
    """从 Excel 读取的单条测试输入"""
    claim_id: int
    item_id: str
    row_index: int  # Excel 中的行号（用于回写）


@dataclass
class ValidateResult:
    """单条校验结果项"""
    name: str
    message: str
    severity: str  # PASS / ERROR / WARNING
    args: Optional[List[Any]] = None


@dataclass
class TestResult:
    """单条测试完整结果"""
    claim_id: int
    item_id: str
    url: str
    service_type: str = ""  # 路由到的服务类型（如 eer、ptp、otc、claim）
    status_code: int = 0
    success: bool = False
    passed: bool = False
    results: List[ValidateResult] = field(default_factory=list)
    error: Optional[str] = None
    trace_id: Optional[str] = None
    test_time: str = ""
    response_time_ms: int = 0
    raw_response: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if not self.test_time:
            self.test_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def results_summary(self) -> str:
        """校验结果摘要"""
        if not self.results:
            return ""
        parts = []
        for r in self.results:
            parts.append(f"[{r.severity}] {r.name}: {r.message}")
        return "\n".join(parts)

    @property
    def error_results(self) -> List[ValidateResult]:
        """获取所有 ERROR 级别的校验结果"""
        return [r for r in self.results if r.severity == "ERROR"]

    @property
    def warning_results(self) -> List[ValidateResult]:
        """获取所有 WARNING 级别的校验结果"""
        return [r for r in self.results if r.severity == "WARNING"]
