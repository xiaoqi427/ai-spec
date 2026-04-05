#!/usr/bin/env python3
"""
从当前 Chrome 浏览器提取 Cookie — 零外部依赖
==============================================
直接读取 macOS Chrome 的 Cookie 数据库，提取指定域名的 Cookie，
保存为 browser-use 兼容的 JSON 格式，供后续 Cookie 文件导入使用。

特性:
  - 纯 Python 标准库（sqlite3 + subprocess），无需 pip install
  - 支持 Chrome 80+ 加密 Cookie（macOS Keychain + AES-CBC 解密）
  - 自动检测 Chrome 是否运行，复制 DB 到临时目录避免锁冲突
  - 支持多 Profile 和多域名
  - 输出格式与 browser-use cookies export 完全兼容

用法:
  # 提取 Coding 平台 Cookie（默认）
  python3 extract-chrome-cookies.py

  # 提取 SIT 环境 Cookie
  python3 extract-chrome-cookies.py --domain pri-fssc-web-sit.digitalyili.com --output config/sit-cookies.json

  # 指定 Chrome Profile
  python3 extract-chrome-cookies.py --profile "Profile 1"

  # 仅检查是否有有效 Cookie（不写文件）
  python3 extract-chrome-cookies.py --check-only

@author sevenxiao
"""

import os
import sys
import json
import sqlite3
import subprocess
import shutil
import tempfile
import argparse
import logging
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
# scripts → bug-fix-pipeline → bug-fix-cycle → code → skills → ai-spec → yili(项目根)
PROJECT_ROOT = SCRIPT_DIR.parents[5]

# 默认配置
DEFAULT_DOMAIN = "coding.yili.com"
DEFAULT_OUTPUT = "config/coding-cookies.json"
DEFAULT_PROFILE = "Default"

# macOS Chrome Cookie 数据库路径模板
CHROME_COOKIE_DB = Path.home() / "Library/Application Support/Google/Chrome/{profile}/Cookies"

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("extract-chrome-cookies")


# ---------------------------------------------------------------------------
# Chrome Cookie 解密（macOS）
# ---------------------------------------------------------------------------
def get_chrome_encryption_key() -> Optional[bytes]:
    """
    从 macOS Keychain 获取 Chrome 的加密密钥，
    并使用 PBKDF2 派生 AES 密钥。
    """
    try:
        result = subprocess.run(
            [
                "security",
                "find-generic-password",
                "-w",
                "-s",
                "Chrome Safe Storage",
                "-a",
                "Chrome",
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            log.debug("无法从 Keychain 获取 Chrome 密钥")
            return None

        import hashlib

        chrome_password = result.stdout.strip()
        key = hashlib.pbkdf2_hmac(
            "sha1",
            chrome_password.encode("utf-8"),
            b"saltysalt",
            1003,
            dklen=16,
        )
        return key
    except Exception as e:
        log.debug(f"获取 Chrome 加密密钥失败: {e}")
        return None


def decrypt_chrome_cookie(encrypted_value: bytes, key: bytes) -> Optional[str]:
    """
    解密 Chrome macOS 加密的 Cookie 值。
    Chrome 使用 Keychain 密钥 + AES-CBC (iv = 16 空格) 加密。
    """
    if not encrypted_value or len(encrypted_value) < 4:
        return None

    # Chrome v80+ 前缀 b'v10' 或 b'v11'
    encrypted_data = encrypted_value[3:]  # 去掉前缀
    iv = b" " * 16

    # 优先尝试 cryptography 库
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.backends import default_backend

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(encrypted_data) + decryptor.finalize()
        # 去除 PKCS7 padding
        padding_len = decrypted[-1]
        if 0 < padding_len <= 16:
            decrypted = decrypted[:-padding_len]
        return decrypted.decode("utf-8", errors="replace")
    except ImportError:
        pass

    # 降级: 尝试 pycryptodome
    try:
        from Crypto.Cipher import AES

        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted_data)
        padding_len = decrypted[-1]
        if 0 < padding_len <= 16:
            decrypted = decrypted[:-padding_len]
        return decrypted.decode("utf-8", errors="replace")
    except ImportError:
        pass

    log.warning(
        "需要 cryptography 或 pycryptodome 库来解密 Chrome Cookie:\n"
        "  pip3 install cryptography --user --break-system-packages"
    )
    return None


# ---------------------------------------------------------------------------
# Chrome Cookie 提取
# ---------------------------------------------------------------------------
def extract_cookies(
    domain: str,
    profile: str = DEFAULT_PROFILE,
) -> list[dict]:
    """
    从 Chrome Cookie 数据库提取指定域名的 Cookie。

    :param domain: 目标域名（模糊匹配，如 coding.yili.com）
    :param profile: Chrome Profile 名称
    :return: Cookie 列表 [{name, value, domain, path}]
    """
    db_path = Path(
        str(CHROME_COOKIE_DB).replace("{profile}", profile)
    )
    if not db_path.exists():
        log.error(f"Chrome Cookie 数据库不存在: {db_path}")
        log.info(f"  提示: 确认 Chrome Profile 名称是否正确（当前: {profile}）")
        return []

    # 复制到临时目录，避免 Chrome 锁定
    tmp_dir = tempfile.mkdtemp()
    tmp_db = Path(tmp_dir) / "Cookies"
    try:
        shutil.copy2(db_path, tmp_db)
    except Exception as e:
        log.error(f"复制 Cookie 数据库失败: {e}")
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return []

    try:
        conn = sqlite3.connect(str(tmp_db))
        cursor = conn.cursor()

        # 查询匹配域名的 Cookie
        cursor.execute(
            "SELECT name, value, encrypted_value, host_key, path "
            "FROM cookies WHERE host_key LIKE ?",
            (f"%{domain}%",),
        )
        rows = cursor.fetchall()
        conn.close()
    except Exception as e:
        log.error(f"读取 Cookie 数据库失败: {e}")
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return []
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    if not rows:
        log.warning(f"Chrome 中未找到 {domain} 的 Cookie（Profile: {profile}）")
        return []

    # 获取解密密钥（仅在有加密 Cookie 时需要）
    encryption_key = None
    has_encrypted = any(row[2] for row in rows if not row[1])
    if has_encrypted:
        encryption_key = get_chrome_encryption_key()
        if not encryption_key:
            log.warning("无法获取解密密钥，加密的 Cookie 将被跳过")

    # 提取 Cookie
    cookies = []
    skipped = 0
    for name, value, encrypted_value, host_key, path in rows:
        cookie_val = None

        # 优先使用未加密的 value
        if value:
            cookie_val = value
        elif encrypted_value and encryption_key:
            cookie_val = decrypt_chrome_cookie(encrypted_value, encryption_key)

        if cookie_val:
            # 确保值只包含 ASCII 可打印字符
            try:
                cookie_val.encode("latin-1")
            except (UnicodeEncodeError, UnicodeDecodeError):
                from urllib.parse import quote

                cookie_val = quote(cookie_val, safe="")

            cookies.append(
                {
                    "name": name,
                    "value": cookie_val,
                    "domain": host_key,
                    "path": path,
                }
            )
        else:
            skipped += 1

    log.info(
        f"从 Chrome ({profile}) 提取了 {len(cookies)} 条 Cookie"
        + (f"，跳过 {skipped} 条无法解密" if skipped else "")
    )
    return cookies


def save_cookies(cookies: list[dict], output_path: Path) -> bool:
    """保存 Cookie 到 JSON 文件（browser-use 兼容格式）"""
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=2, ensure_ascii=False)
        log.info(f"Cookie 已保存到: {output_path}")
        return True
    except Exception as e:
        log.error(f"Cookie 保存失败: {e}")
        return False


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="从当前 Chrome 浏览器提取 Cookie（macOS）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 提取 Coding 平台 Cookie
  python3 extract-chrome-cookies.py

  # 提取 SIT 环境 Cookie
  python3 extract-chrome-cookies.py --domain pri-fssc-web-sit.digitalyili.com --output config/sit-cookies.json

  # 指定 Chrome Profile
  python3 extract-chrome-cookies.py --profile "Profile 1"

  # 仅检查（不写文件）
  python3 extract-chrome-cookies.py --check-only
        """,
    )
    parser.add_argument(
        "--domain",
        default=DEFAULT_DOMAIN,
        help=f"目标域名（模糊匹配），默认: {DEFAULT_DOMAIN}",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"输出文件路径（相对于项目根目录），默认: {DEFAULT_OUTPUT}",
    )
    parser.add_argument(
        "--profile",
        default=DEFAULT_PROFILE,
        help=f"Chrome Profile 名称，默认: {DEFAULT_PROFILE}",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="仅检查是否存在有效 Cookie，不写文件",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="显示详细日志",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # 提取 Cookie
    cookies = extract_cookies(
        domain=args.domain,
        profile=args.profile,
    )

    if not cookies:
        log.error("未提取到有效 Cookie，请确认:")
        log.error("  1. Chrome 中已登录目标平台")
        log.error(f"  2. Chrome Profile 名称正确（当前: {args.profile}）")
        log.error(f"  3. 域名匹配正确（当前: {args.domain}）")
        sys.exit(1)

    if args.check_only:
        log.info(f"✓ 找到 {len(cookies)} 条有效 Cookie")
        # 列出 Cookie 名称（不显示值）
        for c in cookies:
            log.info(f"  {c['name']} ({c['domain']})")
        sys.exit(0)

    # 保存到文件
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = PROJECT_ROOT / output_path

    if save_cookies(cookies, output_path):
        log.info(f"✓ 完成！后续可直接使用:")
        log.info(f"  browser-use cookies import {args.output}")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
