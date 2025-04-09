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
from app.exceptions.base import BaseExceptions
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


def register_exception_handlers(app: FastAPI) -> None:
    """
    注册异常处理器
    :param app: FastAPI实例
    :return: None
    """

    @app.exception_handler(BaseExceptions)
    async def base_exception_handler(_: Request, exc: BaseExceptions):
        """
        处理自定义业务异常
        :param _: 请求对象（未使用）
        :param exc: 自定义业务异常实例
        :return: JSON响应
        """
        logger.error(f"BaseExceptions -> code: {exc.code} message: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"code": exc.code, "message": exc.message}
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(_: Request, exc: StarletteHTTPException):
        """
        处理FastAPI内置的HTTP异常
        :param _: 请求对象（未使用）
        :param exc: HTTP异常实例
        :return: JSON响应
        """
        logger.warning(f"HTTPException -> code: {exc.status_code} message: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"code": exc.status_code, "message": exc.detail}
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError):
        """
        处理请求参数验证异常
        :param _: 请求对象（未使用）
        :param exc: 请求验证异常实例
        :return: JSON响应
        """
        errors = exc.errors()
        error_msg = "; ".join([f"{err['loc'][-1]}: {err['msg']}" for err in errors])
        logger.warning(f"RequestValidationError -> {error_msg}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"code": status.HTTP_422_UNPROCESSABLE_ENTITY, "message": f"参数验证失败: {error_msg}"}
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(_: Request, exc: Exception):
        """
        处理未捕获的全局异常
        :param _: 请求对象（未使用）
        :param exc: 未捕获的异常实例
        :return: JSON响应
        """
        logger.critical(f"Unhandled Exception -> {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"code": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": "服务器内部错误"}
        )
