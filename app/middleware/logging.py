#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：logging.py
@Author  ：晴天
@Date    ：2025-04-07 10:29:10
"""
import time
import uuid
from typing import Optional
from app.core.logger import logger
from fastapi import FastAPI, Request
from app.utils.date_util import date_util
from app.utils.request_util import request_util
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, StreamingResponse


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    自定义日志中间件，记录请求和常规响应详细信息，包含链路ID，跳过流式或大body响应
    """

    TRACE_ID_HEADER = "X-Trace-ID"  # 链路ID的请求/响应头名称
    X_PROCESS_TIME = "X-Process-Time"  # 响应头中的处理时间名称

    @staticmethod
    async def _get_response_body(response: Response) -> Optional[str]:
        """
        获取响应体，仅处理常规响应，跳过流式或无法解码的响应
        :param response: 响应对象
        :return: 响应体字符串或占位符
        """
        if isinstance(response, StreamingResponse):
            return "[流式响应，跳过body记录]"

        try:
            return response.body.decode("utf-8") if response.body else None
        except (AttributeError, UnicodeDecodeError):
            return "[无法读取body，跳过]"

    @staticmethod
    def _get_trace_id(request: Request) -> str:
        """
        获取或生成链路ID
        :param request: 请求对象
        :return: 链路ID
        """
        trace_id = request.headers.get(LoggingMiddleware.TRACE_ID_HEADER)
        return trace_id if trace_id else str(uuid.uuid4())

    async def dispatch(self, request: Request, call_next):
        """
        处理请求和响应的日志记录，包含链路ID
        :param request: 请求对象
        :param call_next: 下一个中间件或路由处理函数
        :return: 响应对象
        """
        # 获取或生成链路ID
        trace_id = self._get_trace_id(request)
        start_time = time.time()

        # 获取并记录请求信息
        request_info = await request_util.get_request_info(request)
        request_detail = {
            "trace_id": trace_id,
            "request_detail": request_info.model_dump()
        }
        logger.info(f"Request: {request_detail}")

        # 处理请求
        response = await call_next(request)

        # 计算处理时间
        process_time = time.time() - start_time

        # 获取响应体
        response_body = await self._get_response_body(response)

        # 构造响应日志
        response_detail = {
            "trace_id": trace_id,
            "response_detail": {
                "trace_id": trace_id,
                "status_code": response.status_code,
                "process_time": f"{process_time:.3f}s",
                "headers": dict(response.headers),
                "body": response_body if response_body else "[空响应]",
                "timestamp": date_util.to_iso_format(date_util.now())
            }
        }

        # 记录响应日志
        logger.info(f"Response: {response_detail}")

        # 在响应头中添加链路ID
        response.headers[self.TRACE_ID_HEADER] = trace_id
        # 在响应头中添加处理耗时
        response.headers[self.X_PROCESS_TIME] = f"{process_time:.3f}s"

        return response


def register_logging_middleware(app: FastAPI):
    """
    注册请求日志中间件
    :param app: FastAPI 应用实例
    :return: None
    """
    app.add_middleware(LoggingMiddleware)  # type: ignore
