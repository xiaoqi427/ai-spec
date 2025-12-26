import os
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class ScreenshotCaptor:
    def __init__(
        self,
        browser: str,
        driver_path: str,
        window_width: int,
        window_height: int,
        timeout_seconds: int,
    ) -> None:
        self.browser = browser.lower()
        self.driver_path = driver_path
        self.window_width = window_width
        self.window_height = window_height
        self.timeout_seconds = timeout_seconds
        self._driver: Optional[webdriver.Remote] = None

    def open(self) -> None:
        """启动浏览器（当前实现为无头 Chrome）。"""

        if self._driver is not None:
            return

        if self.browser != "chrome":
            raise ValueError("当前 ScreenshotCaptor 仅示例支持 chrome 浏览器，请在配置中设置 browser=chrome")

        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument(f"--window-size={self.window_width},{self.window_height}")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"--user-data-dir=/tmp/chrome_user_data_{os.getpid()}")

        service = Service(executable_path=self.driver_path)
        self._driver = webdriver.Chrome(service=service, options=chrome_options)

    def get_driver(self) -> webdriver.Remote:
        """获取WebDriver实例，供外部使用（如登录操作）。"""
        return self._driver

    def capture_page(self, url: str, save_path: str) -> str:
        """打开指定 URL 并对整页截图，返回保存路径。"""

        if self._driver is None:
            raise RuntimeError("浏览器未打开，请先调用 open()")

        print(f"正在访问: {url}")
        self._driver.set_page_load_timeout(self.timeout_seconds)
        
        try:
            self._driver.get(url)
            print(f"页面加载完成")
        except Exception as e:
            print(f"页面加载超时或失败: {e}，继续截图...")

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        self._driver.save_screenshot(save_path)
        print(f"截图已保存: {save_path}")
        return save_path

    def close(self) -> None:
        """关闭浏览器。"""

        if self._driver is not None:
            self._driver.quit()
            self._driver = None
