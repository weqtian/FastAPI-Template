#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：user_service.py
@Author  ：晴天
@Date    ：2025-04-14 14:49:09
"""
from typing import Any, Dict
from app.core.logger import logger
from app.enums.status_code import StatusCode
from app.exceptions.custom import BusinessException
from app.repositories.user_repo import UserRepository


class UserService:
    """ 用户服务 """

    def __init__(self, repo: UserRepository):
        self._user_repo = repo

    async def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """
        获取用户信息
        :param user_id: 用户id
        :return: 用户信息
        """
        user = await self._user_repo.get_user_by_id(user_id)
        if not user:
            logger.error(f"用户不存在: {user_id}")
            raise BusinessException(code=StatusCode.USER_NOT_EXIST.get_code(),
                                    message=StatusCode.USER_NOT_EXIST.get_message())
        return user
