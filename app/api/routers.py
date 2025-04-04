#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：routers.py
@Author  ：晴天
@Date    ：2025-04-04 16:54:10
"""
from fastapi import FastAPI
from app.core.config import config
from app.core.logger import logger
from app.api.endpoints.auth import auth_router


def register_routers(app: FastAPI) -> None:
    """
    注册路由
    :param app: FastAPI实例
    :return: None
    """
    app.include_router(auth_router, prefix=config.PROJECT_API_PREFIX)
