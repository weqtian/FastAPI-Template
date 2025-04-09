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


class BaseResponse(BaseModel):
    """
    基础响应模型
    """
    code: int = 200
    message: str = "OK"
    data: Optional[Dict[str, Any]] = None
    errors: Optional[Dict[str, Any]] = None

