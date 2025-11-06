"""
Core module - 核心业务逻辑模块

包含知识图谱系统的核心功能实现。

主要模块：
- DatabaseManager: 数据库连接和操作管理
- KnowledgeGraphManager: 知识图谱业务逻辑管理
"""

from .database_manager import DatabaseManager, get_db_manager
from .knowledge_graph_manager import KnowledgeGraphManager

__all__ = [
    'DatabaseManager',
    'get_db_manager',
    'KnowledgeGraphManager',
]