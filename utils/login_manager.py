import json
from pathlib import Path
from playwright.sync_api import Page
from utils.logger import get_logger

logger = get_logger(__name__)


class LoginManager:
    """登录状态管理器，支持通过 cookies 自动登录抖音"""

    def __init__(self, page: Page, platform: str = "douyin"):
        self.page = page
        self.platform = platform
        # 修复 Path 拼接问题
        self.cookie_file = Path("data") / "cookies" / f"{platform}_cookies.json"
        # 确保目录存在
        self.cookie_file.parent.mkdir(parents=True, exist_ok=True)

    def save_cookies(self):
        """保存当前页面的 cookies"""
        try:
            cookies = self.page.context.cookies()
            with open(self.cookie_file, "w", encoding="utf-8") as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            logger.info(f"{self.platform} cookies 保存成功: {self.cookie_file}")
            return True
        except Exception as e:
            logger.error(f"保存 cookies 失败: {e}")
            return False

    def load_cookies(
        self,
        url: str = "https://creator.douyin.com/creator-micro/content/upload?enter_from=dou_web",
    ):
        """读取 cookies 并注入到页面，实现自动登录"""
        if not self.cookie_file.exists():
            logger.warning(f"未找到 {self.cookie_file}, 请先手动登录并保存 cookies")
            return False

        try:
            with open(self.cookie_file, "r", encoding="utf-8") as f:
                cookies = json.load(f)

            # Playwright add_cookies 接受的是列表，每个 cookie 里必须包含 name, value, domain 等字段
            self.page.context.add_cookies(cookies)

            # 刷新页面以应用 cookies
            self.page.goto(url)
            logger.info(f"{self.platform} cookies 加载成功，已尝试自动登录")
            return True
        except Exception as e:
            logger.error(f"加载 cookies 失败: {e}")
            return False
