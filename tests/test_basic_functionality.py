#!/usr/bin/env python3
"""
Basic Functionality Tests - 基础功能测试

测试知识图谱系统的基本功能。
"""

import sys
import os
import unittest
import json
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.models import KnowledgeNode, NodeType, KnowledgeRelationship, RelationshipType
from src.core import DatabaseManager, KnowledgeGraphManager
from src.data import DataImporter
from src.config import get_config


class TestBasicFunctionality(unittest.TestCase):
    """基础功能测试类"""

    @classmethod
    def setUpClass(cls):
        """测试类设置"""
        # 加载配置
        cls.config = get_config('testing')

        # 初始化数据库管理器
        cls.db_manager = DatabaseManager(cls.config)
        cls.connected = cls.db_manager.connect()

        if cls.connected:
            # 清空测试数据库
            cls.db_manager.clear_database()
            # 创建约束
            cls.db_manager.create_constraints()

            # 初始化知识图谱管理器
            cls.kg_manager = KnowledgeGraphManager(cls.db_manager)

    @classmethod
    def tearDownClass(cls):
        """测试类清理"""
        if cls.connected:
            # 清空测试数据库
            cls.db_manager.clear_database()
            # 断开连接
            cls.db_manager.disconnect()

    def setUp(self):
        """每个测试方法前的设置"""
        if not self.connected:
            self.skipTest("数据库连接失败")

    def test_database_connection(self):
        """测试数据库连接"""
        self.assertTrue(self.connected)

        # 获取数据库信息
        db_info = self.db_manager.get_database_info()
        self.assertIsInstance(db_info, dict)

    def test_create_node(self):
        """测试创建节点"""
        node_data = {
            'id': 'test_node_1',
            'name': '测试节点',
            'node_type': NodeType.CONCEPT,
            'description': '这是一个测试节点',
            'category': '测试',
            'language': 'cpp'
        }

        node = self.kg_manager.create_node(node_data)
        self.assertIsNotNone(node)
        self.assertEqual(node.id, 'test_node_1')
        self.assertEqual(node.name, '测试节点')

        # 验证节点可以通过查询获取
        retrieved_node = self.kg_manager.get_node('test_node_1')
        self.assertIsNotNone(retrieved_node)
        self.assertEqual(retrieved_node['id'], 'test_node_1')

    def test_create_relationship(self):
        """测试创建关系"""
        # 先创建两个节点
        node1_data = {
            'id': 'test_node_2',
            'name': '测试节点2',
            'node_type': NodeType.CONCEPT,
            'description': '这是第二个测试节点',
            'category': '测试',
            'language': 'cpp'
        }

        node2_data = {
            'id': 'test_node_3',
            'name': '测试节点3',
            'node_type': NodeType.CONCEPT,
            'description': '这是第三个测试节点',
            'category': '测试',
            'language': 'cpp'
        }

        self.kg_manager.create_node(node1_data)
        self.kg_manager.create_node(node2_data)

        # 创建关系
        rel_data = {
            'id': 'test_rel_1',
            'source_id': 'test_node_2',
            'target_id': 'test_node_3',
            'relationship_type': RelationshipType.RELATED_TO,
            'description': '测试关系'
        }

        relationship = self.kg_manager.create_relationship(rel_data)
        self.assertIsNotNone(relationship)
        self.assertEqual(relationship.id, 'test_rel_1')

    def test_search_nodes(self):
        """测试节点搜索"""
        # 创建测试节点
        node_data = {
            'id': 'test_search_node',
            'name': '搜索测试节点',
            'node_type': NodeType.CONCEPT,
            'description': '用于搜索功能的测试节点',
            'category': '搜索测试',
            'language': 'cpp'
        }

        self.kg_manager.create_node(node_data)

        # 搜索节点
        results = self.kg_manager.search_nodes('搜索')
        self.assertGreater(len(results), 0)

        # 验证搜索结果包含创建的节点
        found = any(node['id'] == 'test_search_node' for node in results)
        self.assertTrue(found)

    def test_get_nodes_by_type(self):
        """测试根据类型获取节点"""
        # 创建不同类型的节点
        concept_data = {
            'id': 'test_concept',
            'name': '测试概念',
            'node_type': NodeType.CONCEPT,
            'description': '测试概念节点',
            'language': 'cpp'
        }

        library_data = {
            'id': 'test_library',
            'name': '测试库',
            'node_type': NodeType.LIBRARY,
            'description': '测试库节点',
            'language': 'cpp'
        }

        self.kg_manager.create_node(concept_data)
        self.kg_manager.create_node(library_data)

        # 根据类型获取节点
        concepts = self.kg_manager.get_nodes_by_type(NodeType.CONCEPT)
        libraries = self.kg_manager.get_nodes_by_type(NodeType.LIBRARY)

        self.assertGreater(len(concepts), 0)
        self.assertGreater(len(libraries), 0)

    def test_get_adjacent_nodes(self):
        """测试获取相邻节点"""
        # 创建节点和关系
        node1_data = {
            'id': 'test_adjacent_1',
            'name': '相邻测试节点1',
            'node_type': NodeType.CONCEPT,
            'description': '相邻测试节点1',
            'language': 'cpp'
        }

        node2_data = {
            'id': 'test_adjacent_2',
            'name': '相邻测试节点2',
            'node_type': NodeType.CONCEPT,
            'description': '相邻测试节点2',
            'language': 'cpp'
        }

        self.kg_manager.create_node(node1_data)
        self.kg_manager.create_node(node2_data)

        rel_data = {
            'id': 'test_adjacent_rel',
            'source_id': 'test_adjacent_1',
            'target_id': 'test_adjacent_2',
            'relationship_type': RelationshipType.RELATED_TO,
            'description': '相邻测试关系'
        }

        self.kg_manager.create_relationship(rel_data)

        # 获取相邻节点
        adjacent = self.kg_manager.get_adjacent_nodes('test_adjacent_1')
        self.assertEqual(len(adjacent), 1)
        self.assertEqual(adjacent[0][0]['id'], 'test_adjacent_2')

    def test_update_node(self):
        """测试更新节点"""
        # 创建节点
        node_data = {
            'id': 'test_update_node',
            'name': '更新测试节点',
            'node_type': NodeType.CONCEPT,
            'description': '原始描述',
            'language': 'cpp'
        }

        self.kg_manager.create_node(node_data)

        # 更新节点
        updates = {
            'description': '更新后的描述',
            'category': '更新测试'
        }

        success = self.kg_manager.update_node('test_update_node', updates)
        self.assertTrue(success)

        # 验证更新
        updated_node = self.kg_manager.get_node('test_update_node')
        self.assertEqual(updated_node['description'], '更新后的描述')
        self.assertEqual(updated_node['category'], '更新测试')

    def test_statistics(self):
        """测试统计信息"""
        # 创建一些测试数据
        for i in range(5):
            node_data = {
                'id': f'stat_test_node_{i}',
                'name': f'统计测试节点{i}',
                'node_type': NodeType.CONCEPT,
                'description': f'统计测试节点{i}',
                'language': 'cpp'
            }
            self.kg_manager.create_node(node_data)

        # 获取统计信息
        stats = self.kg_manager.get_statistics()
        self.assertIsInstance(stats, dict)
        self.assertIn('node_count', stats)
        self.assertGreater(stats['node_count'], 0)


class TestDataImport(unittest.TestCase):
    """数据导入测试类"""

    @classmethod
    def setUpClass(cls):
        """测试类设置"""
        cls.config = get_config('testing')
        cls.db_manager = DatabaseManager(cls.config)
        cls.connected = cls.db_manager.connect()

        if cls.connected:
            cls.db_manager.clear_database()
            cls.db_manager.create_constraints()
            cls.kg_manager = KnowledgeGraphManager(cls.db_manager)
            cls.data_importer = DataImporter(cls.kg_manager)

    @classmethod
    def tearDownClass(cls):
        """测试类清理"""
        if cls.connected:
            cls.db_manager.clear_database()
            cls.db_manager.disconnect()

    def setUp(self):
        """每个测试方法前的设置"""
        if not self.connected:
            self.skipTest("数据库连接失败")

    def test_import_cpp_data(self):
        """测试导入C++数据"""
        cpp_data_file = project_root / "data" / "raw" / "cpp_knowledge_data.json"
        if cpp_data_file.exists():
            result = self.data_importer.import_from_json(str(cpp_data_file))
            self.assertIsInstance(result, dict)
            self.assertIn('nodes', result)
            self.assertIn('relationships', result)
            self.assertGreater(result['nodes'], 0)
        else:
            self.skipTest("C++数据文件不存在")


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    test_suite = unittest.TestSuite()

    # 添加测试类
    test_suite.addTest(unittest.makeSuite(TestBasicFunctionality))
    test_suite.addTest(unittest.makeSuite(TestDataImport))

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # 返回测试结果
    return result.wasSuccessful()


if __name__ == '__main__':
    print("开始运行CS Knowledge Graph基础功能测试...")
    success = run_tests()
    if success:
        print("\n所有测试通过!")
    else:
        print("\n部分测试失败!")
        sys.exit(1)