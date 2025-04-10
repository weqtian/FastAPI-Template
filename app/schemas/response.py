#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FastAPI-Template
@File    ：response.py
@Author  ：晴天
@Date    ：2025-04-10 10:35:14
"""
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from app.enums.status_code import StatusCode


class Response(BaseModel):
    """
    通用响应模型，用于 FastAPI 项目中的 API 返回值。

    :param code: 业务状态码，例如 200 表示成功，400 表示客户端错误。
    :param message: 状态描述信息，例如 "操作成功" 或 "参数错误"。
    :param data: 业务数据，成功时返回的具体内容，类型由泛型 T 指定。
    :param errors: 错误详情，失败时返回的错误信息，通常为字典形式。
    :param timestamp: 响应生成时间，默认为 UTC 时间。
    """
    code: int = Field(default=StatusCode.SUCCESS.get_code(), description="业务状态码")
    message: str = Field(default=StatusCode.SUCCESS.get_message(), description="状态描述信息")
    data: Optional[Dict[str, Any]] = Field(default=None, description="业务数据")
    errors: Optional[Dict[str, Any]] = Field(default=None, description="业务数据")
    timestamp: datetime = Field(default=datetime.now(), description="响应生成时间")

    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "message": "操作成功",
                "data": None,
                "errors": None,
                "timestamp": "2023-10-01T12:34:56.789Z"
            }
        }
