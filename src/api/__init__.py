"""
API module - API接口模块

提供RESTful API接口供前端调用。

主要功能：
- 节点和关系的CRUD操作
- 知识图谱查询和搜索
- 数据导入和导出
- 统计信息获取
"""

from .app import create_app

__all__ = [
    'create_app',
]