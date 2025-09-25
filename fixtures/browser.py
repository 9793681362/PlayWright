"""浏览器夹具管理"""

from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext
from typing import Optional
from config.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)


class BrowserManager:
    """浏览器管理类"""

    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    def start_browser(self) -> Page:
        """启动浏览器并返回页面对象"""
        try:
            logger.info("启动浏览器...")
            self.playwright = sync_playwright().start()

            browser_config = self.config.browser.copy()  # 创建副本避免修改原配置

            # 从配置中提取 viewport，因为 launch 方法不接受 viewport 参数
            viewport = browser_config.pop("viewport", {"width": 1920, "height": 1080})

            # 启动浏览器
            self.browser = self.playwright.chromium.launch(**browser_config)

            # 创建上下文时设置 viewport
            self.context = self.browser.new_context(
                viewport=viewport, ignore_https_errors=True
            )

            self.page = self.context.new_page()

            # 设置超时时间
            execution_config = self.config.execution
            self.page.set_default_timeout(execution_config.get("timeout", 30000))
            self.page.set_default_navigation_timeout(
                execution_config.get("navigation_timeout", 60000)
            )

            logger.info("浏览器启动成功")
            return self.page

        except Exception as e:
            logger.error(f"浏览器启动失败: {e}")
            raise

    def close_browser(self) -> None:
        """关闭浏览器"""
        try:
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            logger.info("浏览器已关闭")
        except Exception as e:
            logger.error(f"关闭浏览器时出错: {e}")

    def __enter__(self):
        self.start_browser()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # pass
        self.close_browser()
