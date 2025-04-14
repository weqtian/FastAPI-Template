#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：user_service.py
@Author  ：晴天
@Date    ：2025-04-14 14:49:09
"""
from typing import Any, Dict, List
from app.core.logger import logger
from app.enums.status_code import StatusCode
from app.exceptions.custom import BusinessException
from app.repositories.user_repo import UserRepository
from beanie.odm.enums import SortDirection
from app.schemas.request.user import Pagination


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
        try:
            user = await self._user_repo.get_user_by_id(user_id)
        except Exception as e:
            logger.error(f"获取用户信息失败: {e}")
            raise BusinessException(code=StatusCode.SYSTEM_ERROR.get_code(),
                                    message=StatusCode.SYSTEM_ERROR.get_message())
        if not user:
            logger.error(f"用户不存在: {user_id}")
            raise BusinessException(code=StatusCode.USER_NOT_EXIST.get_code(),
                                    message=StatusCode.USER_NOT_EXIST.get_message())
        return user

    async def get_user_pagination_list(self, page: int = 1, page_size: int = 10, sort_by: int = 0) -> Dict[str, Any]:
        """
        获取用户分页列表
        :param page: 页码
        :param page_size: 每页数量
        :param sort_by: 排序方式
        :return: 用户分页列表
        """
        sort_by = SortDirection.DESCENDING if sort_by < 1 else SortDirection.ASCENDING
        try:
            users = await self._user_repo.user_pagination_list(
                page=page,
                page_size=page_size,
                sort_by=sort_by
            )
            return users
        except Exception as e:
            logger.error(f"获取用户分页列表失败: {e}")
            raise BusinessException(code=StatusCode.SYSTEM_ERROR.get_code(),
                                    message=StatusCode.SYSTEM_ERROR.get_message())
