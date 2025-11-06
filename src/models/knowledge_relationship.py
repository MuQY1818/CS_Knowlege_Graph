"""
Knowledge Relationship Model - 知识关系模型

定义知识图谱中节点间的关系类型和结构。
"""

from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class RelationshipType(str, Enum):
    """关系类型枚举"""
    # 层次关系
    BELONGS_TO = "belongs_to"           # 属于
    IS_A = "is_a"                      # 是一种
    PART_OF = "part_of"                # 是...的一部分
    CONTAINS = "contains"              # 包含

    # 依赖关系
    DEPENDS_ON = "depends_on"          # 依赖于
    REQUIRES = "requires"              # 需要
    PREREQUISITE = "prerequisite"      # 前置条件

    # 实现关系
    IMPLEMENTS = "implements"          # 实现
    USES = "uses"                      # 使用
    EXTENDS = "extends"                # 扩展
    INHERITS = "inherits"              # 继承

    # 关联关系
    RELATED_TO = "related_to"          # 相关
    SIMILAR_TO = "similar_to"          # 相似
    OPPOSITE_OF = "opposite_of"        # 相反
    CONTRASTS_WITH = "contrasts_with"  # 对比

    # 时序关系
    BEFORE = "before"                  # 之前
    AFTER = "after"                    # 之后
    LEADS_TO = "leads_to"              # 导致

    # 学习关系
    LEARNING_PATH = "learning_path"    # 学习路径
    RECOMMENDED_AFTER = "recommended_after"  # 推荐之后学习
    BUILD_UPON = "build_upon"          # 建立在...基础上

    # 实践关系
    APPLIES_TO = "applies_to"          # 应用于
    SOLVES = "solves"                  # 解决
    EXAMPLE_OF = "example_of"          # ...的示例

    # 评价关系
    GOOD_PRACTICE = "good_practice"    # 好的实践
    BAD_PRACTICE = "bad_practice"      # 坏的实践
    ALTERNATIVE_TO = "alternative_to"  # 替代方案


class RelationshipStrength(str, Enum):
    """关系强度枚举"""
    WEAK = "weak"           # 弱关系
    MODERATE = "moderate"   # 中等关系
    STRONG = "strong"       # 强关系
    CRITICAL = "critical"   # 关键关系


class KnowledgeRelationship(BaseModel):
    """知识关系模型"""

    # 基本信息
    id: str = Field(..., description="关系唯一标识符")
    source_id: str = Field(..., description="源节点ID")
    target_id: str = Field(..., description="目标节点ID")
    relationship_type: RelationshipType = Field(..., description="关系类型")

    # 关系属性
    strength: Optional[RelationshipStrength] = Field(RelationshipStrength.MODERATE, description="关系强度")
    weight: Optional[float] = Field(1.0, description="关系权重", ge=0.0, le=1.0)
    bidirectional: bool = Field(False, description="是否为双向关系")

    # 描述信息
    description: Optional[str] = Field(None, description="关系描述")
    examples: list[str] = Field(default_factory=list, description="关系示例")

    # 元数据
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")
    created_by: Optional[str] = Field(None, description="创建者")

    # 额外属性
    properties: Dict[str, Any] = Field(default_factory=dict, description="额外属性")

    # 可视化相关
    color: Optional[str] = Field(None, description="关系颜色")
    style: Optional[str] = Field(None, description="关系样式")
    label: Optional[str] = Field(None, description="关系标签")


class LearningPathRelationship(KnowledgeRelationship):
    """学习路径关系"""
    relationship_type: RelationshipType = RelationshipType.LEARNING_PATH

    # 学习路径特有属性
    order: int = Field(..., description="学习顺序")
    estimated_time: Optional[int] = Field(None, description="预计学习时间（分钟）")
    difficulty_progression: Optional[float] = Field(None, description="难度递进")


class DependencyRelationship(KnowledgeRelationship):
    """依赖关系"""
    relationship_type: RelationshipType = RelationshipType.DEPENDS_ON

    # 依赖特有属性
    dependency_level: Optional[str] = Field(None, description="依赖级别")
    critical_path: bool = Field(False, description="是否为关键路径")
    alternative_solutions: list[str] = Field(default_factory=list, description="替代解决方案")


class ImplementationRelationship(KnowledgeRelationship):
    """实现关系"""
    relationship_type: RelationshipType = RelationshipType.IMPLEMENTS

    # 实现特有属性
    implementation_details: Optional[str] = Field(None, description="实现细节")
    complexity: Optional[str] = Field(None, description="实现复杂度")
    performance_impact: Optional[str] = Field(None, description="性能影响")


# 关系类型映射
RELATIONSHIP_TYPE_MAPPING = {
    RelationshipType.LEARNING_PATH: LearningPathRelationship,
    RelationshipType.DEPENDS_ON: DependencyRelationship,
    RelationshipType.IMPLEMENTS: ImplementationRelationship,
}


def create_relationship(relationship_type: RelationshipType, **kwargs) -> KnowledgeRelationship:
    """根据关系类型创建对应的关系实例"""
    relationship_class = RELATIONSHIP_TYPE_MAPPING.get(relationship_type, KnowledgeRelationship)
    return relationship_class(relationship_type=relationship_type, **kwargs)