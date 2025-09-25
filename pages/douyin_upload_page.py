import json
from pathlib import Path
from utils.logger import get_logger

logger = get_logger(__name__)


class DouyinUploadPage:
    """抖音视频上传页面，专注于页面操作"""

    def __init__(self, page):
        self.page = page
        self.url = (
            "https://creator.douyin.com/creator-micro/content/upload?enter_from=dou_web"
        )

    def open(self):
        """打开上传页面并最大化窗口"""

        # 1. 导航到目标 URL
        self.page.goto(self.url)
        logger.info(f"成功导航到上传页面: {self.url}")

        # 2. 将浏览器窗口最大化
        # 正确的写法是传递一个包含 width 和 height 的字典
        self.page.set_viewport_size({"width": 1920, "height": 1080})
        logger.info("浏览器窗口已设置为最大化视口。")

    def click_upload_button(self):
        """点击上传视频按钮"""
        logger.info("正在尝试点击上传视频按钮...")

        # 使用组合定位器，先找到父元素，再在其内部根据角色和文本定位
        self.page.locator("div.container-drag-upload-tL99XD").get_by_role(
            "button", name="上传视频"
        ).click()

        logger.info("✔ 已成功点击上传视频按钮。")
