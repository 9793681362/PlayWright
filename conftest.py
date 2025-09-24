"""Pytest配置"""

import pytest
import asyncio
from playwright.sync_api import sync_playwright
from config.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)

@pytest.fixture(scope="function")
def browser():
    """浏览器夹具 - 修复同步API问题"""
    from fixtures.browser import BrowserManager
    config = Config()
    
    # 确保在独立的事件循环中运行
    with BrowserManager(config) as browser_manager:
        yield browser_manager.page

@pytest.fixture(scope="session")
def event_loop():
    """为整个测试会话创建事件循环"""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def douyin_login_page(browser):
    """抖音登录页面夹具"""
    from pages.douyin_login_page import DouyinLoginPage
    return DouyinLoginPage(browser)

@pytest.fixture
def douyin_upload_page(browser):
    """抖音上传页面夹具"""
    from pages.douyin_upload_page import DouyinUploadPage
    return DouyinUploadPage(browser)

def pytest_configure(config):
    """Pytest配置钩子"""
    # 确保报告目录存在
    from config.settings import FILE_PATHS
    FILE_PATHS['reports'].mkdir(exist_ok=True)
    FILE_PATHS['screenshots'].mkdir(exist_ok=True)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试报告钩子，用于失败时截图"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # 测试失败时截图
        try:
            if "browser" in item.funcargs:
                page = item.funcargs["browser"]
                screenshot_name = f"{item.name}_failure.png"
                page.screenshot(path=f"reports/screenshots/{screenshot_name}")
                logger.info(f"测试失败截图已保存: {screenshot_name}")
        except Exception as e:
            logger.error(f"截图失败: {e}")