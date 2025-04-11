#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：user_model.py
@Author  ：晴天
@Date    ：2025-04-04 16:12:37
"""
from pydantic import Field
from typing import ClassVar
from datetime import datetime
from app.models.base import BaseDocument


class User(BaseDocument):
    """用户表模型，继承自 BaseDocument"""

    # 邮箱地址
    email: str = Field(..., description="用户邮箱地址，唯一标识用户身份，符合邮箱格式")
    # 用户ID，系统生成的唯一标识符
    user_id: str = Field(..., description="用户唯一标识符，系统生成的 ID")
    # 用户展示 ID，用于前端显示的唯一标识
    display_id: str = Field(..., description="用户展示 ID，用于前端显示的唯一标识")
    # 用户昵称，展示名称，最多 50 个字符
    nickname: str = Field(..., max_length=50, description="用户昵称，展示名称，最多 50 个字符")
    # 用户头像文件 URL，指向头像存储位置
    head_file_url: str = Field(..., description="用户头像文件 URL，指向头像存储位置")
    # 用户性别，0 表示未知，1 表示男，2 表示女
    gender: int = Field(..., ge=0, le=2, description="用户性别，0 表示未知，1 表示男，2 表示女")
    # 用户生日，格式为 'YYYY-MM-DD'
    birthday: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="用户生日，格式为 'YYYY-MM-DD'")
    # 用户密码 敏感字段，序列化时排除
    password: str = Field(..., min_length=8, description="用户密码，加密后的哈希值，至少 8 位", exclude=True)
    # 创建IP地址，记录用户创建记录时的 IP 地址
    create_ip: str | None = Field(default=None, description="创建IP地址，记录用户创建记录时的 IP 地址")
    # 用户角色，用于权限控制，如 'admin'、'user' 等
    role_id: str | None = Field(default=None, description="用户角色ID，用于权限控制，如 'admin'、'user' 等")
    # 记录激活状态，True 表示记录有效，False 表示记录被禁用
    is_active: bool = Field(default=True, description="记录是否激活，True 表示激活（有效），False 表示禁用")
    # 逻辑删除标志，True 表示记录已被删除（软删除），False 表示未删除
    is_deleted: bool = Field(default=False, description="记录是否逻辑删除，True 表示已删除（软删除），False 表示未删除")
    # 创建时间戳，以毫秒为单位，用于记录创建的精确时间
    create_time: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000), description="记录创建时间戳（毫秒），表示记录创建的精确时间")
    # 创建日期时间，使用 ISODate 格式，便于人类阅读和查询
    create_date: datetime = Field(default_factory=datetime.now, description="记录创建日期时间，ISODate 格式，便于人类阅读和查询")
    # 创建者标识，记录是谁创建了这条记录，默认值为 "system"
    create_by: str = Field(default="system", description="记录创建者标识，表示创建此记录的用户或系统，默认值为 'system'")
    # 最后修改者标识，记录最后修改此记录的用户或系统
    last_modify_by: str = Field(default="system", description="最后修改者标识，表示最后修改此记录的用户或系统，默认值为 'system'")
    # 最后修改时间戳，以毫秒为单位，记录最后一次修改的精确时间
    last_modify_time: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000), description="最后修改时间戳（毫秒），表示记录最后一次修改的精确时间")
    # 最后修改日期时间，使用 ISODate 格式，记录最后修改的时间
    last_modify_date: datetime = Field(default_factory=datetime.now, description="最后修改日期时间，ISODate 格式，表示记录最后修改的时间")
    # 敏感字段，序列化时排除
    access_token: str | None = Field(default=None, description="用户访问令牌，用于身份验证，可为空", exclude=True)
    # 敏感字段，序列化时排除
    refresh_token: str | None = Field(default=None, description="用户刷新令牌，用于更新访问令牌，可为空", exclude=True)

    # 启用字段排序，确保字段按照定义的顺序存储
    enforce_field_order: ClassVar[bool] = True  # 启用字段排序

    class Settings:
        """Beanie 配置"""
        name = "user"
        indexes = [
            "email",
            "user_id",
            "display_id",
            [("email", 1), ("user_id", 1)],  # 复合索引
            [("create_date", -1)],  # 按创建时间降序
            [("is_active", 1)],  # 按激活状态查询
            [("is_deleted", 1)],  # 按删除状态查询
        ]
        use_state_management = True  # 启用状态管理
