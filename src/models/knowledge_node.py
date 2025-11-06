"""
Knowledge Node Model - 知识节点模型

定义知识图谱中的节点结构和属性。
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class NodeType(str, Enum):
    """节点类型枚举"""
    CONCEPT = "concept"         # 概念
    LANGUAGE = "language"       # 编程语言
    TECHNOLOGY = "technology"   # 技术
    LIBRARY = "library"         # 库/框架
    TOOL = "tool"              # 工具
    PARADIGM = "paradigm"      # 编程范式
    PATTERN = "pattern"        # 设计模式
    ALGORITHM = "algorithm"    # 算法
    DATA_STRUCTURE = "data_structure"  # 数据结构
    PROBLEM = "problem"        # 问题
    SOLUTION = "solution"      # 解决方案
    BEST_PRACTICE = "best_practice"  # 最佳实践
    COMMON_MISTAKE = "common_mistake" # 常见错误


class DifficultyLevel(str, Enum):
    """难度级别枚举"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class KnowledgeNode(BaseModel):
    """知识节点模型"""

    # 基本信息
    id: str = Field(..., description="节点唯一标识符")
    name: str = Field(..., description="节点名称")
    node_type: NodeType = Field(..., description="节点类型")
    description: str = Field(..., description="节点描述")

    # 学习相关
    difficulty_level: Optional[DifficultyLevel] = Field(None, description="难度级别")
    prerequisites: List[str] = Field(default_factory=list, description="前置知识节点ID列表")
    learning_time: Optional[int] = Field(None, description="预计学习时间（分钟）")

    # 分类和标签
    category: Optional[str] = Field(None, description="主要分类")
    subcategory: Optional[str] = Field(None, description="子分类")
    tags: List[str] = Field(default_factory=list, description="标签列表")

    # 语言特定
    language: Optional[str] = Field(None, description="相关编程语言")

    # 元数据
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")
    created_by: Optional[str] = Field(None, description="创建者")

    # 额外属性
    properties: Dict[str, Any] = Field(default_factory=dict, description="额外属性")

    # 可视化相关
    color: Optional[str] = Field(None, description="节点颜色")
    size: Optional[int] = Field(None, description="节点大小")
    icon: Optional[str] = Field(None, description="节点图标")


class ConceptNode(KnowledgeNode):
    """概念节点"""
    node_type: NodeType = NodeType.CONCEPT

    # 概念特有属性
    definition: Optional[str] = Field(None, description="正式定义")
    examples: List[str] = Field(default_factory=list, description="示例")
    related_concepts: List[str] = Field(default_factory=list, description="相关概念")


class LanguageNode(KnowledgeNode):
    """编程语言节点"""
    node_type: NodeType = NodeType.LANGUAGE

    # 语言特有属性
    version: Optional[str] = Field(None, description="语言版本")
    paradigm: List[str] = Field(default_factory=list, description="支持的编程范式")
    typing_system: Optional[str] = Field(None, description="类型系统")
    memory_management: Optional[str] = Field(None, description="内存管理方式")
    use_cases: List[str] = Field(default_factory=list, description="典型用例")


class TechnologyNode(KnowledgeNode):
    """技术节点"""
    node_type: NodeType = NodeType.TECHNOLOGY

    # 技术特有属性
    domain: Optional[str] = Field(None, description="技术领域")
    maturity: Optional[str] = Field(None, description="成熟度")
    alternatives: List[str] = Field(default_factory=list, description="替代技术")
    advantages: List[str] = Field(default_factory=list, description="优势")
    disadvantages: List[str] = Field(default_factory=list, description="劣势")


class LibraryNode(KnowledgeNode):
    """库/框架节点"""
    node_type: NodeType = NodeType.LIBRARY

    # 库特有属性
    version: Optional[str] = Field(None, description="版本")
    license: Optional[str] = Field(None, description="许可证")
    repository_url: Optional[str] = Field(None, description="代码仓库URL")
    documentation_url: Optional[str] = Field(None, description="文档URL")
    dependencies: List[str] = Field(default_factory=list, description="依赖")


# 节点类型映射
NODE_TYPE_MAPPING = {
    NodeType.CONCEPT: ConceptNode,
    NodeType.LANGUAGE: LanguageNode,
    NodeType.TECHNOLOGY: TechnologyNode,
    NodeType.LIBRARY: LibraryNode,
}


def create_node(node_type: NodeType, **kwargs) -> KnowledgeNode:
    """根据节点类型创建对应的节点实例"""
    node_class = NODE_TYPE_MAPPING.get(node_type, KnowledgeNode)
    return node_class(node_type=node_type, **kwargs)