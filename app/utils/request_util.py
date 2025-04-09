#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：request_util.py
@Author  ：晴天
@Date    ：2025-04-09 18:15:29
"""
from fastapi import Request
from datetime import datetime
from app.core.logger import logger
from app.enums.status_code import StatusCode
from app.exceptions.custom import ServiceException
from app.schemas.request.request_info import RequestInfo


class RequestUtil:
    """请求信息处理工具类，提供获取和记录请求信息的功能"""

    @staticmethod
    async def get_request_info(request: Request) -> RequestInfo:
        """
        获取完整的请求信息并封装成 RequestInfo 对象

        Args:
            request: FastAPI 的 Request 对象，包含所有请求相关信息

        Returns:
            RequestInfo: 封装了请求信息的模型实例

        Raises:
            HTTPException: 如果处理请求信息时发生严重错误
        """
        try:
            # 初始化请求体变量
            body = None
            # 对于需要处理请求体的 HTTP 方法
            if request.method in ["GET", "POST", "PUT", "PATCH"]:
                try:
                    # 尝试解析 JSON 格式的请求体
                    body = await request.json()
                except Exception:
                    try:
                        # 如果不是 JSON，尝试获取原始字节并解码为字符串
                        body = await request.body()
                        if isinstance(body, bytes):
                            body = body.decode("utf-8")
                    except Exception as e:
                        # 记录无法解析请求体的警告
                        logger.warning(f"Failed to parse request body: {e}")

            # 获取客户端 IP 地址，如果无法获取则使用 "unknown"
            client_ip = request.client.host if request.client else "unknown"

            # 创建并填充 RequestInfo 对象
            request_info = RequestInfo(
                method=request.method,  # 请求方法
                url=str(request.url),  # 请求的完整 URL
                headers=dict(request.headers),  # 请求头字典
                query_params=dict(request.query_params),  # 查询参数
                path_params=request.path_params,  # 路径参数
                body=body,  # 请求体内容
                client_ip=client_ip,  # 客户端 IP
                timestamp=datetime.now()  # 当前 UTC 时间
            )

            # 记录请求信息到日志
            logger.info(f"Request received: {request_info.model_dump()}")

            return request_info

        except Exception as e:
            # 记录错误并抛出 HTTP 异常
            logger.error(f"Error processing request info: {e}")
            raise ServiceException(code=StatusCode.SYSTEM_ERROR.value[0], message=StatusCode.SYSTEM_ERROR.value[1])


request_util = RequestUtil()
