# CS Knowledge Graph 使用指南

## 快速开始

### 1. 环境准备

确保你已经安装了以下软件：
- Python 3.9+
- Conda (推荐使用 Miniconda)
- Neo4j 数据库 (可选，如果不使用Neo4j，系统将使用内存存储)

### 2. 激活环境

```bash
# 激活conda环境
conda activate cs_kg_env

# 如果没有环境，请先创建
conda create -n cs_kg_env python=3.9 -y
conda activate cs_kg_env
```

### 3. 安装依赖

```bash
# 如果有代理，先激活代理
proxy

# 安装核心依赖（已安装的可跳过）
pip install flask pydantic python-dotenv neo4j pandas networkx matplotlib plotly
```

### 4. 配置环境变量（可选）

```bash
# 复制环境配置文件
cp config/.env.example config/.env

# 编辑配置文件
nano config/.env
```

### 5. 启动系统

```bash
# 启动API服务器
python main.py
```

启动成功后，你将看到类似输出：
```
2025-11-06 13:00:00 - __main__ - INFO - 启动CS Knowledge Graph系统...
2025-11-06 13:00:01 - src.core.database_manager - INFO - 成功连接到Neo4j数据库
2025-11-06 13:00:01 - __main__ - INFO - API服务器启动在 http://0.0.0.0:5000
```

## API接口说明

### 基础信息

- 基础URL: `http://localhost:5000`
- 数据格式: JSON
- 字符编码: UTF-8

### 主要接口

#### 1. 健康检查
```bash
GET /health
```

#### 2. 节点操作

**获取节点列表**
```bash
GET /api/nodes?type=concept&language=cpp&limit=20
GET /api/nodes?search=指针&limit=10
```

**获取单个节点**
```bash
GET /api/nodes/pointer
```

**创建节点**
```bash
POST /api/nodes
Content-Type: application/json

{
  "id": "new_concept",
  "name": "新概念",
  "node_type": "concept",
  "description": "这是一个新的编程概念",
  "language": "cpp",
  "category": "基础概念",
  "difficulty_level": "beginner"
}
```

**更新节点**
```bash
PUT /api/nodes/pointer
Content-Type: application/json

{
  "description": "更新后的描述",
  "category": "高级概念"
}
```

**删除节点**
```bash
DELETE /api/nodes/pointer
```

**获取相邻节点**
```bash
GET /api/nodes/pointer/adjacent
```

#### 3. 关系操作

**创建关系**
```bash
POST /api/relationships
Content-Type: application/json

{
  "id": "rel_001",
  "source_id": "pointer",
  "target_id": "memory_management",
  "relationship_type": "related_to",
  "description": "指针与内存管理密切相关"
}
```

#### 4. 查询功能

**查找最短路径**
```bash
GET /api/path/basic_types/smart_pointer
```

**获取学习路径**
```bash
GET /api/learning-path/basic_types?max_depth=5
```

**获取统计信息**
```bash
GET /api/statistics
```

#### 5. 数据操作

**导入数据**
```bash
POST /api/import
Content-Type: application/json

{
  "metadata": {
    "language": "cpp",
    "description": "C++知识数据"
  },
  "nodes": [...],
  "relationships": [...]
}
```

**导出数据**
```bash
GET /api/export?language=cpp&node_type=concept
```

## 运行测试

```bash
# 运行所有测试
python tests/test_basic_functionality.py

# 或者使用unittest模块
python -m unittest tests.test_basic_functionality -v
```

## 示例用法

### 1. 查询C++基础概念

```bash
# 查找所有C++概念
curl "http://localhost:5000/api/nodes?type=concept&language=cpp"

# 搜索指针相关概念
curl "http://localhost:5000/api/nodes?search=指针"
```

### 2. 获取学习路径

```bash
# 获取从基础概念到智能指针的学习路径
curl "http://localhost:5000/api/learning-path/basic_types"
```

### 3. 创建新知识点

```bash
curl -X POST "http://localhost:5000/api/nodes" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "modern_cpp_20",
    "name": "C++20新特性",
    "node_type": "concept",
    "description": "C++20引入的新特性",
    "language": "cpp",
    "category": "现代C++特性"
  }'
```

### 4. 建立知识关联

```bash
curl -X POST "http://localhost:5000/api/relationships" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "cpp20_requires_cpp11",
    "source_id": "modern_cpp_20",
    "target_id": "auto_keyword",
    "relationship_type": "builds_upon",
    "description": "C++20建立在C++11特性基础上"
  }'
```

## 数据结构说明

### 节点类型

- `concept`: 概念
- `language`: 编程语言
- `technology`: 技术
- `library`: 库/框架
- `tool`: 工具

### 关系类型

- `belongs_to`: 属于
- `depends_on`: 依赖于
- `implements`: 实现
- `related_to`: 相关
- `learning_path`: 学习路径

### 难度级别

- `beginner`: 初级
- `intermediate`: 中级
- `advanced`: 高级
- `expert`: 专家级

## 扩展开发

### 添加新的编程语言

1. 在 `data/raw/` 目录下创建新的JSON数据文件
2. 参照 `cpp_knowledge_data.json` 的格式
3. 使用API导入数据

### 添加新功能

1. 在 `src/core/` 中添加业务逻辑
2. 在 `src/api/` 中添加API接口
3. 编写相应的测试用例

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查Neo4j是否启动
   - 验证连接配置
   - 确认用户名密码正确

2. **端口占用**
   - 修改配置文件中的端口设置
   - 或者停止占用端口的进程

3. **依赖包安装失败**
   - 确保网络连接正常
   - 使用代理或国内镜像源
   - 检查Python版本兼容性

### 日志查看

系统日志保存在 `logs/app.log` 文件中：
```bash
tail -f logs/app.log
```

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 编写测试
5. 创建 Pull Request

## 联系方式

如有问题或建议，请通过以下方式联系：
- 创建 GitHub Issue
- 发送邮件至项目维护者