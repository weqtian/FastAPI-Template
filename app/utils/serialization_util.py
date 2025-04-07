#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：serialization_util.py
@Author  ：晴天
@Date    ：2025-04-07 18:56:54
"""


def serialize_data(data: dict | list) -> dict | list:
    """
    序列化数据
    :param data: 待序列化的数据,可以是字典或列表
    :return: 删除敏感字段并返回处理好的数据
    """
    def serialize_item(item: dict) -> dict:
        """辅助函数，序列化字典项"""
        if "id" in item:
            item["id"] = str(item["id"])
        return item

    if isinstance(data, dict):  # 如果data是字典
        return serialize_item(data)

    elif isinstance(data, list):  # 如果data是列表
        return [serialize_item(item) for item in data if isinstance(item, dict)]

    return data
