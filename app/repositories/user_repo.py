#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：user_repo.py
@Author  ：晴天
@Date    ：2025-04-04 17:23:35
"""
from typing import Dict, Any
from app.models.user import User
from app.core.logger import logger


class UserRepository:
    """用户数据库操作封装"""

    @staticmethod
    async def get_user_by_email(email: str) -> Dict[str, Any] | None:
        """根据邮箱获取用户"""
        try:
            user = await User.find_one(User.email == email)
            return user.model_dump() if user else None
        except Exception as e:
            logger.error(f"查询用户异常: {e}")
            raise

    @staticmethod
    async def get_user_by_id(user_id: str) -> Dict[str, Any] | None:
        """根据用户 ID 获取用户"""
        try:
            user = await User.find_one(User.user_id == user_id)
            return user.model_dump() if user else None
        except Exception as e:
            logger.error(f"查询用户异常: {e}")
            raise

    @staticmethod
    async def get_user_by_display_id(display_id: str) -> Dict[str, Any] | None:
        """根据用户展示 ID 获取用户"""
        try:
            user = await User.find_one(User.display_id == display_id)
            return user.model_dump() if user else None
        except Exception as e:
            logger.error(f"查询用户异常: {e}")
            raise

    @staticmethod
    async def create(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建用户"""
        try:
            user = User(**user_data)
            await user.create()
            return user.model_dump()
        except Exception as e:
            logger.error(f"创建用户失败: {e}")
            raise
