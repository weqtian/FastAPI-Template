#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：user_repo.py
@Author  ：晴天
@Date    ：2025-04-04 17:23:35
"""
from typing import Dict, Any, List
from app.core.logger import logger
from app.models.user_model import User
from beanie.odm.enums import SortDirection
from app.schemas.pagination import PaginationResult


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

    @staticmethod
    async def user_pagination_list(
            page: int = 1,
            page_size: int = 10,
            sort_field: List[str] = None,
            sort_by: SortDirection = SortDirection.DESCENDING,
            filters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        获取用户分页列表
        :param page: 页码
        :param page_size: 每页数量
        :param sort_field: 排序字段，例如 create_date
        :param sort_by: 排序方式 DESCENDING: 降序, ASCENDING: 升序，默认: SortDirection.DESCENDING
        :param filters: 过滤条件，例如 {"is_active": True}
        :return: 分页结果
        """
        try:
            # 默认过滤条件：未删除的用户
            query_filters = {"is_deleted": False}
            if filters:
                query_filters.update(filters)
            # 创建查询
            query = User.find(query_filters)
            # 应用排序
            if sort_field:
                for field in sort_field:
                    query = query.sort((field, sort_by))
            else:
                # 默认按创建时间降序
                query = query.sort([("create_date", sort_by)])
            # 计算总数
            total = await query.count()
            # 应用分页
            skip = (page - 1) * page_size
            users = await query.skip(skip).limit(page_size).to_list()
            # 序列化结果
            user_list = [user.model_serialize() for user in users]
            return PaginationResult(list=user_list, total=total, page=page, page_size=page_size).model_dump()
        except Exception as e:
            logger.error(f"获取用户分页列表失败: {e}")
            raise
