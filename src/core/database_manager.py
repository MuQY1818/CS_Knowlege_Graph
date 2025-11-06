"""
Database Manager - 数据库管理模块

负责与Neo4j数据库的连接和操作。
"""

import logging
from typing import Dict, List, Any, Optional, Union
from neo4j import GraphDatabase
from contextlib import contextmanager
from ..config import Config


class DatabaseManager:
    """Neo4j数据库管理器"""

    def __init__(self, config: Config = None):
        """初始化数据库管理器"""
        self.config = config or Config()
        self.driver = None
        self.logger = logging.getLogger(__name__)

    def connect(self) -> bool:
        """连接到数据库"""
        try:
            self.driver = GraphDatabase.driver(
                self.config.NEO4J_URI,
                auth=(self.config.NEO4J_USER, self.config.NEO4J_PASSWORD)
            )
            # 测试连接
            with self.driver.session() as session:
                result = session.run("RETURN 1 as test")
                result.single()

            self.logger.info("成功连接到Neo4j数据库")
            return True
        except Exception as e:
            self.logger.error(f"连接数据库失败: {e}")
            return False

    def disconnect(self):
        """断开数据库连接"""
        if self.driver:
            self.driver.close()
            self.logger.info("数据库连接已断开")

    @contextmanager
    def session(self, database="neo4j"):
        """创建数据库会话上下文"""
        if not self.driver:
            raise RuntimeError("数据库未连接")
        session = self.driver.session(database=database)
        try:
            yield session
        finally:
            session.close()

    def execute_query(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """执行查询并返回结果"""
        parameters = parameters or {}
        try:
            with self.session() as session:
                result = session.run(query, parameters)
                return [record.data() for record in result]
        except Exception as e:
            self.logger.error(f"查询执行失败: {e}")
            raise

    def execute_write_query(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """执行写操作查询"""
        parameters = parameters or {}
        try:
            with self.session() as session:
                result = session.run(query, parameters)
                return [record.data() for record in result]
        except Exception as e:
            self.logger.error(f"写操作执行失败: {e}")
            raise

    def clear_database(self) -> bool:
        """清空数据库（谨慎使用）"""
        try:
            with self.session() as session:
                # 删除所有关系和节点
                session.run("MATCH (n) DETACH DELETE n")
                self.logger.warning("数据库已清空")
                return True
        except Exception as e:
            self.logger.error(f"清空数据库失败: {e}")
            return False

    def create_constraints(self):
        """创建数据库约束"""
        constraints = [
            "CREATE CONSTRAINT node_id_unique IF NOT EXISTS FOR (n) REQUIRE n.id IS UNIQUE",
            "CREATE CONSTRAINT relationship_id_unique IF NOT EXISTS FOR ()-[r]-() REQUIRE r.id IS UNIQUE",
            "CREATE INDEX node_type_index IF NOT EXISTS FOR (n) ON (n.node_type)",
            "CREATE INDEX node_language_index IF NOT EXISTS FOR (n) ON (n.language)",
            "CREATE INDEX node_category_index IF NOT EXISTS FOR (n) ON (n.category)",
        ]

        for constraint in constraints:
            try:
                with self.session() as session:
                    session.run(constraint)
                    self.logger.info(f"创建约束成功: {constraint}")
            except Exception as e:
                self.logger.error(f"创建约束失败: {constraint}, 错误: {e}")

    def get_database_info(self) -> Dict[str, Any]:
        """获取数据库信息"""
        try:
            with self.session() as session:
                # 获取节点数量
                node_count = session.run("MATCH (n) RETURN count(n) as count").single()["count"]

                # 获取关系数量
                rel_count = session.run("MATCH ()-[r]->() RETURN count(r) as count").single()["count"]

                # 获取节点类型分布
                node_types = session.run("""
                    MATCH (n)
                    RETURN n.node_type as type, count(n) as count
                    ORDER BY count DESC
                """).data()

                # 获取关系类型分布
                rel_types = session.run("""
                    MATCH ()-[r]->()
                    RETURN type(r) as type, count(r) as count
                    ORDER BY count DESC
                """).data()

                return {
                    "node_count": node_count,
                    "relationship_count": rel_count,
                    "node_types": node_types,
                    "relationship_types": rel_types
                }
        except Exception as e:
            self.logger.error(f"获取数据库信息失败: {e}")
            return {}


# 全局数据库管理器实例
db_manager = DatabaseManager()


def get_db_manager() -> DatabaseManager:
    """获取数据库管理器实例"""
    return db_manager