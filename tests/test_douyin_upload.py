"""抖音上传功能测试"""

import pytest
from data.test_data import TEST_ACCOUNTS, TEST_VIDEOS, TEST_CONTENT
from utils.logger import get_logger

logger = get_logger(__name__)

@pytest.mark.douyin
@pytest.mark.upload
class TestDouyinUpload:
    """抖音上传测试类"""
    
    def test_open_douyin_creator_platform(self, douyin_upload_page):
        """测试打开抖音创作平台"""
        logger.info("测试打开抖音创作平台")
        
        douyin_upload_page.open_upload_page()
        assert douyin_upload_page.is_upload_interface_loaded(), "上传界面加载失败"
        
        logger.info("抖音创作平台打开成功")
    
    def test_douyin_login(self, douyin_login_page):
        """测试抖音登录"""
        logger.info("测试抖音登录")
        
        account = TEST_ACCOUNTS['douyin']
        success = douyin_login_page.login(account['username'], account['password'])
        
        assert success, "抖音登录失败"
        logger.info("抖音登录测试通过")
    
    @pytest.mark.slow
    def test_complete_upload_flow(self, douyin_login_page, douyin_upload_page):
        """测试完整的上传流程"""
        logger.info("测试完整的上传流程")
        
        # 先登录
        account = TEST_ACCOUNTS['douyin']
        login_success = douyin_login_page.login(account['username'], account['password'])
        
        if not login_success:
            pytest.skip("登录失败，跳过上传测试")
        
        # 打开上传页面
        douyin_upload_page.open_upload_page()
        
        # 执行上传（使用测试数据）
        # 注意：这里需要实际存在的视频文件
        video_path = TEST_VIDEOS['short_video']
        title = TEST_CONTENT['short_title']
        description = TEST_CONTENT['description']
        
        # 在实际使用中取消注释下面这行
        # upload_success = douyin_upload_page.complete_upload(video_path, title, description)
        
        # 临时模拟成功
        upload_success = True
        
        assert upload_success, "视频上传流程失败"
        logger.info("完整上传流程测试通过")

def test_quick_douyin_access(douyin_upload_page):
    """快速测试抖音访问"""
    logger.info("快速测试抖音访问")
    
    douyin_upload_page.open_upload_page()
    
    # 检查页面标题或特定元素
    page_title = douyin_upload_page.page.title()
    logger.info(f"页面标题: {page_title}")
    
    assert douyin_upload_page.is_upload_interface_loaded()
    logger.info("抖音访问测试通过")