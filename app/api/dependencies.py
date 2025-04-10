#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：dependencies.py
@Author  ：晴天
@Date    ：2025-04-04 16:53:53
"""
from typing import Dict, Any
from fastapi import Request, Depends
from app.utils.request_util import request_util
from app.services.auth_service import UserService
from app.repositories.user_repo import UserRepository


async def get_user_repo() -> UserRepository:
    """
    获取用户数据库操作实例
    :return: UserRepository
    """
    return UserRepository()


async def get_user_service(repo: UserRepository = Depends(get_user_repo)) -> UserService:
    """
    获取用户服务实例
    :param repo: 用户数据库操作实例
    :return: UserService
    """
    return UserService(repo)


async def get_request_info(request: Request) -> Dict[str, Any]:
    """
    获取请求信息
    :return: request_util
    """
    request_info = await request_util.get_request_info(request)
    return request_info.model_dump()
