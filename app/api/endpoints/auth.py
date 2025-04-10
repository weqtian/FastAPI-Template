#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：auth.py
@Author  ：晴天
@Date    ：2025-04-04 16:56:42
"""
from fastapi import APIRouter, Depends
from app.schemas.response import Response
from app.services.user_service import UserService
from app.api.dependencies import get_user_service, get_request_info
from app.schemas.request.auth import RegisterUser, LoginUser


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register", summary="注册", response_model=Response, response_model_exclude_none=True)
async def register(user_data: RegisterUser, request = Depends(get_request_info),
                   user_service: UserService = Depends(get_user_service)):
    """ 注册用户 """
    result = await user_service.register(user_data, request)
    return Response(data=result)


@auth_router.post("/login", summary="登录", response_model=Response, response_model_exclude_none=True)
async def login(user_data: LoginUser, request = Depends(get_request_info),
                user_service: UserService = Depends(get_user_service)):
    """ 登录用户 """
    result = await user_service.login(user_data, request)
    return Response(data=result)


@auth_router.post("/logout", summary="退出登录")
async def logout():

    return {"message": "logout"}
