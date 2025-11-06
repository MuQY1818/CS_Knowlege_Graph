"""
Graph Visualizer - 图谱可视化模块

提供知识图谱的可视化功能。
"""

import logging
import json
from typing import Dict, List, Any, Optional, Tuple
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False


class GraphVisualizer:
    """图谱可视化器"""

    def __init__(self):
        """初始化可视化器"""
        self.logger = logging.getLogger(__name__)

        # 节点颜色配置
        self.node_colors = {
            'concept': '#3498db',      # 蓝色
            'language': '#e74c3c',     # 红色
            'technology': '#2ecc71',   # 绿色
            'library': '#f39c12',      # 橙色
            'tool': '#9b59b6',         # 紫色
            'paradigm': '#1abc9c',     # 青色
            'pattern': '#34495e',      # 深灰色
            'algorithm': '#e67e22',    # 深橙色
            'data_structure': '#16a085', # 深青色
            'problem': '#c0392b',      # 深红色
            'solution': '#27ae60',     # 深绿色
            'best_practice': '#f1c40f', # 黄色
            'common_mistake': '#95a5a6' # 灰色
        }

        # 节点大小配置
        self.node_sizes = {
            'concept': 800,
            'language': 1200,
            'technology': 1000,
            'library': 900,
            'tool': 700,
            'paradigm': 600,
            'pattern': 600,
            'algorithm': 700,
            'data_structure': 700,
            'problem': 600,
            'solution': 600,
            'best_practice': 800,
            'common_mistake': 600
        }

    def create_networkx_graph(self, nodes: List[Dict[str, Any]],
                            relationships: List[Dict[str, Any]]) -> nx.Graph:
        """创建NetworkX图对象"""
        G = nx.Graph()

        # 添加节点
        for node in nodes:
            node_id = node['id']
            node_type = node.get('node_type', 'concept')
            node_name = node.get('name', node_id)

            G.add_node(node_id,
                      name=node_name,
                      type=node_type,
                      color=self.node_colors.get(node_type, '#95a5a6'),
                      size=self.node_sizes.get(node_type, 800),
                      description=node.get('description', ''),
                      category=node.get('category', ''),
                      difficulty=node.get('difficulty_level', ''))

        # 添加边
        for rel in relationships:
            source_id = rel.get('source_id')
            target_id = rel.get('target_id')
            rel_type = rel.get('type', rel.get('relationship_type', 'related'))

            if source_id and target_id and source_id in G.nodes and target_id in G.nodes:
                G.add_edge(source_id, target_id,
                          type=rel_type,
                          description=rel.get('description', ''),
                          weight=rel.get('weight', 1.0))

        return G

    def create_matplotlib_visualization(self, nodes: List[Dict[str, Any]],
                                     relationships: List[Dict[str, Any]],
                                     layout: str = 'spring',
                                     figsize: Tuple[int, int] = (12, 8),
                                     save_path: Optional[str] = None) -> plt.Figure:
        """创建Matplotlib图谱可视化"""
        try:
            # 创建图对象
            G = self.create_networkx_graph(nodes, relationships)

            # 设置布局
            if layout == 'spring':
                pos = nx.spring_layout(G, k=1, iterations=50)
            elif layout == 'circular':
                pos = nx.circular_layout(G)
            elif layout == 'shell':
                pos = nx.shell_layout(G)
            elif layout == 'kamada_kawai':
                pos = nx.kamada_kawai_layout(G)
            else:
                pos = nx.spring_layout(G)

            # 创建图形
            fig, ax = plt.subplots(figsize=figsize)
            ax.set_title('知识图谱可视化', fontsize=16, fontweight='bold')

            # 绘制边
            nx.draw_networkx_edges(G, pos,
                                 edge_color='#7f8c8d',
                                 width=1.5,
                                 alpha=0.6,
                                 ax=ax)

            # 绘制节点
            node_colors = [G.nodes[node]['color'] for node in G.nodes()]
            node_sizes = [G.nodes[node]['size'] for node in G.nodes()]

            nx.draw_networkx_nodes(G, pos,
                                 node_color=node_colors,
                                 node_size=node_sizes,
                                 alpha=0.8,
                                 ax=ax)

            # 绘制标签
            labels = {node: G.nodes[node]['name'] for node in G.nodes()}
            nx.draw_networkx_labels(G, pos, labels,
                                  font_size=10,
                                  font_weight='bold',
                                  ax=ax)

            # 创建图例
            legend_elements = []
            node_types_in_graph = set(G.nodes[node]['type'] for node in G.nodes())
            for node_type in node_types_in_graph:
                color = self.node_colors.get(node_type, '#95a5a6')
                type_names = {
                    'concept': '概念',
                    'language': '语言',
                    'technology': '技术',
                    'library': '库/框架',
                    'tool': '工具',
                    'paradigm': '编程范式',
                    'pattern': '设计模式',
                    'algorithm': '算法',
                    'data_structure': '数据结构'
                }
                legend_elements.append(mpatches.Patch(color=color,
                                                    label=type_names.get(node_type, node_type)))

            ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))

            # 移除坐标轴
            ax.axis('off')
            plt.tight_layout()

            # 保存图片
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"图谱可视化已保存到: {save_path}")

            return fig

        except Exception as e:
            self.logger.error(f"创建Matplotlib可视化失败: {e}")
            return None

    def create_plotly_visualization(self, nodes: List[Dict[str, Any]],
                                  relationships: List[Dict[str, Any]],
                                  layout: str = 'spring') -> go.Figure:
        """创建Plotly交互式图谱可视化"""
        try:
            # 创建图对象
            G = self.create_networkx_graph(nodes, relationships)

            # 设置布局
            if layout == 'spring':
                pos = nx.spring_layout(G, k=1, iterations=50)
            elif layout == 'circular':
                pos = nx.circular_layout(G)
            elif layout == 'kamada_kawai':
                pos = nx.kamada_kawai_layout(G)
            else:
                pos = nx.spring_layout(G)

            # 准备边数据
            edge_x = []
            edge_y = []
            edge_info = []

            for edge in G.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])

                edge_data = G.edges[edge]
                edge_info.append(f"关系: {edge_data.get('type', 'unknown')}<br>"
                               f"描述: {edge_data.get('description', 'N/A')}")

            # 创建边的轨迹
            edge_trace = go.Scatter(
                x=edge_x, y=edge_y,
                line=dict(width=1.5, color='#888'),
                hoverinfo='none',
                mode='lines'
            )

            # 准备节点数据
            node_x = []
            node_y = []
            node_text = []
            node_info = []
            node_colors = []
            node_sizes = []

            for node in G.nodes():
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)

                node_data = G.nodes[node]
                node_text.append(node_data['name'])

                # 创建悬停信息
                hover_text = (f"名称: {node_data['name']}<br>"
                            f"类型: {node_data['type']}<br>"
                            f"描述: {node_data.get('description', 'N/A')}<br>"
                            f"分类: {node_data.get('category', 'N/A')}")
                if node_data.get('difficulty'):
                    hover_text += f"<br>难度: {node_data['difficulty']}"
                node_info.append(hover_text)

                node_colors.append(node_data['color'])
                node_sizes.append(node_data['size'] / 100)  # Plotly使用较小的尺寸值

            # 创建节点的轨迹
            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers+text',
                hoverinfo='text',
                text=node_text,
                hovertext=node_info,
                textposition="middle center",
                hoverlabel=dict(bgcolor="white", font_size=12),
                marker=dict(
                    showscale=True,
                    colorscale='Viridis',
                    reversescale=True,
                    color=node_colors,
                    size=node_sizes,
                    colorbar=dict(
                        thickness=15,
                        len=0.5,
                        x=1.02,
                        title="节点类型"
                    ),
                    line=dict(width=2)
                )
            )

            # 创建图形
            fig = go.Figure(data=[edge_trace, node_trace],
                          layout=go.Layout(
                              title='知识图谱交互式可视化',
                              titlefont_size=16,
                              showlegend=False,
                              hovermode='closest',
                              margin=dict(b=20, l=5, r=5, t=40),
                              annotations=[
                                  dict(
                                      text="拖拽节点进行交互，点击节点查看详情",
                                      showarrow=False,
                                      xref="paper", yref="paper",
                                      x=0.005, y=-0.002,
                                      xanchor='left', yanchor='bottom',
                                      font=dict(color="#888", size=12)
                                  )
                              ],
                              xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                              yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                              plot_bgcolor='white'
                          ))

            return fig

        except Exception as e:
            self.logger.error(f"创建Plotly可视化失败: {e}")
            return None

    def create_subgraph_visualization(self, nodes: List[Dict[str, Any]],
                                   relationships: List[Dict[str, Any]],
                                   center_node: str,
                                   depth: int = 2) -> go.Figure:
        """创建子图谱可视化（以某个节点为中心）"""
        try:
            # 创建完整图
            G = self.create_networkx_graph(nodes, relationships)

            # 找到中心节点的邻居
            if center_node not in G.nodes:
                self.logger.error(f"中心节点 {center_node} 不存在")
                return None

            # 获取指定深度的子图
            subgraph_nodes = {center_node}
            current_level = {center_node}

            for _ in range(depth):
                next_level = set()
                for node in current_level:
                    next_level.update(G.neighbors(node))
                subgraph_nodes.update(next_level)
                current_level = next_level

            # 创建子图
            subgraph = G.subgraph(subgraph_nodes)

            # 设置布局
            pos = nx.spring_layout(subgraph, k=2, iterations=50)

            # 准备数据
            edge_x, edge_y = [], []
            for edge in subgraph.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])

            edge_trace = go.Scatter(x=edge_x, y=edge_y,
                                  line=dict(width=2, color='#888'),
                                  hoverinfo='none',
                                  mode='lines')

            node_x, node_y = [], []
            node_text, node_info = [], []
            node_colors, node_sizes = [], []

            for node in subgraph.nodes():
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)

                node_data = subgraph.nodes[node]
                node_text.append(node_data['name'])

                is_center = (node == center_node)
                size = node_data['size'] / 80 if is_center else node_data['size'] / 100

                hover_text = (f"名称: {node_data['name']}<br>"
                            f"类型: {node_data['type']}<br>"
                            f"描述: {node_data.get('description', 'N/A')}")
                if is_center:
                    hover_text = f"<b>{hover_text}</b>"

                node_info.append(hover_text)
                node_colors.append(node_data['color'])
                node_sizes.append(size)

            node_trace = go.Scatter(x=node_x, y=node_y,
                                  mode='markers+text',
                                  hoverinfo='text',
                                  text=node_text,
                                  hovertext=node_info,
                                  textposition="middle center",
                                  marker=dict(
                                      color=node_colors,
                                      size=node_sizes,
                                      line=dict(width=2, color='white')
                                  ))

            fig = go.Figure(data=[edge_trace, node_trace],
                          layout=go.Layout(
                              title=f'知识图谱 - {center_node} 及其相关知识',
                              titlefont_size=16,
                              showlegend=False,
                              hovermode='closest',
                              margin=dict(b=20, l=5, r=5, t=40),
                              xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                              yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                          ))

            return fig

        except Exception as e:
            self.logger.error(f"创建子图谱可视化失败: {e}")
            return None

    def create_learning_path_visualization(self, path_nodes: List[str],
                                        nodes: List[Dict[str, Any]]) -> go.Figure:
        """创建学习路径可视化"""
        try:
            # 过滤出路径中的节点
            path_node_data = {node['id']: node for node in nodes if node['id'] in path_nodes}

            if len(path_node_data) < 2:
                self.logger.error("学习路径节点数量不足")
                return None

            # 创建线性布局
            pos = {}
            x_step = 2.0
            for i, node_id in enumerate(path_nodes):
                if node_id in path_node_data:
                    pos[node_id] = (i * x_step, 0)

            # 准备边数据
            edge_x, edge_y = [], []
            for i in range(len(path_nodes) - 1):
                if path_nodes[i] in pos and path_nodes[i + 1] in pos:
                    x0, y0 = pos[path_nodes[i]]
                    x1, y1 = pos[path_nodes[i + 1]]
                    edge_x.extend([x0, x1, None])
                    edge_y.extend([y0, y1, None])

            # 添加箭头
            for i in range(len(path_nodes) - 1):
                if path_nodes[i] in pos and path_nodes[i + 1] in pos:
                    x0, y0 = pos[path_nodes[i]]
                    x1, y1 = pos[path_nodes[i + 1]]
                    # 箭头位置
                    arrow_x = x0 + (x1 - x0) * 0.8
                    arrow_y = y0 + (y1 - y0) * 0.8

            edge_trace = go.Scatter(x=edge_x, y=edge_y,
                                  line=dict(width=3, color='#3498db'),
                                  hoverinfo='none',
                                  mode='lines')

            # 准备节点数据
            node_x, node_y = [], []
            node_text, node_info = [], []
            node_colors = []

            for i, node_id in enumerate(path_nodes):
                if node_id in path_node_data:
                    x, y = pos[node_id]
                    node_x.append(x)
                    node_y.append(y)

                    node_data = path_node_data[node_id]
                    node_text.append(f"{i+1}. {node_data['name']}")

                    hover_text = (f"步骤 {i+1}: {node_data['name']}<br>"
                                f"类型: {node_data['type']}<br>"
                                f"描述: {node_data.get('description', 'N/A')}")
                    node_info.append(hover_text)

                    # 根据难度设置颜色
                    difficulty = node_data.get('difficulty_level', 'intermediate')
                    difficulty_colors = {
                        'beginner': '#2ecc71',    # 绿色
                        'intermediate': '#f39c12', # 橙色
                        'advanced': '#e74c3c',     # 红色
                        'expert': '#9b59b6'        # 紫色
                    }
                    node_colors.append(difficulty_colors.get(difficulty, '#95a5a6'))

            node_trace = go.Scatter(x=node_x, y=node_y,
                                  mode='markers+text',
                                  hoverinfo='text',
                                  text=node_text,
                                  hovertext=node_info,
                                  textposition="top center",
                                  marker=dict(
                                      color=node_colors,
                                      size=30,
                                      line=dict(width=2, color='white')
                                  ))

            fig = go.Figure(data=[edge_trace, node_trace],
                          layout=go.Layout(
                              title='学习路径可视化',
                              titlefont_size=16,
                              showlegend=True,
                              hovermode='closest',
                              margin=dict(b=100, l=50, r=50, t=40),
                              xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                              yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                              annotations=[
                                  dict(
                                      x=0.5, y=-0.15,
                                      xref='paper', yref='paper',
                                      text="绿色: 初级 | 橙色: 中级 | 红色: 高级 | 紫色: 专家级",
                                      showarrow=False,
                                      font=dict(size=12)
                                  )
                              ]
                          ))

            return fig

        except Exception as e:
            self.logger.error(f"创建学习路径可视化失败: {e}")
            return None

    def save_visualization_html(self, fig: go.Figure, filename: str):
        """保存可视化到HTML文件"""
        try:
            fig.write_html(filename)
            self.logger.info(f"可视化已保存到: {filename}")
        except Exception as e:
            self.logger.error(f"保存HTML文件失败: {e}")

    def get_graph_statistics(self, nodes: List[Dict[str, Any]],
                           relationships: List[Dict[str, Any]]) -> Dict[str, Any]:
        """获取图谱统计信息"""
        try:
            G = self.create_networkx_graph(nodes, relationships)

            stats = {
                '节点数量': G.number_of_nodes(),
                '关系数量': G.number_of_edges(),
                '节点类型分布': {},
                '连通分量': nx.number_connected_components(G),
                '平均度': round(sum(dict(G.degree()).values()) / G.number_of_nodes(), 2) if G.number_of_nodes() > 0 else 0,
                '密度': round(nx.density(G), 3)
            }

            # 节点类型分布
            for node in G.nodes():
                node_type = G.nodes[node]['type']
                stats['节点类型分布'][node_type] = stats['节点类型分布'].get(node_type, 0) + 1

            return stats

        except Exception as e:
            self.logger.error(f"获取统计信息失败: {e}")
            return {}