#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：logging.py
@Author  ：晴天
@Date    ：2025-04-07 10:29:10
"""
import time
import json
import uuid
from app.core.logger import logger
from fastapi import FastAPI, Request
from app.utils.request_util import request_util
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    自定义日志中间件，记录请求和响应详细信息
    """

    async def dispatch(self, request: Request, call_next):
        """
        处理请求和响应的日志记录
        :param request: 请求对象
        :param call_next: 下一个中间件或路由处理函数
        :return: 响应对象
        """
        # 生成唯一请求ID
        request_id = str(uuid.uuid4())
        start_time = time.time()

        # 获取请求信息
        request_info = await request_util.get_request_info(request)

        # 记录请求日志
        logger.info(f"Request: {request_info.model_dump()}")

        # 处理请求
        response = await call_next(request)

        # 计算处理时间
        process_time = time.time() - start_time

        # 获取响应内容
        response_body = ""
        if hasattr(response, "body_content"):
            try:
                response_body = b"".join(response.body_content).decode("utf-8")
            except UnicodeDecodeError:
                response_body = "[Binary content]"

        # 构造响应日志
        response_log = {
            "request_id": request_id,
            "status_code": response.status_code,
            "process_time": f"{process_time:.3f}s",
            "headers": dict(response.headers),
            "body": response_body if response_body else "[Empty response]",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }

        # 记录响应日志
        logger.info(f"Response: {json.dumps(response_log, ensure_ascii=False)}")

        return response


def register_logging_middleware(app: FastAPI):
    """
    注册请求日志中间件
    :param app: FastAPI 应用实例
    :return: None
    """
    app.add_middleware(LoggingMiddleware)  # type: ignore
