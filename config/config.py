"""配置管理类"""

import yaml
from pathlib import Path
from .settings import BASE_DIR, BROWSER_CONFIG, EXECUTION_CONFIG, PLATFORM_URLS

class Config:
    """配置管理类"""
    
    def __init__(self, config_file: str = None):
        self.config_file = config_file or BASE_DIR / 'config' / 'default_config.yaml'
        self._config = self._load_config()
        
    def _load_config(self) -> dict:
        """加载配置文件"""
        default_config = {
            'browser': BROWSER_CONFIG,
            'execution': EXECUTION_CONFIG,
            'platform_urls': PLATFORM_URLS
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as file:
                    user_config = yaml.safe_load(file) or {}
                    # 合并配置
                    return self._merge_configs(default_config, user_config)
            except Exception as e:
                print(f"加载配置文件失败，使用默认配置: {e}")
                return default_config
        else:
            return default_config
    
    def _merge_configs(self, default: dict, user: dict) -> dict:
        """递归合并配置"""
        result = default.copy()
        for key, value in user.items():
            if isinstance(value, dict) and key in result and isinstance(result[key], dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    @property
    def browser(self) -> dict:
        return self._config.get('browser', {})
    
    @property
    def execution(self) -> dict:
        return self._config.get('execution', {})
    
    @property
    def platform_urls(self) -> dict:
        return self._config.get('platform_urls', {})
    
    def get_platform_url(self, platform_key: str) -> str:
        return self.platform_urls.get(platform_key, '')