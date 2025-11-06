#!/usr/bin/env python3
"""
数据导入脚本 - 简化版本

通过API直接创建知识节点和关系
"""

import json
import requests
import time
from typing import Dict, Any, List

class KnowledgeGraphImporter:
    """知识图谱导入器"""

    def __init__(self, api_base_url: str = "http://localhost:5000"):
        """初始化导入器"""
        self.api_base_url = api_base_url
        self.session = requests.Session()

    def create_node(self, node_data: Dict[str, Any]) -> bool:
        """创建单个节点"""
        try:
            url = f"{self.api_base_url}/api/nodes"
            response = self.session.post(url, json=node_data)

            if response.status_code == 201:
                print(f"✓ 成功创建节点: {node_data.get('name', node_data.get('id'))}")
                return True
            else:
                print(f"✗ 创建节点失败: {node_data.get('name')} - {response.status_code}")
                print(f"  错误信息: {response.text}")
                return False
        except Exception as e:
            print(f"✗ 创建节点异常: {node_data.get('name')} - {e}")
            return False

    def create_relationship(self, rel_data: Dict[str, Any]) -> bool:
        """创建单个关系"""
        try:
            url = f"{self.api_base_url}/api/relationships"
            response = self.session.post(url, json=rel_data)

            if response.status_code == 201:
                print(f"✓ 成功创建关系: {rel_data.get('description', rel_data.get('id'))}")
                return True
            else:
                print(f"✗ 创建关系失败: {rel_data.get('description')} - {response.status_code}")
                print(f"  错误信息: {response.text}")
                return False
        except Exception as e:
            print(f"✗ 创建关系异常: {rel_data.get('description')} - {e}")
            return False

    def import_from_file(self, file_path: str) -> Dict[str, int]:
        """从文件导入数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            print(f"开始导入数据: {file_path}")
            print(f"元数据: {data.get('metadata', {})}")

            # 导入节点
            nodes = data.get('nodes', [])
            nodes_success = 0
            nodes_total = len(nodes)

            print(f"\n开始导入 {nodes_total} 个节点...")
            for i, node in enumerate(nodes, 1):
                print(f"[{i}/{nodes_total}] ", end="")
                if self.create_node(node):
                    nodes_success += 1
                time.sleep(0.1)  # 避免请求过快

            # 导入关系
            relationships = data.get('relationships', [])
            rels_success = 0
            rels_total = len(relationships)

            print(f"\n开始导入 {rels_total} 个关系...")
            for i, rel in enumerate(relationships, 1):
                print(f"[{i}/{rels_total}] ", end="")
                if self.create_relationship(rel):
                    rels_success += 1
                time.sleep(0.1)  # 避免请求过快

            print(f"\n导入完成:")
            print(f"  节点: {nodes_success}/{nodes_total}")
            print(f"  关系: {rels_success}/{rels_total}")

            return {
                'nodes_success': nodes_success,
                'nodes_total': nodes_total,
                'relationships_success': rels_success,
                'relationships_total': rels_total
            }

        except Exception as e:
            print(f"导入失败: {e}")
            return {
                'nodes_success': 0,
                'nodes_total': 0,
                'relationships_success': 0,
                'relationships_total': 0
            }

    def check_api_health(self) -> bool:
        """检查API健康状态"""
        try:
            url = f"{self.api_base_url}/health"
            response = self.session.get(url)
            if response.status_code == 200:
                health_data = response.json()
                print(f"✓ API健康检查通过")
                print(f"  状态: {health_data.get('status')}")
                print(f"  数据库: {health_data.get('database')}")
                return True
            else:
                print(f"✗ API健康检查失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ API健康检查异常: {e}")
            return False

    def get_statistics(self) -> Dict[str, Any]:
        """获取图谱统计信息"""
        try:
            url = f"{self.api_base_url}/api/statistics"
            response = self.session.get(url)
            if response.status_code == 200:
                return response.json().get('data', {})
            else:
                print(f"获取统计信息失败: {response.status_code}")
                return {}
        except Exception as e:
            print(f"获取统计信息异常: {e}")
            return {}


def main():
    """主函数"""
    print("=" * 60)
    print("CS Knowledge Graph 数据导入工具")
    print("=" * 60)

    # 创建导入器
    importer = KnowledgeGraphImporter()

    # 检查API健康状态
    if not importer.check_api_health():
        print("❌ API服务不可用，请确保知识图谱系统正在运行")
        print("   启动命令: python main.py")
        return

    # 获取当前统计信息
    print("\n当前图谱统计:")
    current_stats = importer.get_statistics()
    print(f"  节点数量: {current_stats.get('节点数量', 0)}")
    print(f"  关系数量: {current_stats.get('关系数量', 0)}")

    # 导入数据
    data_file = "data/cpp_knowledge_updated.json"
    result = importer.import_from_file(data_file)

    # 显示最终结果
    print("\n" + "=" * 60)
    print("导入结果总结:")
    print(f"  节点: {result['nodes_success']}/{result['nodes_total']} 成功")
    print(f"  关系: {result['relationships_success']}/{result['relationships_total']} 成功")

    if result['nodes_success'] > 0 or result['relationships_success'] > 0:
        print("\n✅ 数据导入成功！")

        # 获取更新后的统计信息
        print("\n更新后的图谱统计:")
        updated_stats = importer.get_statistics()
        print(f"  节点数量: {updated_stats.get('节点数量', 0)}")
        print(f"  关系数量: {updated_stats.get('关系数量', 0)}")

        print("\n🎉 您现在可以:")
        print("1. 访问健康检查: http://localhost:5000/health")
        print("2. 查看统计信息: http://localhost:5000/api/statistics")
        print("3. 搜索节点: http://localhost:5000/api/nodes?search=C++")
        print("4. 访问Neo4j浏览器: http://localhost:7474 (用户名: neo4j, 密码: password)")
    else:
        print("\n❌ 数据导入失败，请检查错误信息")

    print("=" * 60)


if __name__ == '__main__':
    main()