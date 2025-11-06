#!/usr/bin/env python3
"""
创建示例数据 - 直接使用Neo4j浏览器创建

由于Cypher语法问题，我们通过简单的API调用创建基础数据
"""

import json
import requests

def create_simple_node():
    """创建一个简单的C++概念节点"""

    # 简化的节点数据
    node_data = {
        "id": "cpp_hello_world",
        "name": "Hello World程序",
        "node_type": "concept",
        "description": "C++的Hello World程序是学习C++的第一个程序",
        "category": "基础概念",
        "language": "cpp",
        "difficulty_level": "beginner",
        "examples": ["#include <iostream>", "int main() { std::cout << \"Hello World!\" << std::endl; return 0; }"]
    }

    try:
        response = requests.post("http://localhost:5000/api/nodes", json=node_data)
        if response.status_code == 201:
            print("✓ 成功创建Hello World节点")
            return True
        else:
            print(f"✗ 创建节点失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"✗ 创建节点异常: {e}")
        return False

def check_system():
    """检查系统状态"""
    try:
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            health_data = response.json()
            print("✓ 系统运行正常")
            print(f"  API状态: {health_data.get('status')}")
            print(f"  数据库: {health_data.get('database')}")

            # 获取统计信息
            stats_response = requests.get("http://localhost:5000/api/statistics")
            if stats_response.status_code == 200:
                stats = stats_response.json().get('data', {})
                print(f"  当前节点数: {stats.get('节点数量', 0)}")
                print(f"  当前关系数: {stats.get('关系数量', 0)}")

            return True
        else:
            print(f"✗ 系统异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 系统检查异常: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("CS Knowledge Graph - 示例数据创建")
    print("=" * 50)

    # 检查系统状态
    if not check_system():
        print("❌ 系统不可用，请确保API服务器正在运行")
        return

    print("\n尝试创建示例节点...")
    if create_simple_node():
        print("\n🎉 示例节点创建成功！")
        print("\n📋 您现在可以:")
        print("1. 访问API健康检查: http://localhost:5000/health")
        print("2. 查看统计信息: http://localhost:5000/api/statistics")
        print("3. 搜索Hello World: http://localhost:5000/api/nodes?search=hello")
        print("4. 访问Neo4j浏览器: http://localhost:7474")
        print("   - 用户名: neo4j")
        print("   - 密码: password")
        print("\n💡 提示: 在Neo4j浏览器中运行以下查询:")
        print("   MATCH (n) RETURN n")
        print("   MATCH (n) WHERE n.name CONTAINS 'Hello' RETURN n")
    else:
        print("\n❌ 示例节点创建失败")
        print("   请检查系统日志以获取详细错误信息")

if __name__ == '__main__':
    main()