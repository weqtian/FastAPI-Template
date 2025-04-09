#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：logging.py
@Author  ：晴天
@Date    ：2025-04-07 10:29:10
"""
from fastapi import FastAPI, Request
from app.utils.request_util import request_util


def register_logging_middleware(app: FastAPI):
    """
    注册请求日志中间件
    :param app: FastAPI 应用实例
    :return: None
    """
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """
        记录请求信息的中间件函数
        :param request: 请求对象
        :param call_next: 下一个中间件或路由处理函数
        :return: 响应对象
        """
        # 获取请求信息
        await request_util.get_request_info(request)

        # 继续处理请求
        response = await call_next(request)
        return response
