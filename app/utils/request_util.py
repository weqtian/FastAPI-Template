#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：request_util.py
@Author  ：晴天
@Date    ：2025-04-09 18:15:29
"""
from fastapi import Request
from app.core.logger import logger
from app.utils.date_util import date_util
from app.enums.status_code import StatusCode
from app.exceptions.custom import ServiceException
from app.schemas.request.request_info import RequestInfo


# 定义需要解析请求体的方法集合
BODY_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


class RequestUtil:
    """请求信息处理工具类，提供获取和记录请求信息的功能"""

    @staticmethod
    async def get_request_info(request: Request) -> RequestInfo:
        """
        获取完整的请求信息并封装成 RequestInfo 对象

        :param request: FastAPI 的 Request 对象，包含所有请求相关信息
        :return: RequestInfo 对象，封装了请求信息
        :raises ServiceException: 处理请求信息时发生错误，根据具体情况抛出不同状态码
        """
        try:
            # 初始化请求体变量
            body = None
            # 仅对需要解析请求体的方法处理
            if request.method in BODY_METHODS:
                content_type = request.headers.get("Content-Type", "").lower()
                if "application/json" in content_type:
                    try:
                        # 尝试解析 JSON 格式的请求体
                        body = await request.json()
                    except ValueError as e:
                        logger.debug(f"Failed to parse JSON body: {e}")
                        # JSON 解析失败，尝试获取原始数据
                        body = await RequestUtil._decode_body(request)
                else:
                    # 非 JSON 请求，直接获取原始数据
                    body = await RequestUtil._decode_body(request)

            # 获取客户端 IP 地址，处理无客户端的情况
            client_ip = request.client.host if request.client else "unknown"
            logger.info(f'path: {request.url.path}')
            # 创建并填充 RequestInfo 对象
            request_info = RequestInfo(
                method=request.method,
                url=str(request.url),
                path=request.url.path,
                host=client_ip,
                headers=dict(request.headers),
                query_params=dict(request.query_params),
                path_params=request.path_params,
                body=body,
                client_ip=client_ip,
                timestamp=date_util.to_iso_format(date_util.now()),  # 使用 UTC 时间
            )

            return request_info

        except ValueError as ve:
            logger.error(f"Invalid request data: {ve}")
            raise ServiceException(
                code=StatusCode.BAD_REQUEST.get_code(),
                message=StatusCode.BAD_REQUEST.get_message(),
            )
        except Exception as e:
            logger.error(f"Error processing request info: {e}")
            raise ServiceException(
                code=StatusCode.SYSTEM_ERROR.get_code(),
                message=StatusCode.SYSTEM_ERROR.get_message(),
            )

    @staticmethod
    async def _decode_body(request: Request) -> str | bytes | None:
        """
        辅助方法：解码请求体为字符串，处理非 JSON 情况

        :param request: FastAPI 的 Request 对象
        :return: 解码后的字符串或原始字节
        :raises ServiceException: 解码失败时抛出异常
        """
        try:
            body = await request.body()
            if not body:
                return None  # 空 body 返回 None
            if isinstance(body, bytes):
                return body.decode("utf-8", errors="replace")  # 解码失败时替换非法字符
            return body
        except Exception as e:
            logger.warning(f"Unable to decode request body: {e}")
            raise ServiceException(
                code=StatusCode.BAD_REQUEST.get_code(),
                message="Failed to decode request body",
            )


request_util = RequestUtil()