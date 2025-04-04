#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：exceptions.py
@Author  ：晴天
@Date    ：2025-04-04 21:18:24
"""
from typing import Any, Dict, Optional
from fastapi import status, HTTPException


class BaseExceptions(HTTPException):
    """ 基础异常类 """

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "服务器内部错误"

    def __init__(self, message: Optional[str] = None, headers: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=self.status_code,
            detail={
                "code": self.status_code,
                "message": message or self.message
            },
            headers=headers
        )


class ValidationError(BaseExceptions):
    """ 参数校验异常 """
    status_code: int = status.HTTP_400_BAD_REQUEST
    message: str = "参数校验失败"


class AuthenticationError(BaseExceptions):
    """ 认证异常 """
    status_code: int = status.HTTP_401_UNAUTHORIZED
    message: str = "认证失败"


class PermissionDeniedError(BaseExceptions):
    """ 权限异常 """
    status_code: int = status.HTTP_403_FORBIDDEN
    message: str = "权限不足"


class NotFoundError(BaseExceptions):
    """ 资源不存在异常 """
    status_code: int = status.HTTP_404_NOT_FOUND
    message: str = "资源不存在"


class ResourceExistsError(BaseExceptions):
    """ 资源已存在异常 """
    status_code: int = status.HTTP_409_CONFLICT
    message: str = "资源已存在"


class BusinessError(BaseExceptions):
    """ 业务异常 """
    status_code: int = status.HTTP_400_BAD_REQUEST
    message: str = "业务异常"


class ServiceUnavailableError(BaseExceptions):
    """ 服务不可用异常 """
    status_code: int = status.HTTP_503_SERVICE_UNAVAILABLE
    message: str = "服务不可用"
