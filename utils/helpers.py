"""辅助函数工具"""

import time
import random
from pathlib import Path
from typing import Any, Callable
from utils.logger import get_logger

logger = get_logger(__name__)

def retry_operation(operation: Callable, max_attempts: int = 3, 
                   delay: float = 1.0, backoff: float = 2.0) -> Any:
    """重试操作，支持指数退避"""
    last_exception = None
    current_delay = delay
    
    for attempt in range(max_attempts):
        try:
            return operation()
        except Exception as e:
            last_exception = e
            logger.warning(f"操作失败，第 {attempt + 1} 次重试: {e}")
            
            if attempt < max_attempts - 1:
                time.sleep(current_delay)
                current_delay *= backoff  # 指数退避
    
    raise last_exception

def random_delay(min_delay: float = 1.0, max_delay: float = 3.0) -> None:
    """随机延迟，模拟人类操作"""
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)

def validate_file_path(file_path: str) -> bool:
    """验证文件路径是否存在"""
    path = Path(file_path)
    if not path.exists():
        logger.error(f"文件不存在: {file_path}")
        return False
    return True

def wait_for_condition(condition: Callable, timeout: int = 30, 
                      interval: float = 1.0) -> bool:
    """等待条件成立"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if condition():
            return True
        time.sleep(interval)
    return False