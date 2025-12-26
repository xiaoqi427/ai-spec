from __future__ import annotations

import json
from typing import List, Optional

import requests
from PIL import Image

from .case_model import BoundingBox, ModelRequest, ModelResponse


class VisionModelClient:
    """调用阿里开源视觉模型（或兼容 HTTP 服务）的客户端。

    为保证系统可执行，如果调用失败，会退化为一个简单的“中心区域”规则，
    返回一块输入区域和一块输出区域，方便你快速体验整体流程。
    """

    def __init__(self, endpoint: str, api_key: Optional[str] = None) -> None:
        self.endpoint = endpoint
        self.api_key = api_key

    def infer(self, request: ModelRequest) -> ModelResponse:
        """调用视觉模型服务并返回输入/输出区域坐标。"""

        try:
            files = {"image": open(request.image_path, "rb")}
            payload = {"prompt": request.prompt}
            headers = {"Accept": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            resp = requests.post(self.endpoint, files=files, data={"payload": json.dumps(payload)}, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()

            input_regions = self._parse_boxes(data.get("input_regions", []))
            output_regions = self._parse_boxes(data.get("output_regions", []))

            if not input_regions and not output_regions:
                # 如果模型没有返回有效数据，则退化为简单规则
                return self._fallback_regions(request.image_path)

            return ModelResponse(input_regions=input_regions, output_regions=output_regions)
        except Exception:
            # 为提高可执行性，任何异常直接退化为简单规则
            return self._fallback_regions(request.image_path)

    def _parse_boxes(self, raw_boxes: List) -> List[BoundingBox]:
        boxes: List[BoundingBox] = []
        for item in raw_boxes:
            # 支持 [x1, y1, x2, y2] 或 {"x1":..} 两种格式
            try:
                if isinstance(item, (list, tuple)) and len(item) == 4:
                    x1, y1, x2, y2 = item
                elif isinstance(item, dict):
                    x1 = item.get("x1")
                    y1 = item.get("y1")
                    x2 = item.get("x2")
                    y2 = item.get("y2")
                else:
                    continue

                boxes.append(BoundingBox(int(x1), int(y1), int(x2), int(y2)))
            except Exception:
                continue
        return boxes

    def _fallback_regions(self, image_path: str) -> ModelResponse:
        """当模型不可用时，基于图片尺寸构造简单的两个矩形区域。"""

        img = Image.open(image_path)
        width, height = img.size

        # 左上为“输入”，右下为“输出”
        input_box = BoundingBox(int(width * 0.05), int(height * 0.05), int(width * 0.45), int(height * 0.45))
        output_box = BoundingBox(int(width * 0.55), int(height * 0.55), int(width * 0.95), int(height * 0.95))

        return ModelResponse(input_regions=[input_box], output_regions=[output_box])
