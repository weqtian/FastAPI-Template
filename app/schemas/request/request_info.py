#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：request_info.py
@Author  ：晴天
@Date    ：2025-04-09 18:18:28
"""
from datetime import datetime
from pydantic import BaseModel
from typing import Dict, Any, Optional


class RequestInfo(BaseModel):
    """
    请求信息的数据模型，用于结构化存储请求的各项信息
    """

    method: str  # HTTP 请求方法（如 GET, POST）
    url: str  # 完整的请求 URL
    path: str  # 请求路径
    host: str  # 请求主机
    headers: Dict[str, str]  # 请求头信息
    query_params: Dict[str, Any]  # URL 查询参数
    path_params: Dict[str, Any]  # 路径参数
    body: Optional[Any] = None  # 请求体内容（可选）
    client_ip: str  # 客户端 IP 地址
    timestamp: str  # 请求时间戳
