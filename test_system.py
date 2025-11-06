#!/usr/bin/env python3
"""
System Test - 系统测试脚本

测试CS Knowledge Graph系统的基本功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """测试模块导入"""
    print("1. 测试模块导入...")
    try:
        # 测试基础模块导入
        from src.models import KnowledgeNode, NodeType, KnowledgeRelationship, RelationshipType
        from src.config import get_config
        from src.core.database_manager import DatabaseManager
        from src.core.knowledge_graph_manager import KnowledgeGraphManager
        from src.data.data_importer import DataImporter
        from src.visualization.graph_visualizer import GraphVisualizer
        print("   ✓ 所有模块导入成功")
        return True
    except Exception as e:
        print(f"   ✗ 模块导入失败: {e}")
        return False

def test_data_models():
    """测试数据模型"""
    print("2. 测试数据模型...")
    try:
        from src.models import KnowledgeNode, NodeType, DifficultyLevel

        # 创建测试节点
        node = KnowledgeNode(
            id="test_node",
            name="测试节点",
            node_type=NodeType.CONCEPT,
            description="这是一个测试节点",
            difficulty_level=DifficultyLevel.BEGINNER,
            language="cpp"
        )

        print(f"   ✓ 节点创建成功: {node.name} ({node.node_type})")
        return True
    except Exception as e:
        print(f"   ✗ 数据模型测试失败: {e}")
        return False

def test_cpp_data_loading():
    """测试C++数据加载"""
    print("3. 测试C++数据加载...")
    try:
        data_file = project_root / "data" / "raw" / "cpp_knowledge_data.json"
        if data_file.exists():
            import json
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            node_count = len(data.get('nodes', []))
            rel_count = len(data.get('relationships', []))

            print(f"   ✓ C++数据加载成功: {node_count} 个节点, {rel_count} 个关系")

            # 显示一些示例节点
            nodes = data.get('nodes', [])[:3]
            for node in nodes:
                print(f"     - {node['name']} ({node['node_type']})")

            return True
        else:
            print(f"   ✗ C++数据文件不存在: {data_file}")
            return False
    except Exception as e:
        print(f"   ✗ C++数据加载失败: {e}")
        return False

def test_visualization():
    """测试可视化功能"""
    print("4. 测试可视化功能...")
    try:
        from src.visualization.graph_visualizer import GraphVisualizer

        visualizer = GraphVisualizer()

        # 加载测试数据
        data_file = project_root / "data" / "raw" / "cpp_knowledge_data.json"
        if data_file.exists():
            import json
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            nodes = data.get('nodes', [])[:10]  # 只测试前10个节点
            relationships = data.get('relationships', [])[:10]

            # 创建图对象
            import networkx as nx
            G = visualizer.create_networkx_graph(nodes, relationships)

            print(f"   ✓ 可视化模块测试成功: 创建了包含 {G.number_of_nodes()} 个节点的图")
            return True
        else:
            print("   ✗ 无法测试可视化: C++数据文件不存在")
            return False
    except Exception as e:
        print(f"   ✗ 可视化测试失败: {e}")
        return False

def test_api_creation():
    """测试API应用创建"""
    print("5. 测试API应用创建...")
    try:
        from src.api.app import create_app

        app = create_app('testing')
        print("   ✓ Flask应用创建成功")

        # 测试路由配置
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(rule.rule)

        print(f"   ✓ API路由配置成功: 共 {len(routes)} 个路由")
        for route in routes[:5]:  # 显示前5个路由
            print(f"     - {route}")

        return True
    except Exception as e:
        print(f"   ✗ API应用创建失败: {e}")
        return False

def test_configuration():
    """测试配置模块"""
    print("6. 测试配置模块...")
    try:
        from src.config import get_config, Config

        # 测试默认配置
        config = get_config()
        print(f"   ✓ 配置加载成功: API端口 {config.API_PORT}")

        # 测试配置验证
        if hasattr(config, 'validate'):
            is_valid = config.validate()
            print(f"   ✓ 配置验证: {'通过' if is_valid else '失败'}")

        return True
    except Exception as e:
        print(f"   ✗ 配置测试失败: {e}")
        return False

def main():
    """运行所有测试"""
    print("=" * 50)
    print("CS Knowledge Graph 系统测试")
    print("=" * 50)

    tests = [
        test_imports,
        test_data_models,
        test_cpp_data_loading,
        test_visualization,
        test_api_creation,
        test_configuration
    ]

    passed = 0
    total = len(tests)

    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"   ✗ 测试异常: {e}")
        print()

    print("=" * 50)
    print(f"测试结果: {passed}/{total} 通过")

    if passed == total:
        print("🎉 所有测试通过！系统运行正常。")
        print("\n下一步操作:")
        print("1. 启动API服务器: python main.py")
        print("2. 访问API文档: http://localhost:5000/health")
        print("3. 查看使用指南: docs/USAGE.md")
    else:
        print("❌ 部分测试失败，请检查错误信息。")

    print("=" * 50)

if __name__ == '__main__':
    main()