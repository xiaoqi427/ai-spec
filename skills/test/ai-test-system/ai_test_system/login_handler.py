import time
from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginHandler:
    """处理Web系统登录的类。"""

    def __init__(
        self,
        login_url: str,
        username: str,
        password: str,
        username_selector: str = "input[name='username']",
        password_selector: str = "input[name='password']",
        submit_selector: str = "button[type='submit']",
        wait_after_login: int = 3,
    ) -> None:
        self.login_url = login_url
        self.username = username
        self.password = password
        self.username_selector = username_selector
        self.password_selector = password_selector
        self.submit_selector = submit_selector
        self.wait_after_login = wait_after_login

    def execute(self, driver: webdriver.Remote) -> None:
        """执行登录操作。
        
        :param driver: Selenium WebDriver实例
        :raises Exception: 登录失败时抛出异常
        """
        print(f"正在登录: {self.login_url}")
        driver.set_page_load_timeout(20)
        try:
            driver.get(self.login_url)
            print("登录页面加载完成")
        except Exception as e:
            print(f"登录页面加载超时: {e}，继续执行...")
        
        try:
            # 等待页面加载
            wait = WebDriverWait(driver, 10)
            
            # 输入用户名
            print(f"查找用户名输入框: {self.username_selector}")
            username_input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.username_selector))
            )
            username_input.send_keys(self.username)
            print(f"已输入用户名: {self.username}")
            
            # 输入密码
            print(f"查找密码输入框: {self.password_selector}")
            password_input = driver.find_element(By.CSS_SELECTOR, self.password_selector)
            password_input.send_keys(self.password)
            print("已输入密码")
            
            # 点击登录按钮
            print(f"查找登录按钮: {self.submit_selector}")
            submit_button = driver.find_element(By.CSS_SELECTOR, self.submit_selector)
            submit_button.click()
            print("已点击登录按钮")
            
            # 等待登录完成
            time.sleep(self.wait_after_login)
            print(f"登录完成，当前URL: {driver.current_url}")
            
        except Exception as e:
            print(f"登录失败: {e}")
            raise
