"""日志管理工具"""

import logging
import sys
from pathlib import Path
from config.settings import LOGGING_CONFIG, FILE_PATHS

def setup_logging():
    """设置日志配置"""
    log_level = getattr(logging, LOGGING_CONFIG['level'].upper())
    
    # 创建日志格式
    formatter = logging.Formatter(LOGGING_CONFIG['format'])
    
    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # 清除已有的处理器
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 文件处理器
    log_file = FILE_PATHS['reports'] / 'execution.log'
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

def get_logger(name: str) -> logging.Logger:
    """获取指定名称的日志记录器"""
    return logging.getLogger(name)

# 初始化日志配置
setup_logging()