#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：auth.py
@Author  ：晴天
@Date    ：2025-04-04 16:56:42
"""
from fastapi.exceptions import RequestValidationError
from app.core.logger import logger
from app.services.user import UserService
from app.exceptions.base import BaseExceptions
from app.schemas.request.auth import RegisterUser
from app.api.dependencies import get_user_service
from app.schemas.response.auth import RegisterResponse
from fastapi import APIRouter, Request, Depends, HTTPException


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register", summary="注册", response_model=RegisterResponse, response_model_exclude_none=True)
async def register(request: Request, user_data: RegisterUser, user_service: UserService = Depends(get_user_service)):
    """ 注册用户 """
    logger.info(f'客户端请求IP: {request.client.host} 请求方法: {request.method} 当前请求参数: {user_data.model_dump()} ')
    try:
        return await user_service.register(user_data)
    except Exception as e:
        logger.error(f"注册用户失败: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@auth_router.post("/login", summary="登录")
async def login():

    return {"message": "login"}


@auth_router.post("/logout", summary="退出登录")
async def logout():

    return {"message": "logout"}



@auth_router.get("/test")
async def test_endpoint():
    return {"code": 0, "message": "成功"}

@auth_router.get("/test-business-error")
async def test_business_error():
    raise BaseExceptions(code=1001, message="业务逻辑错误示例")

@auth_router.get("/test-http-error")
async def test_http_error():
    raise HTTPException(status_code=400, detail="请求参数错误")

@auth_router.get("/test-validation-error")
async def test_validation_error():
    raise RequestValidationError(errors=[{"loc": ["query", "id"], "msg": "invalid id"}])

@auth_router.get("/test-unexpected-error")
async def test_unexpected_error():
    raise ZeroDivisionError("除以零错误")
