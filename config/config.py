"""
Configuration module - 配置管理模块

管理项目的各种配置参数。
"""

import os
from typing import Dict, Any

class Config:
    """应用配置类"""

    # 数据库配置
    NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')

    # API配置
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 5000))
    API_DEBUG = os.getenv('API_DEBUG', 'False').lower() == 'true'

    # 数据路径配置
    DATA_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    RAW_DATA_PATH = os.path.join(DATA_ROOT, 'raw')
    PROCESSED_DATA_PATH = os.path.join(DATA_ROOT, 'processed')
    EXPORT_DATA_PATH = os.path.join(DATA_ROOT, 'exports')

    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')

    # 知识图谱配置
    DEFAULT_LANGUAGE = 'cpp'
    SUPPORTED_LANGUAGES = ['cpp', 'python', 'java', 'javascript']

    # 分页配置
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100

    # 缓存配置
    CACHE_TTL = 3600  # 缓存时间（秒）

    @classmethod
    def validate(cls) -> bool:
        """验证配置的有效性"""
        try:
            os.makedirs(cls.RAW_DATA_PATH, exist_ok=True)
            os.makedirs(cls.PROCESSED_DATA_PATH, exist_ok=True)
            os.makedirs(cls.EXPORT_DATA_PATH, exist_ok=True)
            os.makedirs(os.path.dirname(cls.LOG_FILE), exist_ok=True)
            return True
        except Exception as e:
            print(f"配置验证失败: {e}")
            return False

    @classmethod
    def get_db_config(cls) -> Dict[str, str]:
        """获取数据库配置"""
        return {
            'uri': cls.NEO4J_URI,
            'user': cls.NEO4J_USER,
            'password': cls.NEO4J_PASSWORD
        }


class DevelopmentConfig(Config):
    """开发环境配置"""
    API_DEBUG = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """生产环境配置"""
    API_DEBUG = False
    LOG_LEVEL = 'WARNING'


class TestingConfig(Config):
    """测试环境配置"""
    API_DEBUG = True
    LOG_LEVEL = 'DEBUG'
    # 测试数据库配置
    NEO4J_URI = 'bolt://localhost:7688'  # 不同的端口用于测试


# 配置映射
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name: str = None) -> Config:
    """根据环境名称获取配置"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')

    return config_map.get(config_name, DevelopmentConfig)