#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：auth.py
@Author  ：晴天
@Date    ：2025-04-04 16:56:42
"""
from typing import Annotated
from fastapi import APIRouter, Depends
from app.schemas.response import Response
from app.schemas.security import DecodeTokenData
from app.services.auth_service import AuthService
from app.api.dependencies import get_auth_service, get_request_info, get_current_user
from app.schemas.request.auth import RegisterUser, LoginUser, RefreshToken


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register", summary="注册", response_model=Response, response_model_exclude_none=True)
async def register(user_data: RegisterUser, request = Depends(get_request_info),
                   auth_service: AuthService = Depends(get_auth_service)):
    """ 注册用户 """
    result = await auth_service.register(user_data, request)
    return Response(data=result)


@auth_router.post("/login", summary="登录", response_model=Response, response_model_exclude_none=True)
async def login(user_data: LoginUser, auth_service: AuthService = Depends(get_auth_service)):
    """ 登录用户 """
    result = await auth_service.login(user_data)
    return Response(data=result)


@auth_router.post("/logout", summary="退出登录", response_model=Response, response_model_exclude_none=True)
async def logout(current_user: Annotated[DecodeTokenData, Depends(get_current_user)],
                 auth_service: AuthService = Depends(get_auth_service)):
    """ 退出登录 """
    await auth_service.logout(current_user)
    return Response()


@auth_router.get('/refresh-token', summary="刷新token", response_model=Response, response_model_exclude_none=True)
async def refresh_token(token: RefreshToken, auth_service: AuthService = Depends(get_auth_service)):
    """ 刷新token """
    result = await auth_service.refresh_token(token)
    return Response(data=result)
