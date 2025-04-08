#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：user.py
@Author  ：晴天
@Date    ：2025-04-04 16:12:37
"""
from pydantic import Field
from datetime import datetime
from app.models.base import BaseDocument


class User(BaseDocument):
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
    create_date: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    create_by: str = Field(default="system")
    last_midify_update_by: str = Field(default="system")
    last_modify_update_time: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))
    last_modify_update_date: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    access_token: str = Field(default=None)
    refresh_token: str = Field(default=None)

    class Settings:
        # 定义集合名以及配置索引
        name = "user"
        indexes = ["email", "user_id", "display_id"]
