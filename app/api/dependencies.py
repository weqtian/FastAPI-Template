#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：dependencies.py
@Author  ：晴天
@Date    ：2025-04-04 16:53:53
"""
from fastapi import Depends
from app.services.user_service import UserService
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
