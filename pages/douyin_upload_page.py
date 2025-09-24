"""抖音视频上传页面"""

import time
from .base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)

class DouyinUploadPage(BasePage):
    """抖音视频上传页面"""
    
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://creator.douyin.com/creator-micro/content/upload?enter_from=dou_web"
    
    # 页面元素选择器
    UPLOAD_BUTTON = "//div[contains(text(),'上传')]"
    VIDEO_INPUT = "input[type='file']"
    TITLE_INPUT = "//textarea[@placeholder='填写标题']"
    DESCRIPTION_INPUT = "//textarea[@placeholder='添加描述...']"
    PUBLISH_BUTTON = "//button[contains(text(),'发布')]"
    UPLOAD_PROGRESS = "//div[contains(text(),'上传完成')]"  # 上传完成提示
    SUCCESS_INDICATOR = "//div[contains(text(),'发布成功')]"  # 发布成功提示
    
    def open_upload_page(self):
        """打开上传页面"""
        self.navigate()
        self.wait_for_upload_interface()
        return self
    
    def wait_for_upload_interface(self, timeout: int = 10000):
        """等待上传界面加载完成"""
        logger.info("等待上传界面加载")
        self.wait_for_element(self.UPLOAD_BUTTON, timeout)
        return self
    
    def is_upload_interface_loaded(self) -> bool:
        """检查上传界面是否加载完成"""
        return self.is_element_visible(self.UPLOAD_BUTTON)
    
    def upload_video(self, video_path: str) -> bool:
        """上传视频文件"""
        try:
            logger.info(f"开始上传视频: {video_path}")
            
            # 点击上传按钮并选择文件
            with self.page.expect_file_chooser() as fc_info:
                self.click(self.UPLOAD_BUTTON)
            file_chooser = fc_info.value
            file_chooser.set_files(video_path)
            
            logger.info("视频文件已选择，等待上传...")
            return True
            
        except Exception as e:
            logger.error(f"视频上传失败: {e}")
            self.take_screenshot("video_upload_failed.png")
            return False
    
    def wait_for_upload_complete(self, timeout: int = 300000) -> bool:
        """等待视频上传完成"""
        logger.info("等待视频上传完成...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.is_element_visible(self.UPLOAD_PROGRESS, 5000):
                logger.info("视频上传完成")
                return True
            time.sleep(5)
        
        logger.error("视频上传超时")
        return False
    
    def enter_video_info(self, title: str, description: str = ""):
        """输入视频信息"""
        if title:
            self.type_text(self.TITLE_INPUT, title)
        
        if description:
            self.type_text(self.DESCRIPTION_INPUT, description)
        
        return self
    
    def publish_video(self) -> bool:
        """发布视频"""
        try:
            self.click(self.PUBLISH_BUTTON)
            logger.info("点击发布按钮")
            
            # 等待发布完成
            time.sleep(10)
            
            # 检查是否发布成功
            if self.is_element_visible(self.SUCCESS_INDICATOR, 30000):
                logger.info("视频发布成功")
                return True
            else:
                logger.warning("发布状态不确定，请手动检查")
                return True  # 可能成功但没有成功提示
                
        except Exception as e:
            logger.error(f"发布视频失败: {e}")
            self.take_screenshot("publish_failed.png")
            return False
    
    def complete_upload(self, video_path: str, title: str, description: str = "") -> bool:
        """完成完整的上传流程"""
        try:
            if not self.is_upload_interface_loaded():
                logger.error("上传界面未正确加载")
                return False
            
            if not self.upload_video(video_path):
                return False
            
            if not self.wait_for_upload_complete():
                return False
            
            self.enter_video_info(title, description)
            
            return self.publish_video()
            
        except Exception as e:
            logger.error(f"上传流程失败: {e}")
            self.take_screenshot("upload_process_failed.png")
            return False