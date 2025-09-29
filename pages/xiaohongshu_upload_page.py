from .base_page import BasePage
from utils.logger import get_logger
import time

logger = get_logger(__name__)


class XiaohongshuUploadPage(BasePage):
    """小红书视频上传页面，专注于页面操作"""

    def __init__(self, page):
        super().__init__(page)
        self.url = "https://creator.xiaohongshu.com/publish/publish?source=official&from=menu&target=video"

    def open(self):
        self.page.goto(self.url)
        logger.info(f"成功导航到上传页面: {self.url}")
        # self.page.set_viewport_size({"width": 1920, "height": 1080})
        logger.info("浏览器窗口已设置为最大化视口。")

    def upload_file(self, video_path: str):
        """上传视件"""
        logger.info(f"正在上传视频: {video_path}")
        # input[type=file] 通常是上传按钮
        self.page.set_input_files("input[type='file']", video_path)
        logger.info("✔ 视频上传已触发")

    def fill_title(self, title_text: str):
        """填写作品标题"""
        selector = 'input[placeholder="填写标题会有更多赞哦～"]'
        self.type_text(selector, title_text)
        logger.info(f"✔ 已填写标题: {title_text}")

    def fill_description(self, description_text: str):
        """填写作品描述"""
        editor_selector = "div.tiptap.ProseMirror[contenteditable='true']"

        logger.info("🔹 查找描述编辑器...")
        editor = self.page.locator(editor_selector)

        try:
            editor.wait_for(state="visible", timeout=30000)
            logger.info("✔ 描述编辑器已找到")

            # 使用 evaluate 设置内容（TipTap 推荐方法）
            editor.evaluate(
                f"(el) => {{ el.innerHTML = `<p>{description_text}</p>`; }}"
            )
            logger.info(f"✔ 已填写描述: {description_text}")

        except Exception as e:
            logger.error(f"❌ 填写描述失败: {e}")
            raise

    def upload_image(self):
        """点击上传按钮，通过 filechooser 填入图片路径"""
        cover_path = r"C:\Users\rick1\Desktop\app\re-plan-api\media\output\image.jpg"
        logger.info(f"正在上传封面图: {cover_path}")
        # 点击设置封面按钮
        cover_button = self.page.locator("div.upload-cover:has-text('设置封面')")
        cover_button.click()
        logger.info("✔ 已点击选择封面按钮")

        # 点击上传图片按钮，等待 filechooser 弹出
        with self.page.expect_file_chooser() as fc_info:
            self.page.locator(".upload-btn").click()  # 点击上传图片按钮
        file_chooser = fc_info.value

        # 设置要上传的文件
        file_chooser.set_files(cover_path)
        logger.info("✔ 封面上传成功")

        # 点击完成按钮
        self.page.locator("button:has-text('确定')").click()
        logger.info("✔ 已点击封面完成按钮")

    def click_publish(self):
        """点击发布"""
        self.page.locator("button:has-text('发布')").click()
        logger.info("✔ 点击发布完成")
