#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：user_repo.py
@Author  ：晴天
@Date    ：2025-04-04 17:23:35
"""
from typing import Dict, Any
from app.core.logger import logger
from app.models.user_model import User


class UserRepository:
    """用户数据库操作封装"""

    @staticmethod
    async def get_user_by_email(email: str, include_sensitive: bool = False) -> Dict[str, Any] | None:
        """
        根据邮箱获取用户
        :param email: 用户邮箱
        :param include_sensitive: 是否包含敏感信息
        :return: 用户信息
        """
        try:
            user = await User.find_one(User.email == email)
            return user.model_serialize(include_sensitive=include_sensitive) if user else None
        except Exception as e:
            logger.error(f"查询用户异常: {e}")
            raise

    @staticmethod
    async def get_user_by_id(user_id: str, include_sensitive: bool = False) -> Dict[str, Any] | None:
        """
        根据用户ID获取用户
        :param user_id: 用户ID
        :param include_sensitive: 是否包含敏感信息
        :return: 用户信息
        """
        try:
            user = await User.find_one(User.user_id == user_id)
            return user.model_serialize(include_sensitive=include_sensitive) if user else None
        except Exception as e:
            logger.error(f"查询用户异常: {e}")
            raise

    @staticmethod
    async def get_user_by_display_id(display_id: str, include_sensitive: bool = False) -> Dict[str, Any] | None:
        """
        根据用户展示ID获取用户
        :param display_id: 用户展示ID
        :param include_sensitive: 是否包含敏感信息
        :return: 用户信息
        """
        try:
            user = await User.find_one(User.display_id == display_id)
            return user.model_serialize(include_sensitive=include_sensitive) if user else None
        except Exception as e:
            logger.error(f"查询用户异常: {e}")
            raise

    @staticmethod
    async def create(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建用户
        :param user_data: 用户数据
        :return: 用户信息
        """
        try:
            user = User(**user_data)
            await user.create()
            return user.model_serialize()
        except Exception as e:
            logger.error(f"创建用户失败: {e}")
            raise

    @staticmethod
    async def update_user_by_id(user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any] | None:
        """
        根据用户ID更新用户
        :param user_id: 用户ID
        :param user_data: 用户数据
        :return: 用户信息
        """
        try:
            user = await User.find_one(User.user_id == user_id)
            if not user:
                return None
            await user.set(user_data)
            return user.model_serialize()
        except Exception as e:
            logger.error(f"更新用户失败: {e}")
            raise
