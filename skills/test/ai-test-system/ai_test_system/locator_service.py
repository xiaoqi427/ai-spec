from typing import List

from .case_model import ModelResponse, ParameterRegion


def build_parameter_regions(response: ModelResponse) -> List[ParameterRegion]:
    """根据模型返回结果构造参数区域列表。

    当前简单实现：
    - input_regions 依次命名为 input_1, input_2, ...
    - output_regions 依次命名为 output_1, output_2, ...
    """

    regions: List[ParameterRegion] = []

    for idx, box in enumerate(response.input_regions, start=1):
        regions.append(
            ParameterRegion(
                name=f"input_{idx}",
                role="input",
                box=box,
            )
        )

    for idx, box in enumerate(response.output_regions, start=1):
        regions.append(
            ParameterRegion(
                name=f"output_{idx}",
                role="output",
                box=box,
            )
        )

    return regions
