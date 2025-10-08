import pytest
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from utils.logger import get_logger
from pages.xiaohongshu_upload_page import XiaohongshuUploadPage
from utils.file_reader import read_video_info

logger = get_logger(__name__)

# 定义登录状态文件路径
STORAGE_STATE_PATH = Path("data/cookies/xiaohongshu_login_state.json")
VIDEO_INFO_PATH = Path(
    r"C:\Users\rick1\Desktop\app\re-plan-api\media\output\replan.txt"
)
VIDEO_FILE_PATH = Path(r"C:\Users\rick1\Desktop\app\re-plan-api\media\output\video.mp4")


@pytest.mark.xiaohongshu
def test_upload_video():

    logger.info("开始执行小红书视频上传测试")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])

        # 创建上下文并加载登录状态
        if not STORAGE_STATE_PATH.exists():
            logger.error(
                "未找到登录状态文件，请先运行 save_login_state.py 保存登录状态。"
            )
            context = browser.new_context(no_viewport=True)
        else:
            context = browser.new_context(
                storage_state=STORAGE_STATE_PATH, no_viewport=True
            )
            logger.info("已成功加载登录状态文件。")

        # 新建页面
        page = context.new_page()
        xhs_page = XiaohongshuUploadPage(page)

        # 打开上传页面
        xhs_page.open()

        try:
            # 等待登录成功标志
            page.wait_for_selector("text=发布", timeout=15000)
            logger.info("✔ 自动登录成功，页面已跳转到发布视频页！")

            # 1. 上传视频
            xhs_page.upload_file(str(VIDEO_FILE_PATH))

            # 2. 上传封面
            xhs_page.upload_image()

            # 3. 填写标题和描述
            title, description = read_video_info(VIDEO_INFO_PATH)
            xhs_page.fill_title(title)
            xhs_page.fill_description(description)

            # 4. 点击发布
            xhs_page.click_publish()
            time.sleep(10)

        except Exception as e:
            logger.warning(f"✘ 上传流程异常：{e}")
            page.screenshot(path="login_failed.png")

        finally:
            context.close()
            browser.close()
            logger.info("浏览器已关闭，测试结束。")
