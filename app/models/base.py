#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：base.py
@Author  ：晴天
@Date    ：2025-04-04 19:19:37
"""
from typing import Dict, Any
from beanie import Document, PydanticObjectId


class BaseDocument(Document):
    """ 基础文档类 """

    class Config:
        """ Pydantic 配置 """
        json_encoders = {
            PydanticObjectId: str  # 将 PydanticObjectId 序列化为字符串
        }

    def to_dict(self, exclude_key: set[str] = None) -> Dict[str, Any]:
        """
        将数据转换成字典且自动处理MongoDB的ObjectId类型转换
        :return: 用户数据字典
        """
        exclude = {"id"}
        if exclude_key:
            exclude.update(exclude_key)
        data = self.model_dump(exclude=exclude)  # 排除原始 id 字段
        data["id"] = str(self.id)  # 添加字符串形式的 id
        return data
