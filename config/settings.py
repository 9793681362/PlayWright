"""框架配置设置"""

import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent.parent

# 浏览器配置
BROWSER_CONFIG = {
    'headless': False,
    'slow_mo': 100,
    'viewport': {'width': 1920, 'height': 1080},
    'args': [
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--disable-blink-features=AutomationControlled',
        '--disable-features=VizDisplayCompositor'
    ]
}

# 执行配置
EXECUTION_CONFIG = {
    'timeout': 30000,
    'navigation_timeout': 60000,
    'wait_timeout': 10000,
    'retry_attempts': 3
}

# 平台URL配置
PLATFORM_URLS = {
    'douyin_login': 'https://www.douyin.com',
    'douyin_creator': 'https://creator.douyin.com/creator-micro/content/upload?enter_from=dou_web',
    'xiaohongshu_login': 'https://www.xiaohongshu.com'
}

# 日志配置
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': BASE_DIR / 'reports' / 'execution.log'
}

# 文件路径配置
FILE_PATHS = {
    'reports': BASE_DIR / 'reports',
    'screenshots': BASE_DIR / 'reports' / 'screenshots',
    'videos': BASE_DIR / 'data' / 'videos',
    'images': BASE_DIR / 'data' / 'images'
}

# 创建必要的目录
for path in FILE_PATHS.values():
    path.mkdir(parents=True, exist_ok=True)