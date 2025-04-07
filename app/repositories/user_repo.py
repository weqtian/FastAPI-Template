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
from app.utils.serialization_util import serialize_data


class UserRepository:
    """ 用户数据库操作封装 """

    @staticmethod
    async def get_user_by_email(email: str) -> list | None:
        """
        根据邮箱获取用户
        :param email: 用户邮箱
        :return: User对象
        """
        try:
            user = await User.find(email=email).to_list()
            if not user:
                return None
            return serialize_data(user)
        except Exception as e:
            logger.error(f"查询用户异常: {e}")
            raise e

    @staticmethod
    async def create(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建用户
        :param user_data: 用户数据
        :return:
        """
        try:
            user = User(**user_data)
            await user.create()
            return user.to_dict(exclude_key={"password"})
        except Exception as e:
            logger.error(f"创建用户失败: {e}")
            raise e
