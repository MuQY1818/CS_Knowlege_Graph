"""
Flask API Application - Flask API应用

提供RESTful API接口供前端调用。
"""

import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from typing import Dict, Any
import os
from ..core import DatabaseManager, KnowledgeGraphManager, get_db_manager
from ..data import DataImporter
from config import get_config


def create_app(config_name: str = None) -> Flask:
    """创建Flask应用"""
    app = Flask(__name__)

    # 加载配置
    config = get_config(config_name)
    app.config.from_object(config)

    # 启用CORS
    CORS(app)

    # 配置日志
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 获取项目根目录
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    # 初始化组件
    db_manager = get_db_manager()
    kg_manager = KnowledgeGraphManager(db_manager)
    data_importer = DataImporter(kg_manager)

    # 连接数据库
    if not db_manager.connect():
        app.logger.error("无法连接到数据库")
        return app

    # 创建数据库约束
    try:
        db_manager.create_constraints()
    except Exception as e:
        app.logger.warning(f"创建数据库约束失败: {e}")

    @app.route('/')
    def index():
        """主页 - 返回前端界面"""
        frontend_path = os.path.join(project_root, 'frontend', 'index.html')
        if os.path.exists(frontend_path):
            return send_from_directory(frontend_path, 'index.html')
        else:
            return jsonify({
                'message': 'CS Knowledge Graph API',
                'status': 'running',
                'endpoints': {
                    'health': '/health',
                    'statistics': '/api/statistics',
                    'nodes': '/api/nodes',
                    'documentation': '访问 /docs 查看API文档'
                }
            })

    @app.route('/frontend/<path:filename>')
    def serve_frontend(filename):
        """服务前端静态文件"""
        frontend_dir = os.path.join(project_root, 'frontend')
        return send_from_directory(frontend_dir, filename)

    @app.route('/health', methods=['GET'])
    def health_check():
        """健康检查"""
        try:
            # 检查数据库连接
            db_info = db_manager.get_database_info()
            return jsonify({
                'status': 'healthy',
                'database': 'connected',
                'info': db_info
            })
        except Exception as e:
            return jsonify({
                'status': 'unhealthy',
                'error': str(e)
            }), 500

    @app.route('/api/nodes', methods=['GET'])
    def get_nodes():
        """获取节点列表"""
        try:
            # 获取查询参数
            node_type = request.args.get('type')
            language = request.args.get('language')
            category = request.args.get('category')
            keyword = request.args.get('search')
            limit = int(request.args.get('limit', 20))

            if keyword:
                # 搜索节点
                nodes = kg_manager.search_nodes(keyword, limit)
            elif node_type:
                # 根据类型获取节点
                from ..models import NodeType
                nodes = kg_manager.get_nodes_by_type(NodeType(node_type))
            elif language:
                # 根据语言获取节点
                nodes = kg_manager.get_nodes_by_language(language)
            else:
                # 获取所有节点
                query = "MATCH (n:KnowledgeNode) RETURN n ORDER BY n.name LIMIT $limit"
                result = db_manager.execute_query(query, {'limit': limit})
                nodes = [kg_manager._neo4j_node_to_dict(record['n']) for record in result]

            return jsonify({
                'success': True,
                'data': nodes,
                'count': len(nodes)
            })
        except Exception as e:
            app.logger.error(f"获取节点列表失败: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/nodes/<node_id>', methods=['GET'])
    def get_node(node_id: str):
        """获取单个节点"""
        try:
            node = kg_manager.get_node(node_id)
            if node:
                return jsonify({
                    'success': True,
                    'data': node
                })
            else:
                return jsonify({
                    'success': False,
                    'error': '节点不存在'
                }), 404
        except Exception as e:
            app.logger.error(f"获取节点失败: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/nodes/<node_id>/adjacent', methods=['GET'])
    def get_adjacent_nodes(node_id: str):
        """获取相邻节点"""
        try:
            adjacent = kg_manager.get_adjacent_nodes(node_id)
            result = []
            for node, relationship in adjacent:
                result.append({
                    'node': node,
                    'relationship': relationship
                })
            return jsonify({
                'success': True,
                'data': result,
                'count': len(result)
            })
        except Exception as e:
            app.logger.error(f"获取相邻节点失败: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/nodes', methods=['POST'])
    def create_node():
        """创建节点"""
        try:
            node_data = request.get_json()
            if not node_data:
                return jsonify({
                    'success': False,
                    'error': '请求数据为空'
                }), 400

            node = kg_manager.create_node(node_data)
            if node:
                return jsonify({
                    'success': True,
                    'data': node.dict()
                }), 201
            else:
                return jsonify({
                    'success': False,
                    'error': '创建节点失败'
                }), 500
        except Exception as e:
            app.logger.error(f"创建节点失败: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/nodes/<node_id>', methods=['PUT'])
    def update_node(node_id: str):
        """更新节点"""
        try:
            updates = request.get_json()
            if not updates:
                return jsonify({
                    'success': False,
                    'error': '请求数据为空'
                }), 400

            success = kg_manager.update_node(node_id, updates)
            if success:
                return jsonify({
                    'success': True,
                    'message': '节点更新成功'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': '节点不存在或更新失败'
                }), 404
        except Exception as e:
            app.logger.error(f"更新节点失败: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/nodes/<node_id>', methods=['DELETE'])
    def delete_node(node_id: str):
        """删除节点"""
        try:
            success = kg_manager.delete_node(node_id)
            if success:
                return jsonify({
                    'success': True,
                    'message': '节点删除成功'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': '节点不存在或删除失败'
                }), 404
        except Exception as e:
            app.logger.error(f"删除节点失败: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/relationships', methods=['POST'])
    def create_relationship():
        """创建关系"""
        try:
            rel_data = request.get_json()
            if not rel_data:
                return jsonify({
                    'success': False,
                    'error': '请求数据为空'
                }), 400

            relationship = kg_manager.create_relationship(rel_data)
            if relationship:
                return jsonify({
                    'success': True,
                    'data': relationship.dict()
                }), 201
            else:
                return jsonify({
                    'success': False,
                    'error': '创建关系失败'
                }), 500
        except Exception as e:
            app.logger.error(f"创建关系失败: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/path/<source_id>/<target_id>', methods=['GET'])
    def find_shortest_path(source_id: str, target_id: str):
        """查找最短路径"""
        try:
            path = kg_manager.find_shortest_path(source_id, target_id)
            if path:
                return jsonify({
                    'success': True,
                    'data': path
                })
            else:
                return jsonify({
                    'success': False,
                    'error': '未找到路径'
                }), 404
        except Exception as e:
            app.logger.error(f"查找路径失败: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/learning-path/<node_id>', methods=['GET'])
    def get_learning_path(node_id: str):
        """获取学习路径"""
        try:
            max_depth = int(request.args.get('max_depth', 5))
            path = kg_manager.get_learning_path(node_id, max_depth)
            return jsonify({
                'success': True,
                'data': path
            })
        except Exception as e:
            app.logger.error(f"获取学习路径失败: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/statistics', methods=['GET'])
    def get_statistics():
        """获取统计信息"""
        try:
            stats = kg_manager.get_statistics()
            return jsonify({
                'success': True,
                'data': stats
            })
        except Exception as e:
            app.logger.error(f"获取统计信息失败: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/import', methods=['POST'])
    def import_data():
        """导入数据"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({
                    'success': False,
                    'error': '请求数据为空'
                }), 400

            # 验证数据结构
            validation = data_importer.validate_data_structure(data)
            if validation['errors']:
                return jsonify({
                    'success': False,
                    'error': '数据结构验证失败',
                    'details': validation['errors']
                }), 400

            # 导入数据
            result = data_importer._import_knowledge_data(data)
            return jsonify({
                'success': True,
                'data': result,
                'message': f"成功导入 {result['nodes']} 个节点和 {result['relationships']} 个关系"
            })
        except Exception as e:
            app.logger.error(f"导入数据失败: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/export', methods=['GET'])
    def export_data():
        """导出数据"""
        try:
            # 获取过滤参数
            filters = {}
            if request.args.get('language'):
                filters['language'] = request.args.get('language')
            if request.args.get('node_type'):
                filters['node_type'] = request.args.get('node_type')
            if request.args.get('category'):
                filters['category'] = request.args.get('category')

            # 导出到文件
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"knowledge_graph_export_{timestamp}.json"

            success = data_importer.export_to_json(f"data/exports/{filename}", filters)
            if success:
                return jsonify({
                    'success': True,
                    'data': {
                        'filename': filename,
                        'filters': filters
                    }
                })
            else:
                return jsonify({
                    'success': False,
                    'error': '导出失败'
                }), 500
        except Exception as e:
            app.logger.error(f"导出数据失败: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.errorhandler(404)
    def not_found(error):
        """404错误处理"""
        return jsonify({
            'success': False,
            'error': 'API端点不存在'
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        """500错误处理"""
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500

    # 注册关闭处理
    @app.teardown_appcontext
    def shutdown_db(exception):
        """应用关闭时断开数据库连接"""
        db_manager.disconnect()

    return app


if __name__ == '__main__':
    app = create_app()
    config = get_config()
    app.run(
        host=config.API_HOST,
        port=config.API_PORT,
        debug=config.API_DEBUG
    )