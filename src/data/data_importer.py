"""
Data Importer - 数据导入模块

负责从各种数据源导入知识图谱数据。
"""

import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from ..models import NodeType, RelationshipType
from ..core import KnowledgeGraphManager


class DataImporter:
    """数据导入器"""

    def __init__(self, kg_manager: KnowledgeGraphManager):
        """初始化数据导入器"""
        self.kg_manager = kg_manager
        self.logger = logging.getLogger(__name__)

    def import_from_json(self, file_path: str) -> Dict[str, int]:
        """从JSON文件导入数据"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"文件不存在: {file_path}")

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return self._import_knowledge_data(data)

        except Exception as e:
            self.logger.error(f"从JSON文件导入失败: {e}")
            return {'nodes': 0, 'relationships': 0, 'errors': 1}

    def import_cpp_knowledge_data(self, data_file: str) -> Dict[str, int]:
        """导入C++知识数据"""
        return self.import_from_json(data_file)

    def _import_knowledge_data(self, data: Dict[str, Any]) -> Dict[str, int]:
        """导入知识图谱数据"""
        nodes_count = 0
        relationships_count = 0
        errors = 0

        try:
            # 导入节点
            if 'nodes' in data:
                for node_data in data['nodes']:
                    try:
                        # 转换枚举类型
                        if 'node_type' in node_data:
                            node_data['node_type'] = NodeType(node_data['node_type'])
                        if 'difficulty_level' in node_data and node_data['difficulty_level']:
                            from ..models import DifficultyLevel
                            node_data['difficulty_level'] = DifficultyLevel(node_data['difficulty_level'])

                        node = self.kg_manager.create_node(node_data)
                        if node:
                            nodes_count += 1
                        else:
                            errors += 1
                    except Exception as e:
                        self.logger.error(f"导入节点失败: {e}")
                        errors += 1

            # 导入关系
            if 'relationships' in data:
                for rel_data in data['relationships']:
                    try:
                        # 转换枚举类型
                        if 'relationship_type' in rel_data:
                            rel_data['relationship_type'] = RelationshipType(rel_data['relationship_type'])
                        if 'strength' in rel_data and rel_data['strength']:
                            from ..models import RelationshipStrength
                            rel_data['strength'] = RelationshipStrength(rel_data['strength'])

                        relationship = self.kg_manager.create_relationship(rel_data)
                        if relationship:
                            relationships_count += 1
                        else:
                            errors += 1
                    except Exception as e:
                        self.logger.error(f"导入关系失败: {e}")
                        errors += 1

            self.logger.info(f"数据导入完成: 节点 {nodes_count}, 关系 {relationships_count}, 错误 {errors}")

        except Exception as e:
            self.logger.error(f"导入数据失败: {e}")
            errors += 1

        return {
            'nodes': nodes_count,
            'relationships': relationships_count,
            'errors': errors
        }

    def export_to_json(self, file_path: str, node_filter: Dict[str, Any] = None) -> bool:
        """导出数据到JSON文件"""
        try:
            # 获取所有节点
            if node_filter:
                nodes = self._get_filtered_nodes(node_filter)
            else:
                nodes = self._get_all_nodes()

            # 获取所有关系
            relationships = self._get_all_relationships()

            # 构建导出数据
            export_data = {
                'metadata': {
                    'export_date': str(Path(file_path).stat().st_mtime),
                    'total_nodes': len(nodes),
                    'total_relationships': len(relationships)
                },
                'nodes': nodes,
                'relationships': relationships
            }

            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)

            self.logger.info(f"成功导出数据到: {file_path}")
            return True

        except Exception as e:
            self.logger.error(f"导出数据失败: {e}")
            return False

    def _get_all_nodes(self) -> List[Dict[str, Any]]:
        """获取所有节点"""
        try:
            query = "MATCH (n:KnowledgeNode) RETURN n"
            result = self.kg_manager.db_manager.execute_query(query)
            return [self.kg_manager._neo4j_node_to_dict(record['n']) for record in result]
        except Exception as e:
            self.logger.error(f"获取所有节点失败: {e}")
            return []

    def _get_all_relationships(self) -> List[Dict[str, Any]]:
        """获取所有关系"""
        try:
            query = "MATCH ()-[r]-() RETURN r, startNode(r) as start_node, endNode(r) as end_node"
            result = self.kg_manager.db_manager.execute_query(query)

            relationships = []
            for record in result:
                rel_data = self.kg_manager._neo4j_relationship_to_dict(record)
                relationships.append(rel_data)

            return relationships
        except Exception as e:
            self.logger.error(f"获取所有关系失败: {e}")
            return []

    def _get_filtered_nodes(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """根据过滤条件获取节点"""
        try:
            # 构建查询条件
            conditions = []
            parameters = {}

            for key, value in filters.items():
                if key == 'node_type':
                    conditions.append(f"n.node_type = ${key}")
                elif key == 'language':
                    conditions.append(f"n.language = ${key}")
                elif key == 'category':
                    conditions.append(f"n.category = ${key}")
                elif key == 'difficulty_level':
                    conditions.append(f"n.difficulty_level = ${key}")

                parameters[key] = value

            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

            query = f"""
            MATCH (n:KnowledgeNode)
            {where_clause}
            RETURN n
            ORDER BY n.name
            """

            result = self.kg_manager.db_manager.execute_query(query, parameters)
            return [self.kg_manager._neo4j_node_to_dict(record['n']) for record in result]

        except Exception as e:
            self.logger.error(f"获取过滤节点失败: {e}")
            return []

    def validate_data_structure(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        """验证数据结构"""
        errors = []
        warnings = []

        try:
            # 验证元数据
            if 'metadata' not in data:
                warnings.append("缺少metadata字段")

            # 验证节点
            if 'nodes' not in data:
                errors.append("缺少nodes字段")
            else:
                for i, node in enumerate(data['nodes']):
                    node_errors = self._validate_node(node, f"nodes[{i}]")
                    errors.extend(node_errors)

            # 验证关系
            if 'relationships' not in data:
                warnings.append("缺少relationships字段")
            else:
                for i, rel in enumerate(data['relationships']):
                    rel_errors = self._validate_relationship(rel, f"relationships[{i}]")
                    errors.extend(rel_errors)

        except Exception as e:
            errors.append(f"数据结构验证失败: {e}")

        return {'errors': errors, 'warnings': warnings}

    def _validate_node(self, node: Dict[str, Any], path: str) -> List[str]:
        """验证节点数据"""
        errors = []

        required_fields = ['id', 'name', 'node_type', 'description']
        for field in required_fields:
            if field not in node:
                errors.append(f"{path}: 缺少必需字段 '{field}'")

        # 验证节点类型
        if 'node_type' in node:
            try:
                NodeType(node['node_type'])
            except ValueError:
                errors.append(f"{path}: 无效的节点类型 '{node['node_type']}'")

        # 验证难度级别
        if 'difficulty_level' in node and node['difficulty_level']:
            try:
                from ..models import DifficultyLevel
                DifficultyLevel(node['difficulty_level'])
            except ValueError:
                errors.append(f"{path}: 无效的难度级别 '{node['difficulty_level']}'")

        return errors

    def _validate_relationship(self, rel: Dict[str, Any], path: str) -> List[str]:
        """验证关系数据"""
        errors = []

        required_fields = ['id', 'source_id', 'target_id', 'relationship_type']
        for field in required_fields:
            if field not in rel:
                errors.append(f"{path}: 缺少必需字段 '{field}'")

        # 验证关系类型
        if 'relationship_type' in rel:
            try:
                RelationshipType(rel['relationship_type'])
            except ValueError:
                errors.append(f"{path}: 无效的关系类型 '{rel['relationship_type']}'")

        # 验证关系强度
        if 'strength' in rel and rel['strength']:
            try:
                from ..models import RelationshipStrength
                RelationshipStrength(rel['strength'])
            except ValueError:
                errors.append(f"{path}: 无效的关系强度 '{rel['strength']}'")

        return errors