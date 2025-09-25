import pytest
from playwright.sync_api import sync_playwright
from utils.logger import get_logger
from pages.douyin_upload_page import DouyinUploadPage
from pathlib import Path
import time

logger = get_logger(__name__)

# 定义登录状态文件的路径。请确保你之前保存的文件就在这里。
STORAGE_STATE_PATH = Path("data/cookies/douyin_login_state.json")


@pytest.mark.douyin
def test_upload_video():  # 注意：测试函数名现在是 test_upload_video
    """
    一个完整的视频上传测试用例。
    """
    logger.info("开始执行视频上传测试")

    with sync_playwright() as p:
        # 在这里设置浏览器窗口尺寸和启动参数
        launch_options = {"headless": False, "args": ["--start-maximized"]}

        # 1. 启动浏览器
        browser = p.chromium.launch(**launch_options)

        # 2. 检查登录状态文件是否存在，并用它来创建上下文
        if not STORAGE_STATE_PATH.exists():
            logger.error(
                "未找到登录状态文件。请先运行 'save_login_state.py' 来保存登录状态。"
            )
            context = browser.new_context(no_viewport=True)
        else:
            # 关键：在这里加载 storage_state 来创建上下文
            context = browser.new_context(
                storage_state=STORAGE_STATE_PATH, no_viewport=True
            )
            logger.info("已成功加载登录状态文件。")

        # 3. 从创建好的上下文中获取一个页面
        page = context.new_page()

        # 4. 实例化你的页面对象
        douyin_page = DouyinUploadPage(page)

        # 5. 打开上传页面
        douyin_page.open()

        try:
            # 6. 验证是否自动登录成功。等待一个只有登录后才会出现的元素。
            douyin_page.page.wait_for_selector("text=发布视频", timeout=15000)
            logger.info("✔ 自动登录成功，页面已跳转到发布视频页！")

            # 7. 调用点击上传按钮的方法
            douyin_page.click_upload_button()

            # --- 在这里添加后续的上传、填写信息等操作 ---
            # 例如: douyin_page.upload_file("path/to/your/video.mp4")
            # 例如: douyin_page.fill_description("视频描述")

        except Exception as e:
            logger.warning(
                f"✘ 自动登录或点击上传按钮失败：{e}，可能需要手动登录或登录状态已过期。"
            )
            douyin_page.page.screenshot(path="login_failed.png")

        # 8. 等待一段时间以便你观察结果
        time.sleep(10)

        # 9. 关闭上下文和浏览器
        context.close()
        browser.close()
