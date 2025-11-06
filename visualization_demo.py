#!/usr/bin/env python3
"""
知识图谱可视化演示

直接创建可视化图表展示系统状态
"""

import json
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx
import matplotlib.pyplot as plt
from src.visualization.graph_visualizer import GraphVisualizer
from src.models import KnowledgeNode, NodeType, RelationshipType
import numpy as np

def create_cpp_knowledge_graph():
    """创建C++知识图谱数据"""

    nodes = [
        # 基础概念
        KnowledgeNode(
            id="cpp_hello",
            name="Hello World",
            node_type=NodeType.CONCEPT,
            description="第一个C++程序，包含基本语法结构",
            category="基础概念",
            language="cpp",
            difficulty_level="beginner"
        ),
        KnowledgeNode(
            id="cpp_variables",
            name="变量与数据类型",
            node_type=NodeType.CONCEPT,
            description="int, float, double, char, bool等基本数据类型",
            category="基础概念",
            language="cpp",
            difficulty_level="beginner"
        ),
        KnowledgeNode(
            id="cpp_operators",
            name="运算符",
            node_type=NodeType.CONCEPT,
            description="算术、关系、逻辑、位运算符",
            category="基础概念",
            language="cpp",
            difficulty_level="beginner"
        ),
        KnowledgeNode(
            id="cpp_io",
            name="输入输出流",
            node_type=NodeType.CONCEPT,
            description="cin, cout, iostream库的使用",
            category="基础概念",
            language="cpp",
            difficulty_level="beginner"
        ),

        # 控制流程
        KnowledgeNode(
            id="cpp_conditionals",
            name="条件语句",
            node_type=NodeType.CONCEPT,
            description="if-else, switch-case条件判断",
            category="控制流程",
            language="cpp",
            difficulty_level="beginner"
        ),
        KnowledgeNode(
            id="cpp_loops",
            name="循环结构",
            node_type=NodeType.CONCEPT,
            description="for, while, do-while循环",
            category="控制流程",
            language="cpp",
            difficulty_level="beginner"
        ),
        KnowledgeNode(
            id="cpp_jump",
            name="跳转语句",
            node_type=NodeType.CONCEPT,
            description="break, continue, goto语句",
            category="控制流程",
            language="cpp",
            difficulty_level="beginner"
        ),

        # 函数
        KnowledgeNode(
            id="cpp_functions",
            name="函数基础",
            node_type=NodeType.CONCEPT,
            description="函数定义、声明、调用、参数传递",
            category="函数",
            language="cpp",
            difficulty_level="beginner"
        ),
        KnowledgeNode(
            id="cpp_function_overloading",
            name="函数重载",
            node_type=NodeType.CONCEPT,
            description="同名函数不同参数的重载机制",
            category="函数",
            language="cpp",
            difficulty_level="intermediate"
        ),
        KnowledgeNode(
            id="cpp_recursion",
            name="递归函数",
            node_type=NodeType.CONCEPT,
            description="函数调用自身的递归编程",
            category="函数",
            language="cpp",
            difficulty_level="intermediate"
        ),

        # 数组和字符串
        KnowledgeNode(
            id="cpp_arrays",
            name="数组",
            node_type=NodeType.CONCEPT,
            description="一维和多维数组的使用",
            category="数据结构",
            language="cpp",
            difficulty_level="beginner"
        ),
        KnowledgeNode(
            id="cpp_strings",
            name="字符串处理",
            node_type=NodeType.CONCEPT,
            description="C风格字符串和string类",
            category="数据结构",
            language="cpp",
            difficulty_level="beginner"
        ),

        # 指针和内存管理
        KnowledgeNode(
            id="cpp_pointers",
            name="指针基础",
            node_type=NodeType.CONCEPT,
            description="指针概念、声明、使用和算术运算",
            category="内存管理",
            language="cpp",
            difficulty_level="intermediate"
        ),
        KnowledgeNode(
            id="cpp_dynamic_memory",
            name="动态内存分配",
            node_type=NodeType.CONCEPT,
            description="new, delete操作符，堆内存管理",
            category="内存管理",
            language="cpp",
            difficulty_level="intermediate"
        ),
        KnowledgeNode(
            id="cpp_smart_pointers",
            name="智能指针",
            node_type=NodeType.CONCEPT,
            description="unique_ptr, shared_ptr, weak_ptr",
            category="现代C++",
            language="cpp",
            difficulty_level="advanced"
        ),

        # 面向对象编程
        KnowledgeNode(
            id="cpp_classes",
            name="类与对象",
            node_type=NodeType.CONCEPT,
            description="类的定义、对象的创建和使用",
            category="面向对象",
            language="cpp",
            difficulty_level="intermediate"
        ),
        KnowledgeNode(
            id="cpp_constructors",
            name="构造函数与析构函数",
            node_type=NodeType.CONCEPT,
            description="对象生命周期管理",
            category="面向对象",
            language="cpp",
            difficulty_level="intermediate"
        ),
        KnowledgeNode(
            id="cpp_inheritance",
            name="继承",
            node_type=NodeType.CONCEPT,
            description="单继承、多继承、虚继承",
            category="面向对象",
            language="cpp",
            difficulty_level="intermediate"
        ),
        KnowledgeNode(
            id="cpp_polymorphism",
            name="多态",
            node_type=NodeType.CONCEPT,
            description="虚函数、纯虚函数、抽象类",
            category="面向对象",
            language="cpp",
            difficulty_level="advanced"
        ),
        KnowledgeNode(
            id="cpp_encapsulation",
            name="封装",
            node_type=NodeType.CONCEPT,
            description="public, private, protected访问控制",
            category="面向对象",
            language="cpp",
            difficulty_level="intermediate"
        ),

        # STL容器
        KnowledgeNode(
            id="cpp_vector",
            name="vector动态数组",
            node_type=NodeType.CONCEPT,
            description="可变大小数组，随机访问容器",
            category="STL容器",
            language="cpp",
            difficulty_level="intermediate"
        ),
        KnowledgeNode(
            id="cpp_list",
            name="list双向链表",
            node_type=NodeType.CONCEPT,
            description="双向链表，高效插入删除",
            category="STL容器",
            language="cpp",
            difficulty_level="intermediate"
        ),
        KnowledgeNode(
            id="cpp_map",
            name="map映射",
            node_type=NodeType.CONCEPT,
            description="键值对存储，自动排序",
            category="STL容器",
            language="cpp",
            difficulty_level="intermediate"
        ),
        KnowledgeNode(
            id="cpp_set",
            name="set集合",
            node_type=NodeType.CONCEPT,
            description="唯一元素集合，自动排序",
            category="STL容器",
            language="cpp",
            difficulty_level="intermediate"
        ),

        # 算法
        KnowledgeNode(
            id="cpp_algorithms",
            name="STL算法",
            node_type=NodeType.CONCEPT,
            description="sort, find, copy等标准算法",
            category="算法",
            language="cpp",
            difficulty_level="intermediate"
        ),
        KnowledgeNode(
            id="cpp_iterators",
            name="迭代器",
            node_type=NodeType.CONCEPT,
            description="容器和算法之间的桥梁",
            category="算法",
            language="cpp",
            difficulty_level="intermediate"
        ),

        # 模板编程
        KnowledgeNode(
            id="cpp_templates",
            name="模板基础",
            node_type=NodeType.CONCEPT,
            description="函数模板和类模板",
            category="模板编程",
            language="cpp",
            difficulty_level="advanced"
        ),
        KnowledgeNode(
            id="cpp_template_specialization",
            name="模板特化",
            node_type=NodeType.CONCEPT,
            description="全特化和偏特化",
            category="模板编程",
            language="cpp",
            difficulty_level="advanced"
        ),

        # 现代C++特性
        KnowledgeNode(
            id="cpp_lambda",
            name="Lambda表达式",
            node_type=NodeType.CONCEPT,
            description="匿名函数和闭包",
            category="现代C++",
            language="cpp",
            difficulty_level="advanced"
        ),
        KnowledgeNode(
            id="cpp_auto",
            name="auto关键字",
            node_type=NodeType.CONCEPT,
            description="类型推导和简化代码",
            category="现代C++",
            language="cpp",
            difficulty_level="intermediate"
        ),
        KnowledgeNode(
            id="cpp_range_for",
            name="范围for循环",
            node_type=NodeType.CONCEPT,
            description="基于范围的for循环语法",
            category="现代C++",
            language="cpp",
            difficulty_level="intermediate"
        ),

        # 异常处理
        KnowledgeNode(
            id="cpp_exceptions",
            name="异常处理",
            node_type=NodeType.CONCEPT,
            description="try-catch-finally异常处理机制",
            category="错误处理",
            language="cpp",
            difficulty_level="advanced"
        ),

        # 文件操作
        KnowledgeNode(
            id="cpp_file_io",
            name="文件操作",
            node_type=NodeType.CONCEPT,
            description="fstream文件读写操作",
            category="文件处理",
            language="cpp",
            difficulty_level="intermediate"
        ),

        # 多线程
        KnowledgeNode(
            id="cpp_threads",
            name="多线程编程",
            node_type=NodeType.CONCEPT,
            description="thread, mutex, condition_variable",
            category="并发编程",
            language="cpp",
            difficulty_level="advanced"
        )
    ]

    return nodes

def create_sample_relationships():
    """创建示例关系"""

    return [
        # 基础概念之间的学习路径
        {'source_id': 'cpp_hello', 'target_id': 'cpp_variables', 'relationship_type': 'leads_to', 'description': 'Hello World后学习变量'},
        {'source_id': 'cpp_variables', 'target_id': 'cpp_operators', 'relationship_type': 'prerequisite', 'description': '变量需要运算符操作'},
        {'source_id': 'cpp_operators', 'target_id': 'cpp_io', 'relationship_type': 'used_in', 'description': '运算符用于输入输出'},
        {'source_id': 'cpp_variables', 'target_id': 'cpp_arrays', 'relationship_type': 'extends_to', 'description': '变量扩展到数组'},
        {'source_id': 'cpp_variables', 'target_id': 'cpp_strings', 'relationship_type': 'extends_to', 'description': '变量扩展到字符串'},

        # 控制流程学习路径
        {'source_id': 'cpp_variables', 'target_id': 'cpp_conditionals', 'relationship_type': 'prerequisite', 'description': '变量是条件判断的基础'},
        {'source_id': 'cpp_conditionals', 'target_id': 'cpp_loops', 'relationship_type': 'leads_to', 'description': '条件后学习循环'},
        {'source_id': 'cpp_loops', 'target_id': 'cpp_jump', 'relationship_type': 'controls', 'description': '跳转语句控制循环'},

        # 函数学习路径
        {'source_id': 'cpp_loops', 'target_id': 'cpp_functions', 'relationship_type': 'leads_to', 'description': '掌握循环后学习函数'},
        {'source_id': 'cpp_functions', 'target_id': 'cpp_function_overloading', 'relationship_type': 'extends_to', 'description': '函数扩展到重载'},
        {'source_id': 'cpp_function_overloading', 'target_id': 'cpp_recursion', 'relationship_type': 'enables', 'description': '重载函数可用于递归'},

        # 数据结构
        {'source_id': 'cpp_arrays', 'target_id': 'cpp_strings', 'relationship_type': 'related_to', 'description': '数组用于字符串存储'},
        {'source_id': 'cpp_strings', 'target_id': 'cpp_functions', 'relationship_type': 'used_in', 'description': '字符串在函数中使用'},

        # 内存管理进阶路径
        {'source_id': 'cpp_variables', 'target_id': 'cpp_pointers', 'relationship_type': 'leads_to', 'description': '变量概念引出指针'},
        {'source_id': 'cpp_pointers', 'target_id': 'cpp_dynamic_memory', 'relationship_type': 'enables', 'description': '指针支持动态内存'},
        {'source_id': 'cpp_dynamic_memory', 'target_id': 'cpp_smart_pointers', 'relationship_type': 'improves', 'description': '智能指针改进动态内存管理'},

        # 面向对象编程路径
        {'source_id': 'cpp_functions', 'target_id': 'cpp_classes', 'relationship_type': 'evolves_to', 'description': '函数演进到类'},
        {'source_id': 'cpp_classes', 'target_id': 'cpp_constructors', 'relationship_type': 'includes', 'description': '类包含构造函数'},
        {'source_id': 'cpp_constructors', 'target_id': 'cpp_destructors', 'relationship_type': 'paired_with', 'description': '构造与析构成对'},
        {'source_id': 'cpp_classes', 'target_id': 'cpp_inheritance', 'relationship_type': 'supports', 'description': '类支持继承'},
        {'source_id': 'cpp_inheritance', 'target_id': 'cpp_polymorphism', 'relationship_type': 'enables', 'description': '继承实现多态'},
        {'source_id': 'cpp_classes', 'target_id': 'cpp_encapsulation', 'relationship_type': 'implements', 'description': '类实现封装'},

        # STL容器和算法
        {'source_id': 'cpp_arrays', 'target_id': 'cpp_vector', 'relationship_type': 'improves', 'description': 'vector改进数组'},
        {'source_id': 'cpp_vector', 'target_id': 'cpp_list', 'relationship_type': 'alternative_to', 'description': 'list是vector的替代'},
        {'source_id': 'cpp_vector', 'target_id': 'cpp_map', 'relationship_type': 'complements', 'description': 'map补充vector功能'},
        {'source_id': 'cpp_map', 'target_id': 'cpp_set', 'relationship_type': 'related_to', 'description': 'map和set相关联'},
        {'source_id': 'cpp_vector', 'target_id': 'cpp_algorithms', 'relationship_type': 'works_with', 'description': '容器配合算法使用'},
        {'source_id': 'cpp_algorithms', 'target_id': 'cpp_iterators', 'relationship_type': 'uses', 'description': '算法使用迭代器'},

        # 模板编程
        {'source_id': 'cpp_classes', 'target_id': 'cpp_templates', 'relationship_type': 'enables', 'description': '类支持模板'},
        {'source_id': 'cpp_templates', 'target_id': 'cpp_template_specialization', 'relationship_type': 'extends_to', 'description': '模板扩展到特化'},
        {'source_id': 'cpp_templates', 'target_id': 'cpp_vector', 'relationship_type': 'creates', 'description': '模板创建vector容器'},
        {'source_id': 'cpp_templates', 'target_id': 'cpp_algorithms', 'relationship_type': 'enables', 'description': '模板实现通用算法'},

        # 现代C++特性
        {'source_id': 'cpp_functions', 'target_id': 'cpp_lambda', 'relationship_type': 'modernizes', 'description': 'lambda现代化函数编程'},
        {'source_id': 'cpp_templates', 'target_id': 'cpp_auto', 'relationship_type': 'simplifies', 'description': 'auto简化模板使用'},
        {'source_id': 'cpp_loops', 'target_id': 'cpp_range_for', 'relationship_type': 'modernizes', 'description': '范围for现代化循环'},
        {'source_id': 'cpp_dynamic_memory', 'target_id': 'cpp_smart_pointers', 'relationship_type': 'modernizes', 'description': '智能指针现代化内存管理'},

        # 错误处理
        {'source_id': 'cpp_functions', 'target_id': 'cpp_exceptions', 'relationship_type': 'handles_errors', 'description': '异常处理函数错误'},
        {'source_id': 'cpp_constructors', 'target_id': 'cpp_exceptions', 'relationship_type': 'uses', 'description': '构造函数使用异常处理'},

        # 文件操作
        {'source_id': 'cpp_io', 'target_id': 'cpp_file_io', 'relationship_type': 'extends_to', 'description': 'IO扩展到文件操作'},
        {'source_id': 'cpp_strings', 'target_id': 'cpp_file_io', 'relationship_type': 'used_in', 'description': '字符串用于文件读写'},

        # 高级主题
        {'source_id': 'cpp_classes', 'target_id': 'cpp_threads', 'relationship_type': 'concurrent_with', 'description': '类支持多线程'},
        {'source_id': 'cpp_smart_pointers', 'target_id': 'cpp_threads', 'relationship_type': 'helps', 'description': '智能指针帮助线程安全'},
        {'source_id': 'cpp_exceptions', 'target_id': 'cpp_threads', 'relationship_type': 'used_in', 'description': '异常用于线程处理'}
    ]

def create_networkx_graph(nodes, relationships):
    """创建NetworkX图对象"""
    G = nx.DiGraph()

    # 添加节点
    for node in nodes:
        G.add_node(node.id, **node.model_dump())

    # 添加边
    for rel in relationships:
        G.add_edge(rel['source_id'], rel['target_id'], **rel)

    return G

def create_interactive_visualization(nodes, relationships, save_path="knowledge_graph.html"):
    """创建交互式Plotly可视化"""

    # 创建布局
    G = create_networkx_graph(nodes, relationships)
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

    # 准备边数据
    edge_x = []
    edge_y = []

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    # 边轨迹 - 使用渐变色和动态效果
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=3, color='#BDC3C7'),
        hoverinfo='none',
        mode='lines',
        opacity=0.6
    )

    # 节点数据
    node_x = []
    node_y = []
    node_text = []
    node_info = []
    node_colors = []
    node_sizes = []
    node_symbols = []

    # 根据分类定义丰富的颜色方案
    category_colors = {
        '基础概念': '#FF6B6B',      # 红色系
        '控制流程': '#4ECDC4',      # 青色系
        '函数': '#45B7D1',          # 蓝色系
        '数据结构': '#96CEB4',      # 绿色系
        '内存管理': '#FFEAA7',      # 黄色系
        '面向对象': '#DDA0DD',      # 紫色系
        'STL容器': '#FFB6C1',      # 粉色系
        '算法': '#87CEEB',          # 天蓝色系
        '模板编程': '#F4A460',      # 沙色系
        '现代C++': '#98D8C8',      # 薄荷绿系
        '错误处理': '#FFA07A',      # 浅橙红系
        '文件处理': '#20B2AA',      # 浅海绿系
        '并发编程': '#9370DB'       # 中紫色系
    }

    # 根据难度定义大小
    difficulty_sizes = {
        'beginner': 35,      # 初学者 - 大节点
        'intermediate': 25,   # 中级 - 中等节点
        'advanced': 30       # 高级 - 大节点突出重要性
    }

    # 根据分类定义符号
    category_symbols = {
        '基础概念': 'circle',
        '控制流程': 'diamond',
        '函数': 'square',
        '数据结构': 'triangle-up',
        '内存管理': 'hexagon',
        '面向对象': 'star',
        'STL容器': 'diamond',
        '算法': 'pentagon',
        '模板编程': 'triangle-down',
        '现代C++': 'star',
        '错误处理': 'x',
        '文件处理': 'triangle-left',
        '并发编程': 'cross'
    }

    # 创建节点ID到节点对象的映射
    node_map = {node.id: node for node in nodes}

    for node_id in G.nodes():
        x, y = pos[node_id]
        node_x.append(x)
        node_y.append(y)

        # 从映射中获取节点数据
        if node_id in node_map:
            node_obj = node_map[node_id]
            node_text.append(node_obj.name)
        else:
            # 如果找不到节点，使用默认值
            node_text.append("Unknown Node")
            node_obj = type('Node', (), {
                'name': 'Unknown Node',
                'category': '其他',
                'difficulty_level': 'beginner',
                'description': '未知节点',
                'node_type': type('NodeType', (), {'value': 'unknown'})()
            })()

        # 悬停信息
        hover_text = (f"<b>{node_obj.name}</b><br>"
                      f"📚 分类: {node_obj.category}<br>"
                      f"🎯 难度: {node_obj.difficulty_level}<br>"
                      f"📝 描述: {node_obj.description}<br>"
                      f"🔧 类型: {node_obj.node_type.value}")
        node_info.append(hover_text)

        # 根据分类设置颜色
        category = node_obj.category
        node_colors.append(category_colors.get(category, '#BDC3C7'))

        # 根据难度设置大小
        difficulty = node_obj.difficulty_level
        node_sizes.append(difficulty_sizes.get(difficulty, 25))

        # 根据分类设置符号
        node_symbols.append(category_symbols.get(category, 'circle'))

    # 节点轨迹
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        hovertext=node_info,
        textposition="middle center",
        hoverlabel=dict(bgcolor="white", font_size=12),
        marker=dict(
            color=node_colors,
            size=node_sizes,
            symbol=node_symbols,
            line=dict(width=3, color='white'),
            opacity=0.9
        ),
        textfont=dict(
            family="Arial, sans-serif",
            size=10,
            color='white'
        )
    )

    # 创建图
    fig = go.Figure(data=[edge_trace, node_trace],
                     layout=go.Layout(
                         title=dict(
                             text='<b>C++ 知识图谱学习路径 🚀</b>',
                             font=dict(size=24, family="Arial, sans-serif", color='#2c3e50')
                         ),
                         showlegend=True,
                         hovermode='closest',
                         margin=dict(b=50, l=50, r=50, t=80),
                         xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                         yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                         plot_bgcolor='#f8f9fa',
                         paper_bgcolor='white',
                         annotations=[
                             dict(
                                 text="💡 拖拽节点进行交互，悬停查看详细信息",
                                 showarrow=False,
                                 x=0.5,
                                 y=-0.05,
                                 xref='paper',
                                 yref='paper',
                                 font=dict(size=14, color='#7f8c8d', family="Arial, sans-serif")
                             )
                         ]
                     ))

    # 添加按分类的图例
    legend_items = []
    for category in set(n.category for n in nodes):
        if category in category_colors:
            legend_items.append(
                go.Scatter(
                    x=[0], y=[0],
                    mode='markers',
                    marker=dict(
                        size=12,
                        color=category_colors[category],
                        symbol='circle',
                        line=dict(width=2, color='white')
                    ),
                    name=category,
                    showlegend=True
                )
            )

    # 创建新的数据列表包含图例
    all_data = list(fig.data) + legend_items
    fig = go.Figure(data=all_data, layout=fig.layout)

    # 保存HTML文件
    fig.write_html(save_path)
    print(f"✅ 交互式可视化已保存到: {save_path}")

    return fig

def create_static_visualization(nodes, relationships, save_path="static_graph.png"):
    """创建静态Matplotlib可视化"""

    G = create_networkx_graph(nodes, relationships)
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

    # 创建图形
    plt.figure(figsize=(14, 10))

    # 使用与交互式可视化相同的颜色方案
    category_colors = {
        '基础概念': '#FF6B6B',
        '控制流程': '#4ECDC4',
        '函数': '#45B7D1',
        '数据结构': '#96CEB4',
        '内存管理': '#FFEAA7',
        '面向对象': '#DDA0DD',
        'STL容器': '#FFB6C1',
        '算法': '#87CEEB',
        '模板编程': '#F4A460',
        '现代C++': '#98D8C8',
        '错误处理': '#FFA07A',
        '文件处理': '#20B2AA',
        '并发编程': '#9370DB'
    }

    # 创建节点ID到节点的映射
    node_map = {node.id: node for node in nodes}

    node_colors = []
    node_sizes = []

    for n in G.nodes():
        if n in node_map:
            node_obj = node_map[n]
            category = node_obj.category
            node_colors.append(category_colors.get(category, '#BDC3C7'))

            # 根据难度设置大小
            difficulty = node_obj.difficulty_level
            if difficulty == 'beginner':
                node_sizes.append(1000)
            elif difficulty == 'intermediate':
                node_sizes.append(800)
            else:  # advanced
                node_sizes.append(900)
        else:
            node_colors.append('#BDC3C7')
            node_sizes.append(500)

    # 绘制图
    nx.draw(G, pos,
            with_labels=True,
            node_color=node_colors,
            node_size=node_sizes,
            font_size=12,
            font_weight='bold',
            edge_color='#888',
            width=2,
            alpha=0.8,
            arrows=True,
            arrowsize=20)

    plt.title("C++知识图谱 - 系统架构展示", fontsize=16, fontweight='bold', pad=20)
    plt.axis('off')

    # 添加图例
    legend_elements = []
    seen_categories = set()
    for node in G.nodes():
        if node in node_map:
            node_obj = node_map[node]
            category = node_obj.category
            if category not in seen_categories:
                seen_categories.add(category)
                legend_elements.append(
                    plt.Line2D([0], [0], marker='o', color='w',
                                markerfacecolor=category_colors.get(category, '#95a5a6'),
                                markersize=10, label=category)
                )

    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
    plt.tight_layout()

    # 保存图片
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ 静态可视化已保存到: {save_path}")
    plt.close()

def create_statistics_chart(nodes, relationships, save_path="statistics.html"):
    """创建统计图表"""

    # 统计节点类型分布
    node_types = {}
    difficulty_levels = {}
    categories = {}

    for node in nodes:
        # 节点类型统计
        node_type = node.node_type.value
        node_types[node_type] = node_types.get(node_type, 0) + 1

        # 难度级别统计
        difficulty = node.difficulty_level.value if node.difficulty_level else 'unknown'
        difficulty_levels[difficulty] = difficulty_levels.get(difficulty, 0) + 1

        # 分类统计
        category = node.category
        categories[category] = categories.get(category, 0) + 1

    # 创建子图
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('节点类型分布', '难度级别分布', '知识分类分布', '学习路径关系'),
        specs=[[{"type": "pie"}, {"type": "pie"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )

    # 节点类型饼图
    fig.add_trace(
        go.Pie(labels=list(node_types.keys()), values=list(node_types.values()), name="节点类型"),
        row=1, col=1
    )

    # 难度级别饼图
    fig.add_trace(
        go.Pie(labels=list(difficulty_levels.keys()), values=list(difficulty_levels.values()), name="难度级别"),
        row=1, col=2
    )

    # 分类条形图
    fig.add_trace(
        go.Bar(x=list(categories.keys()), y=list(categories.values()), name="知识分类"),
        row=2, col=1
    )

    # 关系类型条形图
    rel_types = {}
    for rel in relationships:
        rel_type = rel['relationship_type']
        rel_types[rel_type] = rel_types.get(rel_type, 0) + 1

    fig.add_trace(
        go.Bar(x=list(rel_types.keys()), y=list(rel_types.values()), name="关系类型"),
        row=2, col=2
    )

    # 更新布局
    fig.update_layout(
        title_text="<b>C++知识图谱统计分析</b>",
        showlegend=False,
        height=800,
        title_font_size=20
    )

    # 保存HTML
    fig.write_html(save_path)
    print(f"✅ 统计图表已保存到: {save_path}")

def main():
    """主函数"""
    print("=" * 60)
    print("CS Knowledge Graph 可视化演示")
    print("=" * 60)

    # 创建数据
    print("📊 创建C++知识图谱数据...")
    nodes = create_cpp_knowledge_graph()
    relationships = create_sample_relationships()

    print(f"   创建了 {len(nodes)} 个知识节点")
    print(f"   创建了 {len(relationships)} 个知识关系")
    print()

    # 生成可视化
    print("🎨 生成可视化图表...")

    # 交互式可视化
    print("   1. 创建交互式Plotly可视化...")
    create_interactive_visualization(nodes, relationships, "frontend/interactive_graph.html")

    # 静态可视化
    print("   2. 创建静态Matplotlib可视化...")
    create_static_visualization(nodes, relationships, "frontend/static_graph.png")

    # 统计图表
    print("   3. 创建统计分析图表...")
    create_statistics_chart(nodes, relationships, "frontend/statistics.html")

    print()
    print("🎉 可视化生成完成!")
    print()
    print("📁 生成的文件:")
    print("   - frontend/interactive_graph.html (交互式图谱)")
    print("   - frontend/static_graph.png (静态图谱图片)")
    print("   - frontend/statistics.html (统计图表)")
    print()
    print("🌐 如何查看:")
    print("   1. 访问 http://localhost:5000 查看Web界面")
    print("   2. 在浏览器中打开 frontend/interactive_graph.html")
    print("   3. 查看 frontend/static_graph.png 图片文件")
    print()
    print("💡 系统状态:")
    print("   - API服务器: http://localhost:5000")
    print("   - Neo4j浏览器: http://localhost:7474")
    print("   - Web界面: http://localhost:5000")
    print("=" * 60)

if __name__ == '__main__':
    main()