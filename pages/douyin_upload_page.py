from .base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class DouyinUploadPage(BasePage):  # <-- 继承 BasePage
    """抖音视频上传页面，专注于页面操作"""

    def __init__(self, page):
        super().__init__(page)  # 调用父类构造函数
        self.url = (
            "https://creator.douyin.com/creator-micro/content/upload?enter_from=dou_web"
        )

    def open(self):
        self.page.goto(self.url)
        logger.info(f"成功导航到上传页面: {self.url}")
        self.page.set_viewport_size({"width": 1920, "height": 1080})
        logger.info("浏览器窗口已设置为最大化视口。")

    def click_upload_button(self):
        logger.info("正在尝试点击上传视频按钮...")
        self.page.locator("div.container-drag-upload-tL99XD").get_by_role(
            "button", name="上传视频"
        ).click()
        logger.info("✔ 已成功点击上传视频按钮。")

    def fill_title(self, title_text: str):
        """填写作品标题"""
        selector = 'input[placeholder="填写作品标题，为作品获得更多流量"]'
        self.type_text(selector, title_text)
        logger.info(f"✔ 已填写标题: {title_text}")

    def fill_description(self, description_text: str):
        """填写作品描述"""
        # 这是 contenteditable 富文本框的选择器，根据页面实际属性调整
        selector = "div[contenteditable='true'][data-placeholder='添加作品简介']"

        # 先清空内容
        self.page.locator(selector).evaluate("el => el.innerText = ''")

        # 输入文本
        self.page.locator(selector).type(description_text, delay=50)

        logger.info(f"✔ 已填写描述")

    def upload_image(self):
        """上传封面图"""
        logger.info(f"正在上传封面图...")

        cover_path = r"C:\Users\rick1\Desktop\app\re-plan-api\media\output\image.jpg"
        logger.info(f"正在上传封面: {cover_path}")

        # 1.点击“选择封面”按钮（让 input 出现）
        self.page.locator("div.title-wA45Xd:text('选择封面')").first.click()
        logger.info("✔ 已点击选择封面按钮")

        # 2.上传文件到隐藏的 input
        self.page.set_input_files("input.semi-upload-hidden-input", cover_path)
        logger.info("✔ 封面上传成功")

        # 3.点击完成
        self.page.locator("button", has_text="完成").click()
        logger.info("✔ 已点击封面完成按钮")

    def click_publish(self):
        self.page.locator("#popover-tip-container > button").click()
        logger.info("✔ 点击发布完成")
