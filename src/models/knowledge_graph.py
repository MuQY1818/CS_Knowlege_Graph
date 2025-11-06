"""
Knowledge Graph Model - 知识图谱模型

定义知识图谱的整体结构和操作。
"""

from typing import List, Dict, Any, Optional, Set, Tuple
from pydantic import BaseModel, Field
from .knowledge_node import KnowledgeNode, NodeType
from .knowledge_relationship import KnowledgeRelationship, RelationshipType


class KnowledgeGraph(BaseModel):
    """知识图谱模型"""

    # 基本信息
    id: str = Field(..., description="图谱唯一标识符")
    name: str = Field(..., description="图谱名称")
    description: str = Field(..., description="图谱描述")

    # 图谱内容
    nodes: Dict[str, KnowledgeNode] = Field(default_factory=dict, description="节点字典")
    relationships: Dict[str, KnowledgeRelationship] = Field(default_factory=dict, description="关系字典")

    # 元数据
    domain: Optional[str] = Field(None, description="知识领域")
    version: str = Field(default="1.0.0", description="版本号")
    language: Optional[str] = Field(None, description="主要语言")

    # 统计信息
    node_count: int = Field(default=0, description="节点数量")
    relationship_count: int = Field(default=0, description="关系数量")

    class Config:
        """Pydantic配置"""
        arbitrary_types_allowed = True

    def add_node(self, node: KnowledgeNode) -> None:
        """添加节点"""
        if node.id not in self.nodes:
            self.nodes[node.id] = node
            self.node_count += 1

    def remove_node(self, node_id: str) -> bool:
        """移除节点"""
        if node_id in self.nodes:
            del self.nodes[node_id]
            self.node_count -= 1
            # 同时移除相关关系
            relationships_to_remove = []
            for rel_id, rel in self.relationships.items():
                if rel.source_id == node_id or rel.target_id == node_id:
                    relationships_to_remove.append(rel_id)

            for rel_id in relationships_to_remove:
                self.remove_relationship(rel_id)
            return True
        return False

    def add_relationship(self, relationship: KnowledgeRelationship) -> None:
        """添加关系"""
        # 验证节点存在
        if relationship.source_id not in self.nodes:
            raise ValueError(f"源节点 {relationship.source_id} 不存在")
        if relationship.target_id not in self.nodes:
            raise ValueError(f"目标节点 {relationship.target_id} 不存在")

        if relationship.id not in self.relationships:
            self.relationships[relationship.id] = relationship
            self.relationship_count += 1

    def remove_relationship(self, relationship_id: str) -> bool:
        """移除关系"""
        if relationship_id in self.relationships:
            del self.relationships[relationship_id]
            self.relationship_count -= 1
            return True
        return False

    def get_node(self, node_id: str) -> Optional[KnowledgeNode]:
        """获取节点"""
        return self.nodes.get(node_id)

    def get_relationship(self, relationship_id: str) -> Optional[KnowledgeRelationship]:
        """获取关系"""
        return self.relationships.get(relationship_id)

    def get_nodes_by_type(self, node_type: NodeType) -> List[KnowledgeNode]:
        """根据类型获取节点"""
        return [node for node in self.nodes.values() if node.node_type == node_type]

    def get_nodes_by_language(self, language: str) -> List[KnowledgeNode]:
        """根据语言获取节点"""
        return [node for node in self.nodes.values() if node.language == language]

    def get_relationships_by_type(self, relationship_type: RelationshipType) -> List[KnowledgeRelationship]:
        """根据类型获取关系"""
        return [rel for rel in self.relationships.values() if rel.relationship_type == relationship_type]

    def get_adjacent_nodes(self, node_id: str) -> List[Tuple[KnowledgeNode, KnowledgeRelationship]]:
        """获取相邻节点"""
        adjacent = []
        for rel in self.relationships.values():
            if rel.source_id == node_id:
                target_node = self.get_node(rel.target_id)
                if target_node:
                    adjacent.append((target_node, rel))
            elif rel.target_id == node_id and rel.bidirectional:
                source_node = self.get_node(rel.source_id)
                if source_node:
                    adjacent.append((source_node, rel))
        return adjacent

    def get_outgoing_relationships(self, node_id: str) -> List[KnowledgeRelationship]:
        """获取节点的出边关系"""
        return [rel for rel in self.relationships.values() if rel.source_id == node_id]

    def get_incoming_relationships(self, node_id: str) -> List[KnowledgeRelationship]:
        """获取节点的入边关系"""
        return [rel for rel in self.relationships.values() if rel.target_id == node_id]

    def find_shortest_path(self, source_id: str, target_id: str) -> Optional[List[str]]:
        """查找最短路径（BFS算法）"""
        if source_id not in self.nodes or target_id not in self.nodes:
            return None

        from collections import deque

        queue = deque([(source_id, [source_id])])
        visited = {source_id}

        while queue:
            current_id, path = queue.popleft()

            if current_id == target_id:
                return path

            # 获取相邻节点
            for rel in self.relationships.values():
                next_id = None
                if rel.source_id == current_id:
                    next_id = rel.target_id
                elif rel.bidirectional and rel.target_id == current_id:
                    next_id = rel.source_id

                if next_id and next_id not in visited:
                    visited.add(next_id)
                    queue.append((next_id, path + [next_id]))

        return None

    def get_connected_components(self) -> List[Set[str]]:
        """获取连通分量"""
        visited = set()
        components = []

        for node_id in self.nodes:
            if node_id not in visited:
                component = set()
                stack = [node_id]

                while stack:
                    current_id = stack.pop()
                    if current_id not in visited:
                        visited.add(current_id)
                        component.add(current_id)

                        # 添加相邻节点
                        for rel in self.relationships.values():
                            if rel.source_id == current_id:
                                if rel.target_id not in visited:
                                    stack.append(rel.target_id)
                            elif rel.bidirectional and rel.target_id == current_id:
                                if rel.source_id not in visited:
                                    stack.append(rel.source_id)

                components.append(component)

        return components

    def calculate_statistics(self) -> Dict[str, Any]:
        """计算图谱统计信息"""
        stats = {
            "节点总数": self.node_count,
            "关系总数": self.relationship_count,
            "节点类型分布": {},
            "关系类型分布": {},
            "语言分布": {},
            "连通分量数": len(self.get_connected_components()),
        }

        # 节点类型分布
        for node in self.nodes.values():
            node_type = node.node_type.value
            stats["节点类型分布"][node_type] = stats["节点类型分布"].get(node_type, 0) + 1

        # 关系类型分布
        for rel in self.relationships.values():
            rel_type = rel.relationship_type.value
            stats["关系类型分布"][rel_type] = stats["关系类型分布"].get(rel_type, 0) + 1

        # 语言分布
        for node in self.nodes.values():
            if node.language:
                lang = node.language
                stats["语言分布"][lang] = stats["语言分布"].get(lang, 0) + 1

        return stats

    def export_to_dict(self) -> Dict[str, Any]:
        """导出为字典格式"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "domain": self.domain,
            "version": self.version,
            "language": self.language,
            "nodes": {node_id: node.dict() for node_id, node in self.nodes.items()},
            "relationships": {rel_id: rel.dict() for rel_id, rel in self.relationships.items()},
            "statistics": self.calculate_statistics()
        }

    @classmethod
    def import_from_dict(cls, data: Dict[str, Any]) -> "KnowledgeGraph":
        """从字典导入知识图谱"""
        kg = cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            domain=data.get("domain"),
            version=data.get("version", "1.0.0"),
            language=data.get("language")
        )

        # 导入节点
        for node_data in data.get("nodes", {}).values():
            node = KnowledgeNode(**node_data)
            kg.add_node(node)

        # 导入关系
        for rel_data in data.get("relationships", {}).values():
            relationship = KnowledgeRelationship(**rel_data)
            kg.add_relationship(relationship)

        return kg