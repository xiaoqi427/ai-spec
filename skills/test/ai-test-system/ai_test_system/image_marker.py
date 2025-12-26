import os
from typing import List

from PIL import Image, ImageDraw

from .case_model import ParameterRegion


def mark_image(
    image_path: str,
    regions: List[ParameterRegion],
    input_color: str = "red",
    output_color: str = "green",
    line_width: int = 3,
) -> str:
    """在图片上画红/绿框，返回保存后的新图片路径。"""

    img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    for region in regions:
        box = region.box
        color = input_color if region.role == "input" else output_color
        for offset in range(line_width):
            draw.rectangle(
                [
                    (box.x1 - offset, box.y1 - offset),
                    (box.x2 + offset, box.y2 + offset),
                ],
                outline=color,
            )

    base, ext = os.path.splitext(image_path)
    marked_path = f"{base}_marked{ext or '.png'}"
    img.save(marked_path)
    return marked_path
