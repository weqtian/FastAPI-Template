#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：app_factory.py
@Author  ：晴天
@Date    ：2025-04-04 16:09:00
"""
from fastapi import FastAPI
from app.core.config import config
from app.app_lifespan import lifespan
from app.api.routers import register_routers


def create_app() -> FastAPI:
    """
    FastAPI 工厂函数
    :return: FastAPI 实例
    """
    app = FastAPI(
        title=config.PROJECT_NAME,
        description=config.PROJECT_DESCRIPTION,
        version=config.PROJECT_VERSION,
        lifespan=lifespan,
        debug=config.PROJECT_DEBUG,
        docs_url=config.PROJECT_DOCS_URL,
        redoc_url=config.PROJECT_REDOC_URL,
        openapi_url=config.PROJECT_OPENAPI_URL
    )

    # 注册路由
    register_routers(app)

    return app
