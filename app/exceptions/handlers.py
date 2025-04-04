#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：handlers.py
@Author  ：晴天
@Date    ：2025-04-04 21:29:01
"""
from app.core.logger import logger
from fastapi.responses import JSONResponse
from fastapi import Request, FastAPI, status
from app.exceptions.exceptions import BaseExceptions
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


def register_exception_handlers(app: FastAPI) -> None:
    """
    注册异常处理器
    :param app: FastAPI实例
    :return: None
    """

    @app.exception_handler(BaseExceptions)
    async def base_exception_handler(request: Request, exc: BaseExceptions) -> JSONResponse:
        """
        异常处理器
        :param request: 请求对象
        :param exc: 异常对象
        :return:
        """
        logger.error(
            f"业务异常: {exc.detail} | 状态码: {exc.status_code} | URL: {request.url} | "
            f"方法: {request.method} | 路径: {request.url.path}"
            f"请求IP: {request.client.host} | 请求参数: {request.user.model_dump()}"
        )
        return JSONResponse(status_code=exc.status_code, content=exc.detail)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        """
        参数校验异常处理器
        :param request: 请求对象
        :param exc: 异常对象
        :return:
        """
        errors = []
        for error in exc.errors():
            error_loc = " -> ".join([str(loc) for loc in error["loc"] if loc != "body"])
            errors.append({
                "location": error_loc,
                "message": error["msg"],
                "type": error["type"]
            })
        logger.warning(
            f"验证异常 | URL: {request.url} | 客户端: {request.client.host} | "
            f"方法: {request.method} | 路径: {request.url.path} | 错误详情: {errors}"
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"code": status.HTTP_400_BAD_REQUEST, "message": "请求参数错误", "errors": errors}
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        """ HTTP异常处理器 """
        logger.error(
            f"HTTP异常: {exc.detail} | 状态码: {exc.status_code} | URL: {request.url} | "
            f"方法: {request.method} | 路径: {request.url.path}"
            f"请求IP: {request.client.host}"
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={"code": exc.status_code, "message": exc.detail}
        )

    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """ 全局异常处理器 """
        logger.error(
            f"未知异常: {exc} | URL: {request.url} | 方法: {request.method} | 路径: {request.url.path} "
            f"请求IP: {request.client.host}"
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"code": 500, "message": "服务器内部错误"}
        )