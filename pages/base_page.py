"""页面对象基类"""

from playwright.sync_api import Page, Locator
from typing import Optional, Callable, Any
import time
from utils.logger import get_logger

logger = get_logger(__name__)

class BasePage:
    """所有页面对象的基类"""
    
    def __init__(self, page: Page):
        self.page = page
        self.url = None
        self.timeout = 30000
    
    def navigate(self, url: str = None) -> None:
        """导航到指定URL"""
        target_url = url or self.url
        if not target_url:
            raise ValueError("未提供URL")
        
        logger.info(f"导航到: {target_url}")
        self.page.goto(target_url)
        self.wait_for_page_loaded()
    
    def wait_for_page_loaded(self, timeout: int = None) -> None:
        """等待页面加载完成"""
        timeout = timeout or self.timeout
        self.page.wait_for_load_state('networkidle', timeout=timeout)
    
    def wait_for_element(self, selector: str, timeout: int = None) -> Locator:
        """等待元素出现"""
        timeout = timeout or self.timeout
        logger.debug(f"等待元素: {selector}")
        return self.page.wait_for_selector(selector, timeout=timeout)
    
    def click(self, selector: str, timeout: int = None) -> None:
        """点击元素"""
        timeout = timeout or self.timeout
        logger.debug(f"点击元素: {selector}")
        element = self.wait_for_element(selector, timeout)
        element.click()
    
    def type_text(self, selector: str, text: str, timeout: int = None) -> None:
        """输入文本"""
        timeout = timeout or self.timeout
        logger.debug(f"在元素 {selector} 中输入文本: {text}")
        element = self.wait_for_element(selector, timeout)
        element.fill(text)
    
    def get_text(self, selector: str, timeout: int = None) -> str:
        """获取元素文本"""
        timeout = timeout or self.timeout
        element = self.wait_for_element(selector, timeout)
        return element.text_content().strip()
    
    def is_element_visible(self, selector: str, timeout: int = 5000) -> bool:
        """检查元素是否可见"""
        try:
            self.wait_for_element(selector, timeout)
            return self.page.is_visible(selector)
        except:
            return False
    
    def scroll_to_element(self, selector: str) -> None:
        """滚动到元素"""
        element = self.wait_for_element(selector)
        element.scroll_into_view_if_needed()
    
    def take_screenshot(self, name: str = None) -> str:
        """截取页面截图"""
        from config.settings import FILE_PATHS
        if not name:
            name = f"screenshot_{int(time.time())}.png"
        
        screenshot_path = FILE_PATHS['screenshots'] / name
        self.page.screenshot(path=str(screenshot_path))
        logger.info(f"截图已保存: {screenshot_path}")
        return str(screenshot_path)
    
    def retry_operation(self, operation: Callable, max_attempts: int = 3, 
                       delay: float = 1.0) -> Any:
        """重试操作"""
        last_exception = None
        for attempt in range(max_attempts):
            try:
                return operation()
            except Exception as e:
                last_exception = e
                logger.warning(f"操作失败，第 {attempt + 1} 次重试: {e}")
                if attempt < max_attempts - 1:
                    time.sleep(delay)
        
        raise last_exception