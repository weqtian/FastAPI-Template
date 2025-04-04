#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：base.py
@Author  ：晴天
@Date    ：2025-04-04 17:39:36
"""
from pydantic import BaseModel
from typing import Any, Dict, Optional


class Base(BaseModel):
    """ 基础响应模型 """

    code: int = 200
    message: str = 'success'
    data: Optional[Dict[str, Any]] = None


class SuccessResponse(Base):
    """ 成功响应模型 """
    code: int = 200
    message: str = 'success'
    data: Optional[Dict[str, Any]] = None


class FailResponse(Base):
    """ 失败响应模型 """

    code: int = 500
    message: str = 'fail'
    detail: Optional[Dict[str, Any]] = None
