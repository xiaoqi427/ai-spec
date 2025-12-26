import os
from typing import List

from .case_model import ModelRequest, TestCase
from .config_loader import AppConfig
from .excel_io import read_test_cases, write_screenshot_path
from .image_marker import mark_image
from .locator_service import build_parameter_regions
from .login_handler import LoginHandler
from .screenshot_captor import ScreenshotCaptor
from .vision_model_client import VisionModelClient


class AiTestPipeline:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.screenshot_captor = ScreenshotCaptor(
            browser=config.screenshot.browser,
            driver_path=config.screenshot.driver_path,
            window_width=config.screenshot.window_width,
            window_height=config.screenshot.window_height,
            timeout_seconds=config.screenshot.timeout_seconds,
        )
        self.vision_client = VisionModelClient(
            endpoint=config.vision_model.endpoint,
            api_key=config.vision_model.api_key,
        )

    def _ensure_dirs(self) -> None:
        os.makedirs("./output", exist_ok=True)
        os.makedirs(os.path.dirname(self.config.log.log_file), exist_ok=True)

    def run_single_case(self, test_case: TestCase) -> TestCase:
        """执行单条测试用例：截图、调用模型、标注图片并更新 TestCase。"""

        self._ensure_dirs()

        # 1. 截图
        screenshot_path = os.path.join("./output", f"{test_case.case_id}.png")
        self.screenshot_captor.capture_page(test_case.system_url, screenshot_path)

        # 2. 调用视觉模型
        prompt_parts = [test_case.description]
        if test_case.extra_context:
            prompt_parts.append(str(test_case.extra_context))
        prompt = "\n".join(prompt_parts)

        model_req = ModelRequest(image_path=screenshot_path, prompt=prompt)
        model_resp = self.vision_client.infer(model_req)

        # 3. 构造参数区域，并标注图片
        regions = build_parameter_regions(model_resp)
        marked_path = mark_image(
            image_path=screenshot_path,
            regions=regions,
            input_color=self.config.mark.input_color,
            output_color=self.config.mark.output_color,
            line_width=self.config.mark.line_width,
        )

        test_case.screenshot_path = marked_path
        test_case.parameter_regions = regions
        return test_case

    def run_all_cases(self) -> List[TestCase]:
        """从 Excel 读取所有用例并依次执行，最后写回 Excel。"""

        cfg = self.config
        print(f"正在读取Excel: {cfg.excel.input_path}")
        cases = read_test_cases(
            excel_path=cfg.excel.input_path,
            sheet_name=cfg.excel.sheet_name,
            case_id_column=cfg.excel.case_id_column,
            description_column=cfg.excel.description_column,
            system_url_column=cfg.excel.system_url_column,
            extra_context_column=cfg.excel.extra_context_column,
        )

        if not cases:
            print("未读取到任何测试用例")
            return []

        print(f"读取到 {len(cases)} 条用例，开始执行...")
        self.screenshot_captor.open()
        print("浏览器已启动")
        
        # 如果启用了登录，先执行登录
        if cfg.login.enabled:
            try:
                login_handler = LoginHandler(
                    login_url=cfg.login.login_url,
                    username=cfg.login.username,
                    password=cfg.login.password,
                    username_selector=cfg.login.username_selector,
                    password_selector=cfg.login.password_selector,
                    submit_selector=cfg.login.submit_selector,
                    wait_after_login=cfg.login.wait_after_login,
                )
                login_handler.execute(self.screenshot_captor.get_driver())
            except Exception as e:
                print(f"登录失败: {e}，继续执行...")
        
        try:
            for i, case in enumerate(cases, 1):
                print(f"\n[{i}/{len(cases)}] 处理用例: {case.case_id}")
                updated_case = self.run_single_case(case)
                if updated_case.screenshot_path:
                    write_screenshot_path(
                        excel_path=cfg.excel.input_path,
                        sheet_name=cfg.excel.sheet_name,
                        case_id=updated_case.case_id,
                        screenshot_path=updated_case.screenshot_path,
                        case_id_column=cfg.excel.case_id_column,
                        screenshot_column=cfg.excel.output_image_column,
                    )
                    print(f"用例 {case.case_id} 处理完成")
        finally:
            self.screenshot_captor.close()
            print("\n浏览器已关闭")

        return cases
