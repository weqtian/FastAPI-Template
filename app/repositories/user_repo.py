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
    """ 用户数据库操作封装 """

    @staticmethod
    async def create(user_data: Dict[str, Any]) -> User:
        """
        创建用户
        :param user_data: 用户数据
        :return:
        """
        try:
            user = User(**user_data)
            await user.create()
            return user
        except Exception as e:
            logger.error(f"创建用户失败: {e}")
            raise e
