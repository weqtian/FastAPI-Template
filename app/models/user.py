#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：user.py
@Author  ：晴天
@Date    ：2025-04-04 16:12:37
"""
from pydantic import Field
from app.models.base import BaseDocument


class User(BaseDocument):
    """用户表模型，继承自 BaseDocument"""

    email: str = Field(..., description="用户邮箱地址，唯一标识用户身份，符合邮箱格式")
    password: str = Field(..., min_length=8, description="用户密码，加密后的哈希值，至少 8 位", exclude=True)# 敏感字段，序列化时排除
    user_id: str = Field(..., description="用户唯一标识符，系统生成的 ID")
    display_id: str = Field(..., description="用户展示 ID，用于前端显示的唯一标识")
    nickname: str = Field(..., max_length=50, description="用户昵称，展示名称，最多 50 个字符")
    head_file_url: str = Field(..., description="用户头像文件 URL，指向头像存储位置")
    gender: int = Field(..., ge=0, le=2, description="用户性别，0 表示未知，1 表示男，2 表示女")
    birthday: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="用户生日，格式为 'YYYY-MM-DD'")
    access_token: str | None = Field(default=None, description="用户访问令牌，用于身份验证，可为空", exclude=True) # 敏感字段，序列化时排除
    refresh_token: str | None = Field(default=None, description="用户刷新令牌，用于更新访问令牌，可为空", exclude=True) # 敏感字段，序列化时排除

    # User 类没有额外的 datetime 字段需要格式化，因此无需扩展 datetime_fields_to_format

    class Settings:
        """Beanie 配置"""
        name = "user"
        indexes = [
            "email",
            "user_id",
            "display_id",
            [("email", 1), ("user_id", 1)]  # 复合索引
        ]
        use_state_management = True  # 启用状态管理
