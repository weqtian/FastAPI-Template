#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：user.py
@Author  ：晴天
@Date    ：2025-04-04 16:12:37
"""
from pydantic import Field
from typing import Dict, Any
from datetime import datetime
from beanie import Document, PydanticObjectId


class User(Document):
    """ 用户表模型 """

    email: str
    password: str
    user_id: str
    display_id: str
    nickname: str
    head_file_url: str
    gender: int
    birthday: str
    is_active: bool = Field(default=True)
    is_deleted: bool = Field(default=False)
    create_time: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))
    update_time: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))
    create_date: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    update_date: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    create_by: str = Field(default="system")
    last_midify_update_by: str = Field(default="system")

    class Settings:
        # 定义集合名以及配置索引
        name = "user"
        indexes = ["email", "user_id", "display_id"]

    class Config:
        """Pydantic 配置"""
        json_encoders = {
            PydanticObjectId: str  # 将 PydanticObjectId 序列化为字符串
        }

    def to_dict(self) -> Dict[str, Any]:
        """
        将数据转换成字典且自动处理MongoDB的ObjectId类型转换
        :return: 用户数据字典
        """
        data = self.model_dump(exclude={"id", "password"})  # 排除原始 id 字段
        data["id"] = str(self.id)  # 添加字符串形式的 id
        return data
