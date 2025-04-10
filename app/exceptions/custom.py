#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：custom.py
@Author  ：晴天
@Date    ：2025-04-07 10:33:38
"""
from .base import BaseExceptions


class BusinessException(BaseExceptions):
    """通用业务异常"""
    pass

class AuthException(BaseExceptions):
    """认证异常"""

class ValidationException(BaseExceptions):
    """参数验证异常"""
    pass

class NotFoundException(BaseExceptions):
    """资源未找到异常"""
    pass

class DataBaseException(BaseExceptions):
    """数据库异常"""
    pass

class SerializationException(BaseExceptions):
    """序列化异常"""
    pass

class ServiceException(BaseExceptions):
    """服务异常"""
