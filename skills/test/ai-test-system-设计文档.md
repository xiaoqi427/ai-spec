## ai-test-system 设计文档（用于生成 Python 代码）

### 一、工程概述

- **工程名称**: `ai-test-system`
- **语言与运行环境**: Python 3.10+
- **核心能力**:
  - **大模型视觉能力**: 调用阿里开源视觉 AI 模型（或兼容的 HTTP 推理服务），对页面截图进行理解，识别并定位输入参数区域和输出参数区域。
  - **Excel 测试用例管理**: 从 Excel 读取测试用例，执行后将标注后的截图写回 Excel。
  - **自动化页面截图**: 根据测试用例描述或配置，打开指定系统页面并截图。
  - **参数区域标注**: 将输入参数用红框标出，将输出参数用绿框标出，生成标注图片。

> 说明：本设计文档面向“代码生成”，结构尽量贴近代码实现，便于从本文件直接生成 Python 工程骨架。

---

### 二、工程目录结构设计

工程根目录建议结构如下：

```text
ai-test-system/
  ├── pyproject.toml / setup.py        # 依赖与打包配置（二选一，可后续补充）
  ├── requirements.txt                 # 第三方依赖
  ├── README.md                        # 使用说明
  ├── config/
  │   └── config.yaml                  # 全局配置（模型、Excel 文件路径、浏览器、超时配置等）
  ├── ai_test_system/
  │   ├── __init__.py
  │   ├── main.py                      # 主入口：命令行 / 程序入口
  │   ├── config_loader.py             # 配置加载
  │   ├── excel_io.py                  # Excel 读写
  │   ├── case_model.py                # 测试用例数据模型
  │   ├── screenshot_captor.py         # 打开系统并截图
  │   ├── vision_model_client.py       # 调用阿里视觉模型
  │   ├── locator_service.py           # 基于模型输出进行参数区域定位和分类
  │   ├── image_marker.py              # 对截图画红/绿框
  │   └── pipeline.py                  # 串联整个流程
  └── tests/
      ├── __init__.py
      └── test_basic_pipeline.py       # 基础流程测试（可后续补充）
```

---

### 三、配置设计（`config/config.yaml`）

建议通过 YAML 统一管理配置参数，示例结构如下（用于代码生成时参考）：

```yaml
excel:
  input_path: "tests/data/test_cases.xlsx"      # 读取的测试用例 Excel
  sheet_name: "Sheet1"                          # 用例所在工作表名
  output_image_column: "ScreenshotPath"        # 写回图片路径的列名

screenshot:
  browser: "chrome"                            # 支持 chrome / edge / firefox 等
  driver_path: "drivers/chromedriver"          # 浏览器驱动路径
  window_width: 1920
  window_height: 1080
  timeout_seconds: 20

vision_model:
  provider: "aliyun_open_source"               # 标记模型来源，方便扩展
  endpoint: "http://localhost:8000/predict"     # 模型服务 HTTP 地址
  api_key: ""                                  # 如需要鉴权可配置

mark:
  input_color: "red"                           # 输入参数框颜色
  output_color: "green"                        # 输出参数框颜色
  line_width: 3

log:
  level: "INFO"
  log_file: "logs/ai_test_system.log"
```

> 代码生成时，可根据以上配置结构生成对应的 `Config` 数据类和加载逻辑。

---

### 四、数据模型设计（`case_model.py`）

使用 `dataclasses` 定义核心数据结构，便于序列化和类型检查。

```python
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


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
    prompt: str           # 由用例描述等文本拼接而成


@dataclass
class ModelResponse:
    """视觉模型返回结构（简化版）。"""
    input_regions: List[BoundingBox]
    output_regions: List[BoundingBox]
```

> 实际实现时，可在生成代码时进一步根据 Excel 具体字段名称增加属性。

---

### 五、Excel 读写模块设计（`excel_io.py`）

**依赖建议**: `openpyxl` 或 `pandas` + `openpyxl`。

#### 1. 主要职责

- 从指定 Excel 文件中读取测试用例行，并转换成 `TestCase` 实例列表。
- 在执行完成后，将标注好的截图路径写回到对应行的指定列（例如 `ScreenshotPath`）。

#### 2. 核心函数设计

```python
from typing import List
from .case_model import TestCase


def read_test_cases(excel_path: str, sheet_name: str) -> List[TestCase]:
    """从 Excel 读取测试用例并转换为 TestCase 列表。"""
    ...


def write_screenshot_path(
    excel_path: str,
    sheet_name: str,
    case_id: str,
    screenshot_path: str,
    screenshot_column: str,
) -> None:
    """根据 case_id 将截图路径写回到指定列。"""
    ...
```

> 代码生成时，应根据 Excel 的实际字段（如 `CaseID`, `Description`, `SystemURL` 等）在 `read_test_cases` 内部映射到 `TestCase` 对象属性。

---

### 六、系统截图模块设计（`screenshot_captor.py`）

**依赖建议**: `selenium` 或 `playwright`。

#### 1. 主要职责

- 启动浏览器，打开指定 URL。
- 根据需要等待页面加载完成（显式等待 / 隐式等待）。
- 对整个页面或指定元素进行截图，保存为本地文件，并返回路径。

#### 2. 核心类与方法

```python
from typing import Optional


class ScreenshotCaptor:
    def __init__(
        self,
        browser: str,
        driver_path: str,
        window_width: int,
        window_height: int,
        timeout_seconds: int,
    ) -> None:
        ...

    def open(self) -> None:
        """启动浏览器。"""
        ...

    def capture_page(self, url: str, save_path: str) -> str:
        """打开指定 URL 并对整页截图，返回保存路径。"""
        ...

    def close(self) -> None:
        """关闭浏览器。"""
        ...
```

> 如需更精细的控制（滚动页面、点击操作等），可在后续扩展更多方法。

---

### 七、视觉模型调用模块设计（`vision_model_client.py`）

**依赖建议**: `requests` 或 `httpx`。

#### 1. 主要职责

- 封装阿里开源视觉模型的 HTTP 调用。
- 将本地图片和文本描述发送给模型，解析返回的坐标信息。

#### 2. 核心类与方法

```python
from .case_model import ModelRequest, ModelResponse


class VisionModelClient:
    def __init__(self, endpoint: str, api_key: str | None = None) -> None:
        ...

    def infer(self, request: ModelRequest) -> ModelResponse:
        """调用视觉模型服务并返回输入/输出区域坐标。"""
        ...
```

> 代码生成时，可根据实际模型接口协议（如 JSON 字段名）在 `infer` 方法中进行解析。

---

### 八、参数区域定位与分类模块设计（`locator_service.py`）

此模块将模型返回的 `BoundingBox` 信息封装为 `ParameterRegion`，并根据规则标记为输入/输出参数。

#### 1. 主要职责

- 接收 `ModelResponse`，将其中坐标转换为 `ParameterRegion` 对象列表。
- 如果模型有区分类别（如标签），则根据标签映射为 input/output；如果没有，则可以通过额外规则或多轮提示来判断。

#### 2. 核心函数设计

```python
from typing import List
from .case_model import ModelResponse, ParameterRegion


def build_parameter_regions(response: ModelResponse) -> List[ParameterRegion]:
    """根据模型返回结果构造参数区域列表。"""
    ...
```

> 在生成代码时，可扩展更多参数（例如区域名称、OCR 文本等）。

---

### 九、图像标注模块设计（`image_marker.py`）

**依赖建议**: `Pillow` 或 `opencv-python`。

#### 1. 主要职责

- 读取截图图片，根据 `ParameterRegion` 列表绘制矩形框。
- 输入参数使用红框，输出参数使用绿框，线宽可配置。

#### 2. 核心函数设计

```python
from typing import List
from .case_model import ParameterRegion


def mark_image(
    image_path: str,
    regions: List[ParameterRegion],
    input_color: str = "red",
    output_color: str = "green",
    line_width: int = 3,
) -> str:
    """在图片上画红/绿框，返回保存后的新图片路径。"""
    ...
```

---

### 十、流程编排模块设计（`pipeline.py`）

`pipeline.py` 负责串联：配置加载 → Excel 读取 → 截图 → 模型识别 → 标注 → 写回 Excel。

#### 1. 核心类与方法

```python
from typing import List
from .case_model import TestCase


class AiTestPipeline:
    def __init__(self, config) -> None:
        """初始化所需的各个子组件（ExcelIO、ScreenshotCaptor、VisionModelClient 等）。"""
        ...

    def run_single_case(self, test_case: TestCase) -> TestCase:
        """执行单条测试用例：截图、调用模型、标注图片并更新 TestCase。"""
        ...

    def run_all_cases(self) -> List[TestCase]:
        """从 Excel 读取所有用例并依次执行，最后写回 Excel。"""
        ...
```

#### 2. 典型流程（伪代码）

```python
def run_all_cases(self) -> List[TestCase]:
    cases = self.excel_io.read_test_cases(
        excel_path=self.config.excel.input_path,
        sheet_name=self.config.excel.sheet_name,
    )

    self.screenshot_captor.open()
    try:
        for case in cases:
            updated_case = self.run_single_case(case)
            if updated_case.screenshot_path:
                self.excel_io.write_screenshot_path(
                    excel_path=self.config.excel.input_path,
                    sheet_name=self.config.excel.sheet_name,
                    case_id=updated_case.case_id,
                    screenshot_path=updated_case.screenshot_path,
                    screenshot_column=self.config.excel.output_image_column,
                )
    finally:
        self.screenshot_captor.close()

    return cases
```

---

### 十一、主入口设计（`main.py`）

提供命令行入口，方便通过一条命令执行整个流程。

```python
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
```

---

### 十二、配置加载模块设计（`config_loader.py`）

负责将 YAML 配置转换为带有类型的配置对象。

```python
from dataclasses import dataclass


@dataclass
class ExcelConfig:
    input_path: str
    sheet_name: str
    output_image_column: str


@dataclass
class ScreenshotConfig:
    browser: str
    driver_path: str
    window_width: int
    window_height: int
    timeout_seconds: int


@dataclass
class VisionModelConfig:
    provider: str
    endpoint: str
    api_key: str | None = None


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
    vision_model: VisionModelConfig
    mark: MarkConfig
    log: LogConfig


def load_config(path: str) -> AppConfig:
    """从 YAML 文件加载配置并转换为 AppConfig。"""
    ...
```

---

### 十三、与 Excel 文档的关系说明

- **Excel 地址**: `https://www.kdocs.cn/l/cpSC0fYjdOJn`
- 本设计文档没有绑定具体列名，而是通过配置 + 代码内部映射的方式适配。
- 生成代码时需要根据该 Excel 实际字段：
  - 确定 `case_id`、`description`、`system_url` 等字段对应的列名；
  - 将列名在 `excel_io.py` 中写死或通过配置驱动；
  - 将图片路径写回到约定列（设计中默认 `ScreenshotPath`）。

---

### 十四、后续扩展点

- 支持多种视觉模型（通过 `provider` 字段切换实现类）。
- 支持多种页面打开方式（Web、桌面应用，通过策略模式抽象）。
- 支持将参数框坐标同步到 Excel 对应列，方便进一步做自动化脚本生成。

> 至此，`ai-test-system` 的 Python 工程结构、模块划分、核心类与方法签名已经完整定义，可直接据此自动生成工程骨架代码。
