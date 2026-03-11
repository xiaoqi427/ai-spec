"""登录处理模块：调用登录接口获取 Cookie，注入到 HTTP Session 中"""
from __future__ import annotations

import logging
from http.cookiejar import CookieJar
from typing import Dict, Optional

import requests

from .config_loader import LoginConfig, ServerConfig

logger = logging.getLogger(__name__)


class LoginHandler:
    """自动登录处理器

    调用登录接口，从响应的 Set-Cookie 头中提取所有 Cookie，
    并将其注入到指定的 requests.Session 中，供后续接口调用使用。
    """

    def __init__(self, login_config: LoginConfig, server_config: ServerConfig) -> None:
        self._config = login_config
        self._server_config = server_config

    def login_and_inject(self, session: requests.Session) -> bool:
        """执行登录并将获取到的 Cookie 注入到 session 中

        Args:
            session: 需要注入 Cookie 的 requests.Session 实例

        Returns:
            True 表示登录成功，False 表示登录失败
        """
        if not self._config.enabled:
            logger.info("登录未启用，跳过")
            return True

        login_url = self._config.url
        if not login_url:
            logger.error("登录 URL 为空，无法登录")
            return False

        payload = {
            "usernum": self._config.usernum,
            "password": self._config.password,
        }

        logger.info(f"正在登录: {login_url} (用户: {self._config.usernum})")
        print(f"  正在登录: {login_url} (用户: {self._config.usernum}) ... ", end="", flush=True)

        try:
            # 使用独立请求执行登录，不影响 session 的已有配置
            timeout = (self._server_config.connect_timeout, self._server_config.timeout)
            response = requests.post(
                login_url,
                json=payload,
                timeout=timeout,
                allow_redirects=False,
            )

            logger.debug(f"登录响应状态码: {response.status_code}")
            logger.debug(f"登录响应头: {dict(response.headers)}")

            # 提取 Set-Cookie
            cookies = response.cookies
            cookie_count = len(cookies)

            if cookie_count == 0:
                # 有些服务可能在响应体中返回 token 而非 Set-Cookie
                logger.warning("登录响应中未找到 Set-Cookie 头")
                # 尝试从响应体获取 token
                token = self._extract_token_from_body(response)
                if token:
                    session.headers["Authorization"] = f"Bearer {token}"
                    print(f"成功 (Token)")
                    logger.info(f"从响应体获取到 Token，已注入 Authorization 头")
                    return True

                print("失败 (无 Cookie/Token)")
                logger.error("登录失败：响应中既无 Set-Cookie 也无 Token")
                return False

            # 将所有 Cookie 注入到 session 中
            for cookie in cookies:
                session.cookies.set_cookie(cookie)
                logger.debug(f"注入 Cookie: {cookie.name}={cookie.value[:20]}...")

            # 同时构造 Cookie 字符串注入到请求头（双重保障）
            cookie_str = "; ".join(
                f"{cookie.name}={cookie.value}" for cookie in cookies
            )
            session.headers["Cookie"] = cookie_str

            print(f"成功 ({cookie_count} 个 Cookie)")
            logger.info(f"登录成功，获取到 {cookie_count} 个 Cookie")

            # 打印登录响应体摘要（如果有）
            self._log_login_response(response)

            return True

        except requests.exceptions.ConnectionError as e:
            print(f"失败 (连接错误)")
            logger.error(f"登录连接失败: {e}")
            return False
        except requests.exceptions.Timeout as e:
            print(f"失败 (超时)")
            logger.error(f"登录超时: {e}")
            return False
        except Exception as e:
            print(f"失败 ({e})")
            logger.error(f"登录异常: {e}", exc_info=True)
            return False

    def _extract_token_from_body(self, response: requests.Response) -> Optional[str]:
        """尝试从响应体 JSON 中提取 Token

        支持常见的返回格式:
        - {"data": {"token": "xxx"}}
        - {"data": "xxx"}
        - {"token": "xxx"}
        - {"access_token": "xxx"}
        """
        try:
            body = response.json()
        except Exception:
            return None

        # 检查是否成功
        success = body.get("success", True)
        if not success:
            error_msg = body.get("message", "未知错误")
            logger.error(f"登录接口返回失败: {error_msg}")
            return None

        data = body.get("data")

        # data 直接是 token 字符串
        if isinstance(data, str) and len(data) > 10:
            return data

        # data 是 dict，包含 token 字段
        if isinstance(data, dict):
            for key in ("token", "access_token", "accessToken", "jwt"):
                token = data.get(key)
                if token and isinstance(token, str):
                    return token

        # 顶层 token
        for key in ("token", "access_token", "accessToken"):
            token = body.get(key)
            if token and isinstance(token, str):
                return token

        return None

    def _log_login_response(self, response: requests.Response):
        """记录登录响应体摘要"""
        try:
            body = response.json()
            success = body.get("success")
            message = body.get("message", "")
            code = body.get("code")
            logger.info(f"登录响应: success={success}, code={code}, message={message}")
        except Exception:
            logger.debug(f"登录响应体非 JSON: {response.text[:200]}")
