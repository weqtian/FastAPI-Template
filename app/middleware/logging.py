#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：logging.py
@Author  ：晴天
@Date    ：2025-04-07 10:29:10
"""
import time
from app.core.logger import logger
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
        start_time = time.time()

        # 获取请求信息
        request_info = await request_util.get_request_info(request)
        logger.info(f'Request Info: '
                    f'url: {request_info.url} '
                    f'method: {request_info.method} '
                    f'header: {request_info.headers} '
                    f'query_params: {request_info.query_params} '
                    f'path_params: {request_info.path_params} '
                    f'body: {request_info.body} '
                    f'client_ip: {request_info.client_ip} '
                    f'timestamp: {request_info.timestamp} '
                    )

        # 继续处理请求
        response = await call_next(request)

        # 计算处理时间
        process_time = time.time() - start_time

        # 记录响应信息
        logger.info(f"Response completed: status={response.status_code}, time={process_time:.3f}s")
        return response
