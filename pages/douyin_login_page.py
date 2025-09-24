"""抖音登录页面"""

from .base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)

class DouyinLoginPage(BasePage):
    """抖音登录页面"""
    
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://www.douyin.com"
    
    # 页面元素选择器
    LOGIN_BUTTON = "//div[contains(text(),'登录')]"
    USERNAME_INPUT = "//input[@placeholder='请输入手机号']"
    PASSWORD_INPUT = "//input[@placeholder='请输入密码']"
    SUBMIT_BUTTON = "//button[contains(text(),'登录')]"
    AVATAR = "//div[contains(@class,'avatar')]"  # 登录成功后的头像元素
    
    def open_login_page(self):
        """打开登录页面"""
        self.navigate()
        return self
    
    def click_login_button(self):
        """点击登录按钮"""
        self.click(self.LOGIN_BUTTON)
        return self
    
    def enter_credentials(self, username: str, password: str):
        """输入用户名和密码"""
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        return self
    
    def submit_login(self):
        """提交登录"""
        self.click(self.SUBMIT_BUTTON)
        return self
    
    def is_login_successful(self, timeout: int = 10000) -> bool:
        """检查登录是否成功"""
        try:
            return self.is_element_visible(self.AVATAR, timeout)
        except:
            return False
    
    def login(self, username: str, password: str) -> bool:
        """执行完整登录流程"""
        try:
            logger.info("开始抖音登录流程")
            
            self.open_login_page()
            self.click_login_button()
            self.enter_credentials(username, password)
            self.submit_login()
            
            # 等待登录结果
            time.sleep(5)
            
            if self.is_login_successful():
                logger.info("抖音登录成功")
                return True
            else:
                logger.error("抖音登录失败")
                self.take_screenshot("douyin_login_failed.png")
                return False
                
        except Exception as e:
            logger.error(f"登录过程中出错: {e}")
            self.take_screenshot("douyin_login_error.png")
            return False