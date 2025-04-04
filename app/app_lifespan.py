#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：app_lifespan.py
@Author  ：晴天
@Date    ：2025-04-04 16:40:09
"""
from fastapi import FastAPI
from app.core.logger import logger
from app.core.config import config
from contextlib import asynccontextmanager
from app.database.mongodb_connet import mongodb_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    管理应用的生命周期
    :param app: FastAPI实例
    :return: None
    """
    try:
        logger.info(f"Application Starting Lifespan Initializing Current Environment: {config.PROJECT_ENV}")
        await mongodb_manager.connect()
        logger.info("Application Lifespan Initialization Completed")
        yield
    except Exception as e:
        logger.error(f"Application Lifespan Initialization Fail: {e}")
        raise
    finally:
        await mongodb_manager.disconnect()