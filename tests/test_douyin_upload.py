import pytest
from playwright.sync_api import sync_playwright
from utils.logger import get_logger
from pages.douyin_upload_page import DouyinUploadPage
from pages.base_page import BasePage
from utils.file_reader import read_video_info
from pathlib import Path
import time

logger = get_logger(__name__)

# 定义登录状态文件的路径
STORAGE_STATE_PATH = Path("data/cookies/douyin_login_state.json")
VIDEO_INFO_PATH = Path(
    r"C:\Users\rick1\Desktop\app\re-plan-api\media\output\replan.txt"
)
VIDEO_FILE_PATH = Path(r"C:\Users\rick1\Desktop\app\re-plan-api\media\output\video.mp4")


@pytest.mark.douyin
def test_upload_video():
    logger.info("开始执行视频上传测试")

    with sync_playwright() as p:
        # 启动浏览器
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
        douyin_page = DouyinUploadPage(page)

        # 打开上传页面
        douyin_page.open()

        try:
            # 等待登录成功标志
            douyin_page.page.wait_for_selector("text=发布视频", timeout=15000)
            logger.info("✔ 自动登录成功，页面已跳转到发布视频页！")

            # 1.上传视频
            douyin_page.upload_file(str(VIDEO_FILE_PATH))
            logger.info("✔ 视频上传已触发")

            # 2.上传封面
            douyin_page.upload_image()

            # 3.读取并填写标题和描述
            title, description = read_video_info(VIDEO_INFO_PATH)
            print("标题:", title)
            print("描述:", description)
            douyin_page.fill_title(title)
            douyin_page.fill_description(description)

            # 4.点击发布

            douyin_page.click_publish()
            time.sleep(30)

        except Exception as e:
            logger.warning(f"✘ 上传流程异常：{e}")
            douyin_page.page.screenshot(path="login_failed.png")

        finally:
            context.close()
            browser.close()
            logger.info("浏览器已关闭，测试结束。")
