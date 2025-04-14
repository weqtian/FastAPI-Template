#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：dependencies.py
@Author  ：晴天
@Date    ：2025-04-04 16:53:53
"""
from typing import Dict, Any, Annotated
from app.core.security import jwt_manager
from app.enums.status_code import StatusCode
from app.exceptions.custom import AuthException
from app.utils.request_util import request_util
from app.schemas.security import DecodeTokenData
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.repositories.user_repo import UserRepository
from fastapi import Request, Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# 定义 HTTPBearer 用于提取 Token
security_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
        credentials: Annotated[HTTPAuthorizationCredentials | None,
        Security(security_scheme)] = None) -> DecodeTokenData:
    """
    依赖函数：解析和验证 Token，返回用户信息
    :param credentials: 从请求头中提取的 Authorization 凭证
    :return: DecodeTokenData
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=StatusCode.HEADER_MISSING_AUTHORIZATION.get_message(),
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        decoded_data = jwt_manager.decode_token(credentials.credentials)
        if decoded_data.type != "access":
            raise AuthException(
                code=StatusCode.TOKEN_TYPE_ERROR.get_code(),
                message=StatusCode.TOKEN_TYPE_ERROR.get_message()
            )
        user = await UserRepository.get_user_by_id(decoded_data.user_id, True)
        if not user or credentials.credentials !=  user.get('access_token'):
            raise AuthException(code=StatusCode.TOKEN_INVALID.get_code(),
                                message=StatusCode.TOKEN_INVALID.get_message())
        return decoded_data
    except AuthException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_user_repo() -> UserRepository:
    """
    获取用户数据库操作实例
    :return: UserRepository
    """
    return UserRepository()


async def get_auth_service(repo: UserRepository = Depends(get_user_repo)) -> AuthService:
    """
    获取授权服务实例
    :param repo: 用户数据库操作实例
    :return: UserService
    """
    return AuthService(repo)

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
