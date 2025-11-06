#!/usr/bin/env python3
"""
CS Knowledge Graph 系统演示

展示系统的各种功能
"""

import json
import requests
import time
from typing import Dict, Any

class KnowledgeGraphDemo:
    """知识图谱演示类"""

    def __init__(self, api_base_url: str = "http://localhost:5000"):
        self.api_base_url = api_base_url

    def check_health(self) -> bool:
        """检查系统健康状态"""
        try:
            response = requests.get(f"{self.api_base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print("✅ 系统健康检查通过")
                print(f"   状态: {data.get('status')}")
                print(f"   数据库: {data.get('database')}")
                return True
            else:
                print(f"❌ 健康检查失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 健康检查异常: {e}")
            return False

    def show_statistics(self):
        """显示系统统计信息"""
        try:
            response = requests.get(f"{self.api_base_url}/api/statistics")
            if response.status_code == 200:
                data = response.json()
                stats = data.get('data', {})
                print("\n📊 知识图谱统计信息:")
                print(f"   节点数量: {stats.get('节点数量', 0)}")
                print(f"   关系数量: {stats.get('关系数量', 0)}")

                node_types = stats.get('节点类型分布', {})
                if node_types:
                    print("   节点类型分布:")
                    for node_type, count in node_types.items():
                        print(f"     - {node_type}: {count}")

                return stats
            else:
                print(f"❌ 获取统计信息失败: {response.status_code}")
                return {}
        except Exception as e:
            print(f"❌ 获取统计信息异常: {e}")
            return {}

    def demo_search_functionality(self):
        """演示搜索功能"""
        print("\n🔍 演示搜索功能:")

        search_terms = ["C++", "基础", "语法", "概念", "编程"]

        for term in search_terms:
            try:
                response = requests.get(f"{self.api_base_url}/api/nodes?search={term}&limit=5")
                if response.status_code == 200:
                    data = response.json()
                    nodes = data.get('data', [])
                    print(f"   搜索 '{term}': 找到 {len(nodes)} 个结果")

                    for node in nodes[:2]:  # 显示前2个结果
                        print(f"     - {node.get('name')} ({node.get('node_type')})")
                else:
                    print(f"   搜索 '{term}' 失败: {response.status_code}")
            except Exception as e:
                print(f"   搜索 '{term}' 异常: {e}")

    def demo_node_operations(self):
        """演示节点操作"""
        print("\n📝 演示节点操作:")

        # 尝试获取不同类型的节点
        node_types = ['concept', 'language', 'library']

        for node_type in node_types:
            try:
                response = requests.get(f"{self.api_base_url}/api/nodes?type={node_type}&limit=3")
                if response.status_code == 200:
                    data = response.json()
                    nodes = data.get('data', [])
                    print(f"   {node_type} 类型节点: {len(nodes)} 个")

                    for node in nodes:
                        print(f"     - {node.get('name')} (难度: {node.get('difficulty_level', 'N/A')})")
                else:
                    print(f"   获取 {node_type} 节点失败: {response.status_code}")
            except Exception as e:
                print(f"   获取 {node_type} 节点异常: {e}")

    def show_api_endpoints(self):
        """显示所有可用的API端点"""
        print("\n🌐 可用的API端点:")

        endpoints = [
            ("GET", "/health", "健康检查"),
            ("GET", "/api/statistics", "获取统计信息"),
            ("GET", "/api/nodes", "获取节点列表"),
            ("GET", "/api/nodes/<id>", "获取单个节点"),
            ("GET", "/api/nodes/<id>/adjacent", "获取相邻节点"),
            ("POST", "/api/nodes", "创建节点"),
            ("PUT", "/api/nodes/<id>", "更新节点"),
            ("DELETE", "/api/nodes/<id>", "删除节点"),
            ("POST", "/api/relationships", "创建关系"),
            ("GET", "/api/path/<source>/<target>", "查找最短路径"),
            ("GET", "/api/learning-path/<id>", "获取学习路径"),
            ("POST", "/api/import", "导入数据"),
            ("GET", "/api/export", "导出数据")
        ]

        for method, endpoint, description in endpoints:
            url = f"http://localhost:5000{endpoint}"
            print(f"   {method:4} {endpoint:<30} - {description}")

    def show_neo4j_browser_queries(self):
        """显示Neo4j浏览器示例查询"""
        print("\n💻 Neo4j浏览器示例查询:")
        print("   URL: http://localhost:7474")
        print("   用户名: neo4j, 密码: password")
        print()

        queries = [
            ("查看所有节点", "MATCH (n) RETURN n LIMIT 25"),
            ("查看所有关系", "MATCH ()-[r]-() RETURN r LIMIT 25"),
            ("按类型统计节点", "MATCH (n) RETURN n.node_type, count(n)"),
            ("查找C++相关节点", "MATCH (n) WHERE n.language = 'cpp' RETURN n"),
            ("查找概念节点", "MATCH (n) WHERE n.node_type = 'concept' RETURN n"),
            ("查看节点和关系", "MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 10"),
            ("按难度统计", "MATCH (n) WHERE n.difficulty_level IS NOT NULL RETURN n.difficulty_level, count(n)")
        ]

        for description, query in queries:
            print(f"   {description}:")
            print(f"     {query}")
            print()

    def show_next_steps(self):
        """显示下一步操作建议"""
        print("\n🚀 下一步操作建议:")
        print("   1. 在Neo4j浏览器中手动创建一些C++知识节点")
        print("   2. 通过API接口添加更多知识点")
        print("   3. 使用可视化组件展示知识图谱")
        print("   4. 扩展到其他编程语言")
        print("   5. 添加智能问答功能")
        print()
        print("📚 学习资源:")
        print("   - Neo4j Cypher查询文档: https://neo4j.com/docs/cypher-manual/")
        print("   - C++参考文档: https://en.cppreference.com/")
        print("   - Flask API文档: https://flask.palletsprojects.com/")

    def run_demo(self):
        """运行完整演示"""
        print("=" * 60)
        print("CS Knowledge Graph 系统功能演示")
        print("=" * 60)

        # 健康检查
        if not self.check_health():
            print("❌ 系统不可用，请确保API服务器正在运行")
            print("   启动命令: python main.py")
            return

        # 显示统计信息
        self.show_statistics()

        # 演示搜索功能
        self.demo_search_functionality()

        # 演示节点操作
        self.demo_node_operations()

        # 显示API端点
        self.show_api_endpoints()

        # 显示Neo4j查询
        self.show_neo4j_browser_queries()

        # 显示下一步建议
        self.show_next_steps()

        print("=" * 60)
        print("🎉 演示完成！系统已准备就绪。")
        print("=" * 60)

if __name__ == '__main__':
    demo = KnowledgeGraphDemo()
    demo.run_demo()