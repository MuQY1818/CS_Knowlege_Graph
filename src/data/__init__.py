"""
Data module - 数据处理和导入模块

负责知识的收集、处理、验证和导入功能。

主要模块：
- DataImporter: 数据导入和导出功能
"""

from .data_importer import DataImporter

__all__ = [
    'DataImporter',
]