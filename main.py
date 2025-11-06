#!/usr/bin/env python3
"""
Main entry point for CS Knowledge Graph application

计算机知识图谱系统主入口文件
"""

import logging
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.api import create_app
from src.core import get_db_manager
from src.data import DataImporter
from src.core.knowledge_graph_manager import KnowledgeGraphManager


def setup_logging():
    """设置日志配置"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('logs/app.log', encoding='utf-8')
        ]
    )


def init_database():
    """初始化数据库"""
    try:
        db_manager = get_db_manager()

        # 连接数据库
        if not db_manager.connect():
            logging.error("无法连接到数据库")
            return False

        # 创建约束
        db_manager.create_constraints()
        logging.info("数据库初始化成功")
        return True
    except Exception as e:
        logging.error(f"数据库初始化失败: {e}")
        return False


def import_cpp_data():
    """导入C++知识数据"""
    try:
        db_manager = get_db_manager()
        kg_manager = KnowledgeGraphManager(db_manager)
        data_importer = DataImporter(kg_manager)

        # 导入C++数据
        cpp_data_file = project_root / "data" / "raw" / "cpp_knowledge_data.json"
        if cpp_data_file.exists():
            logging.info("开始导入C++知识数据...")
            result = data_importer.import_from_json(str(cpp_data_file))
            logging.info(f"数据导入完成: {result}")
            return True
        else:
            logging.warning(f"C++数据文件不存在: {cpp_data_file}")
            return False
    except Exception as e:
        logging.error(f"导入C++数据失败: {e}")
        return False


def main():
    """主函数"""
    # 设置日志
    setup_logging()
    logger = logging.getLogger(__name__)

    # 创建日志目录
    os.makedirs("logs", exist_ok=True)

    logger.info("启动CS Knowledge Graph系统...")

    # 初始化数据库
    if not init_database():
        logger.error("数据库初始化失败，程序退出")
        sys.exit(1)

    # 检查是否需要导入初始数据
    db_manager = get_db_manager()
    try:
        db_info = db_manager.get_database_info()
        if db_info.get('node_count', 0) == 0:
            logger.info("数据库为空，开始导入初始数据...")
            import_cpp_data()
    except Exception as e:
        logger.warning(f"检查数据库状态失败: {e}")

    # 创建Flask应用
    app = create_app()

    # 获取配置
    from config import get_config
    config = get_config()

    logger.info(f"API服务器启动在 http://{config.API_HOST}:{config.API_PORT}")
    logger.info("API文档: http://localhost:5000/api/statistics")
    logger.info("健康检查: http://localhost:5000/health")

    try:
        # 启动应用
        app.run(
            host=config.API_HOST,
            port=config.API_PORT,
            debug=config.API_DEBUG
        )
    except KeyboardInterrupt:
        logger.info("接收到中断信号，正在关闭应用...")
    except Exception as e:
        logger.error(f"应用启动失败: {e}")
    finally:
        # 断开数据库连接
        db_manager.disconnect()
        logger.info("应用已关闭")


if __name__ == '__main__':
    main()