# CS Knowledge Graph - 计算机科学知识图谱

## 项目简介

CS Knowledge Graph 是一个专门为计算机科学领域设计的知识图谱系统。系统以C++语言知识为起点，逐步扩展到计算机科学的各个领域，为学习者提供结构化的知识体系。

## 主要功能

- **知识查询和浏览**: 通过图形化界面浏览计算机科学概念之间的关系
- **知识可视化**: 交互式的知识图谱展示，直观呈现知识网络
- **知识管理和编辑**: 支持知识的增删改查操作
- **智能问答系统**: 基于知识图谱的AI问答能力（规划中）

## 技术栈

- **后端**: Python 3.9 + Flask/FastAPI
- **图数据库**: Neo4j
- **前端**: React + D3.js
- **数据处理**: Pandas, NetworkX, SpaCy

## 环境要求

- Python 3.9+
- Neo4j 5.0+
- Conda环境管理器

## 快速开始

### 1. 环境配置

```bash
# 创建conda环境
conda create -n cs_kg_env python=3.9 -y

# 激活环境
conda activate cs_kg_env

# 安装依赖
pip install -r requirements.txt
```

### 2. 数据库配置

确保Neo4j数据库已安装并运行，默认连接配置：
- URL: bolt://localhost:7687
- 用户名: neo4j
- 密码: password

### 3. 运行项目

```bash
# 启动API服务
python src/api/app.py

# 访问Web界面
# http://localhost:5000
```

## 项目结构

```
CS_Knowledge_Graph/
├── src/
│   ├── core/           # 核心业务逻辑
│   ├── data/           # 数据处理和导入
│   ├── api/            # API接口
│   ├── visualization/  # 可视化组件
│   └── models/         # 数据模型
├── data/               # 数据文件
│   ├── raw/           # 原始数据
│   ├── processed/     # 处理后数据
│   └── exports/       # 导出数据
├── tests/              # 测试代码
├── docs/               # 文档
├── frontend/           # 前端代码
└── config/             # 配置文件
```

## 贡献指南

1. Fork 本仓库
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License

## 更新日志

详细更新记录请查看 [CLAUDE.md](./CLAUDE.md)