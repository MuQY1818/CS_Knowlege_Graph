"""
Models module - 数据模型模块

定义知识图谱的数据模型和结构。

主要包含：
- KnowledgeNode: 知识节点模型
- KnowledgeRelationship: 知识关系模型
- KnowledgeGraph: 知识图谱模型
"""

from .knowledge_node import (
    KnowledgeNode,
    NodeType,
    DifficultyLevel,
    ConceptNode,
    LanguageNode,
    TechnologyNode,
    LibraryNode,
    create_node
)
from .knowledge_relationship import (
    KnowledgeRelationship,
    RelationshipType,
    RelationshipStrength,
    LearningPathRelationship,
    DependencyRelationship,
    ImplementationRelationship,
    create_relationship
)
from .knowledge_graph import KnowledgeGraph

__all__ = [
    # Node models
    'KnowledgeNode',
    'NodeType',
    'DifficultyLevel',
    'ConceptNode',
    'LanguageNode',
    'TechnologyNode',
    'LibraryNode',
    'create_node',

    # Relationship models
    'KnowledgeRelationship',
    'RelationshipType',
    'RelationshipStrength',
    'LearningPathRelationship',
    'DependencyRelationship',
    'ImplementationRelationship',
    'create_relationship',

    # Graph model
    'KnowledgeGraph',
]