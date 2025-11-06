"""
Knowledge Graph Manager - 知识图谱管理模块

负责知识图谱的核心业务逻辑操作。
"""

import logging
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from ..models import (
    KnowledgeNode, KnowledgeRelationship, KnowledgeGraph,
    NodeType, RelationshipType, create_node, create_relationship
)
from .database_manager import DatabaseManager


class KnowledgeGraphManager:
    """知识图谱管理器"""

    def __init__(self, db_manager: DatabaseManager):
        """初始化知识图谱管理器"""
        self.db_manager = db_manager
        self.logger = logging.getLogger(__name__)

    def create_node(self, node_data: Dict[str, Any]) -> Optional[KnowledgeNode]:
        """创建知识节点"""
        try:
            # 创建节点对象
            node = create_node(**node_data)

            # 构建Cypher查询
            properties = {
                'id': node.id,
                'name': node.name,
                'node_type': node.node_type.value,
                'description': node.description,
                'category': node.category,
                'language': node.language,
                'difficulty_level': node.difficulty_level.value if node.difficulty_level else None,
                'created_at': node.created_at.isoformat(),
                'updated_at': node.updated_at.isoformat(),
                'properties': json.dumps(node.properties)
            }

            # 添加可选属性
            if node.subcategory:
                properties['subcategory'] = node.subcategory
            if node.tags:
                properties['tags'] = json.dumps(node.tags)
            if node.prerequisites:
                properties['prerequisites'] = json.dumps(node.prerequisites)
            if node.learning_time:
                properties['learning_time'] = node.learning_time

            query = """
            CREATE (n:KnowledgeNode {
                id: $id,
                name: $name,
                node_type: $node_type,
                description: $description,
                category: $category,
                subcategory: $subcategory,
                language: $language,
                difficulty_level: $difficulty_level,
                tags: $tags,
                prerequisites: $prerequisites,
                learning_time: $learning_time,
                created_at: datetime($created_at),
                updated_at: datetime($updated_at),
                properties: $properties
            })
            RETURN n
            """

            self.db_manager.execute_write_query(query, properties)
            self.logger.info(f"成功创建节点: {node.id}")
            return node

        except Exception as e:
            self.logger.error(f"创建节点失败: {e}")
            return None

    def create_relationship(self, rel_data: Dict[str, Any]) -> Optional[KnowledgeRelationship]:
        """创建知识关系"""
        try:
            # 创建关系对象
            relationship = create_relationship(**rel_data)

            # 构建Cypher查询
            properties = {
                'source_id': relationship.source_id,
                'target_id': relationship.target_id,
                'rel_id': relationship.id,
                'relationship_type': relationship.relationship_type.value,
                'description': relationship.description,
                'strength': relationship.strength.value if relationship.strength else None,
                'weight': relationship.weight,
                'bidirectional': relationship.bidirectional,
                'created_at': relationship.created_at.isoformat(),
                'updated_at': relationship.updated_at.isoformat(),
                'properties': json.dumps(relationship.properties)
            }

            # 添加可选属性
            if relationship.examples:
                properties['examples'] = json.dumps(relationship.examples)

            query = f"""
            MATCH (a:KnowledgeNode {{id: $source_id}})
            MATCH (b:KnowledgeNode {{id: $target_id}})
            CREATE (a)-[r:{relationship.relationship_type.value} {{
                id: $rel_id,
                description: $description,
                strength: $strength,
                weight: $weight,
                bidirectional: $bidirectional,
                examples: $examples,
                created_at: datetime($created_at),
                updated_at: datetime($updated_at),
                properties: $properties
            }}]->(b)
            RETURN r
            """

            self.db_manager.execute_write_query(query, properties)
            self.logger.info(f"成功创建关系: {relationship.id}")
            return relationship

        except Exception as e:
            self.logger.error(f"创建关系失败: {e}")
            return None

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """获取节点"""
        try:
            query = """
            MATCH (n:KnowledgeNode {id: $node_id})
            RETURN n
            """
            result = self.db_manager.execute_query(query, {'node_id': node_id})
            if result:
                return self._neo4j_node_to_dict(result[0]['n'])
            return None
        except Exception as e:
            self.logger.error(f"获取节点失败: {e}")
            return None

    def get_relationship(self, rel_id: str) -> Optional[Dict[str, Any]]:
        """获取关系"""
        try:
            query = """
            MATCH ()-[r]-{id: $rel_id}
            RETURN r, startNode(r) as start_node, endNode(r) as end_node
            """
            result = self.db_manager.execute_query(query, {'rel_id': rel_id})
            if result:
                return self._neo4j_relationship_to_dict(result[0])
            return None
        except Exception as e:
            self.logger.error(f"获取关系失败: {e}")
            return None

    def get_nodes_by_type(self, node_type: NodeType) -> List[Dict[str, Any]]:
        """根据类型获取节点"""
        try:
            query = """
            MATCH (n:KnowledgeNode {node_type: $node_type})
            RETURN n
            ORDER BY n.name
            """
            result = self.db_manager.execute_query(query, {'node_type': node_type.value})
            return [self._neo4j_node_to_dict(record['n']) for record in result]
        except Exception as e:
            self.logger.error(f"根据类型获取节点失败: {e}")
            return []

    def get_nodes_by_language(self, language: str) -> List[Dict[str, Any]]:
        """根据语言获取节点"""
        try:
            query = """
            MATCH (n:KnowledgeNode {language: $language})
            RETURN n
            ORDER BY n.name
            """
            result = self.db_manager.execute_query(query, {'language': language})
            return [self._neo4j_node_to_dict(record['n']) for record in result]
        except Exception as e:
            self.logger.error(f"根据语言获取节点失败: {e}")
            return []

    def search_nodes(self, keyword: str, limit: int = 20) -> List[Dict[str, Any]]:
        """搜索节点"""
        try:
            query = """
            MATCH (n:KnowledgeNode)
            WHERE toLower(n.name) CONTAINS toLower($keyword)
               OR toLower(n.description) CONTAINS toLower($keyword)
               OR toLower(n.category) CONTAINS toLower($keyword)
            RETURN n,
                   CASE
                       WHEN toLower(n.name) STARTS WITH toLower($keyword) THEN 1
                       WHEN toLower(n.name) CONTAINS toLower($keyword) THEN 2
                       ELSE 3
                   END as relevance_score
            ORDER BY relevance_score, n.name
            LIMIT $limit
            """
            result = self.db_manager.execute_query(query, {
                'keyword': keyword,
                'limit': limit
            })
            return [self._neo4j_node_to_dict(record['n']) for record in result]
        except Exception as e:
            self.logger.error(f"搜索节点失败: {e}")
            return []

    def get_adjacent_nodes(self, node_id: str) -> List[Tuple[Dict[str, Any], Dict[str, Any]]]:
        """获取相邻节点"""
        try:
            query = """
            MATCH (n:KnowledgeNode {id: $node_id})-[r]-(m:KnowledgeNode)
            RETURN m, r, startNode(r) as start_node
            """
            result = self.db_manager.execute_query(query, {'node_id': node_id})

            adjacent_nodes = []
            for record in result:
                node = self._neo4j_node_to_dict(record['m'])
                relationship = self._neo4j_relationship_to_dict({
                    'r': record['r'],
                    'start_node': record['start_node']
                })
                adjacent_nodes.append((node, relationship))

            return adjacent_nodes
        except Exception as e:
            self.logger.error(f"获取相邻节点失败: {e}")
            return []

    def find_shortest_path(self, source_id: str, target_id: str) -> Optional[List[str]]:
        """查找最短路径"""
        try:
            query = """
            MATCH (start:KnowledgeNode {id: $source_id}), (end:KnowledgeNode {id: $target_id}),
                  path = shortestPath((start)-[*]-(end))
            RETURN [node in nodes(path) | node.id] as path_ids
            """
            result = self.db_manager.execute_query(query, {
                'source_id': source_id,
                'target_id': target_id
            })

            if result:
                return result[0]['path_ids']
            return None
        except Exception as e:
            self.logger.error(f"查找最短路径失败: {e}")
            return None

    def get_learning_path(self, start_node_id: str, max_depth: int = 5) -> List[str]:
        """获取学习路径"""
        try:
            query = """
            MATCH (start:KnowledgeNode {id: $start_node_id})
            MATCH path = (start)-[:PREREQUISITE|DEPENDS_ON*1..$max_depth]->(end:KnowledgeNode)
            WHERE NOT exists((end)-[:PREREQUISITE|DEPENDS_ON]->())
            RETURN DISTINCT nodes(path) as path_nodes
            ORDER BY length(path)
            LIMIT 1
            """
            result = self.db_manager.execute_query(query, {
                'start_node_id': start_node_id,
                'max_depth': max_depth
            })

            if result:
                return [node['id'] for node in result[0]['path_nodes']]
            return []
        except Exception as e:
            self.logger.error(f"获取学习路径失败: {e}")
            return []

    def delete_node(self, node_id: str) -> bool:
        """删除节点"""
        try:
            query = """
            MATCH (n:KnowledgeNode {id: $node_id})
            DETACH DELETE n
            """
            self.db_manager.execute_write_query(query, {'node_id': node_id})
            self.logger.info(f"成功删除节点: {node_id}")
            return True
        except Exception as e:
            self.logger.error(f"删除节点失败: {e}")
            return False

    def update_node(self, node_id: str, updates: Dict[str, Any]) -> bool:
        """更新节点"""
        try:
            # 添加更新时间
            updates['updated_at'] = datetime.now().isoformat()

            # 构建SET子句
            set_clauses = []
            for key, value in updates.items():
                if key in ['tags', 'properties', 'prerequisites']:
                    set_clauses.append(f"n.{key} = '{json.dumps(value)}'")
                else:
                    set_clauses.append(f"n.{key} = ${key}")

            if not set_clauses:
                return False

            query = f"""
            MATCH (n:KnowledgeNode {{id: $node_id}})
            SET {', '.join(set_clauses)}
            RETURN n
            """

            parameters = {'node_id': node_id, **updates}
            result = self.db_manager.execute_write_query(query, parameters)

            if result:
                self.logger.info(f"成功更新节点: {node_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"更新节点失败: {e}")
            return False

    def get_statistics(self) -> Dict[str, Any]:
        """获取图谱统计信息"""
        try:
            query = """
            MATCH (n:KnowledgeNode)
            OPTIONAL MATCH (n)-[r]-()
            WITH count(DISTINCT n) as node_count, count(DISTINCT r) as rel_count
            MATCH (n:KnowledgeNode)
            RETURN node_count, rel_count,
                   collect(DISTINCT n.node_type) as node_types,
                   collect(DISTINCT n.language) as languages,
                   collect(DISTINCT n.category) as categories
            """
            result = self.db_manager.execute_query(query)

            if result:
                stats = result[0]
                return {
                    'node_count': stats['node_count'],
                    'relationship_count': stats['rel_count'],
                    'node_types': stats['node_types'],
                    'languages': [lang for lang in stats['languages'] if lang],
                    'categories': [cat for cat in stats['categories'] if cat]
                }
            return {}
        except Exception as e:
            self.logger.error(f"获取统计信息失败: {e}")
            return {}

    def _neo4j_node_to_dict(self, node) -> Dict[str, Any]:
        """将Neo4j节点转换为字典"""
        properties = dict(node)
        # 解析JSON字段
        for field in ['properties', 'tags', 'prerequisites']:
            if field in properties and properties[field]:
                try:
                    properties[field] = json.loads(properties[field])
                except:
                    pass
        return properties

    def _neo4j_relationship_to_dict(self, record) -> Dict[str, Any]:
        """将Neo4j关系转换为字典"""
        rel = record['r']
        properties = dict(rel)

        # 解析JSON字段
        for field in ['properties', 'examples']:
            if field in properties and properties[field]:
                try:
                    properties[field] = json.loads(properties[field])
                except:
                    pass

        # 添加关系信息
        properties['type'] = type(rel).__name__
        properties['source_id'] = record['start_node']['id']

        return properties