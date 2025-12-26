from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class BoundingBox:
    """通用矩形框坐标，左上角 (x1, y1)，右下角 (x2, y2)。"""

    x1: int
    y1: int
    x2: int
    y2: int


@dataclass
class ParameterRegion:
    """参数区域（可作为输入或输出）。"""

    name: str
    role: str  # "input" 或 "output"
    box: BoundingBox


@dataclass
class TestCase:
    """从 Excel 行解析出的测试用例信息。"""

    case_id: str
    description: str
    system_url: str
    extra_context: Optional[str] = None
    screenshot_path: Optional[str] = None
    parameter_regions: List[ParameterRegion] = field(default_factory=list)


@dataclass
class ModelRequest:
    """发送给视觉模型的请求结构。"""

    image_path: str
    prompt: str


@dataclass
class ModelResponse:
    """视觉模型返回结构（简化版）。"""

    input_regions: List[BoundingBox]
    output_regions: List[BoundingBox]
