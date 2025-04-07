#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：auth.py
@Author  ：晴天
@Date    ：2025-04-04 16:56:42
"""
from app.core.logger import logger
from app.services.user import UserService
from fastapi import APIRouter, Request, Depends
from app.schemas.request.auth import RegisterUser
from app.api.dependencies import get_user_service
from app.schemas.response.auth import RegisterResponse


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register", summary="注册", response_model=RegisterResponse, response_model_exclude_none=True)
async def register(request: Request, user_data: RegisterUser, user_service: UserService = Depends(get_user_service)):
    """ 注册用户 """
    logger.info(f'客户端请求IP: {request.client.host} 请求方法: {request.method} 当前请求参数: {user_data.model_dump()} ')
    return await user_service.register(user_data)


@auth_router.post("/login", summary="登录")
async def login():

    return {"message": "login"}


@auth_router.post("/logout", summary="退出登录")
async def logout():

    return {"message": "logout"}
