#!/usr/bin/env python3
"""
创建演示数据脚本
"""

import requests
import json

def create_demo_data():
    """创建演示数据"""

    # C++基础知识点
    nodes = [
        {
            "id": "cpp_hello",
            "name": "Hello World",
            "node_type": "concept",
            "description": "C++ Hello World 程序",
            "category": "基础概念",
            "language": "cpp",
            "difficulty_level": "beginner"
        },
        {
            "id": "cpp_variables",
            "name": "变量",
            "node_type": "concept",
            "description": "C++中的变量声明和使用",
            "category": "基础概念",
            "language": "cpp",
            "difficulty_level": "beginner"
        },
        {
            "id": "cpp_loops",
            "name": "循环",
            "node_type": "concept",
            "description": "for循环和while循环",
            "category": "控制流程",
            "language": "cpp",
            "difficulty_level": "beginner"
        },
        {
            "id": "cpp_classes",
            "name": "类",
            "node_type": "concept",
            "description": "C++面向对象编程的类",
            "category": "面向对象",
            "language": "cpp",
            "difficulty_level": "intermediate"
        },
        {
            "id": "cpp_pointers",
            "name": "指针",
            "node_type": "concept",
            "description": "C++指针的概念和使用",
            "category": "内存管理",
            "language": "cpp",
            "difficulty_level": "advanced"
        },
        {
            "id": "cpp_vector",
            "name": "vector容器",
            "node_type": "concept",
            "description": "STL vector动态数组",
            "category": "STL容器",
            "language": "cpp",
            "difficulty_level": "intermediate"
        }
    ]

    # 创建关系
    relationships = [
        {
            "id": "hello_to_variables",
            "source_id": "cpp_hello",
            "target_id": "cpp_variables",
            "relationship_type": "leads_to",
            "description": "Hello World后学习变量"
        },
        {
            "id": "variables_to_loops",
            "source_id": "cpp_variables",
            "target_id": "cpp_loops",
            "relationship_type": "prerequisite",
            "description": "变量是循环的基础"
        },
        {
            "id": "loops_to_classes",
            "source_id": "cpp_loops",
            "target_id": "cpp_classes",
            "relationship_type": "builds_upon",
            "description": "循环后学习类"
        },
        {
            "id": "classes_to_pointers",
            "source_id": "cpp_classes",
            "target_id": "cpp_pointers",
            "relationship_type": "uses",
            "description": "类使用指针"
        },
        {
            "id": "variables_to_vector",
            "source_id": "cpp_variables",
            "target_id": "cpp_vector",
            "relationship_type": "related_to",
            "description": "变量与容器相关"
        }
    ]

    print("正在创建演示数据...")

    # 创建节点
    for node in nodes:
        try:
            response = requests.post("http://localhost:5000/api/nodes", json=node)
            if response.status_code == 201:
                print(f"✓ 创建节点: {node['name']}")
            else:
                print(f"✗ 创建节点失败: {node['name']} - {response.status_code}")
        except Exception as e:
            print(f"✗ 创建节点异常: {node['name']} - {e}")

    # 创建关系
    for rel in relationships:
        try:
            response = requests.post("http://localhost:5000/api/relationships", json=rel)
            if response.status_code == 201:
                print(f"✓ 创建关系: {rel['description']}")
            else:
                print(f"✗ 创建关系失败: {rel['description']} - {response.status_code}")
        except Exception as e:
            print(f"✗ 创建关系异常: {rel['description']} - {e}")

    print("演示数据创建完成!")

if __name__ == '__main__':
    create_demo_data()