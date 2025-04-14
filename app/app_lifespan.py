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
from app.database.mongodb_con import mongodb_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    管理应用的生命周期
    :param app: FastAPI实例
    :return: None
    """
    logger.info(f"Application startup, current environment: {config.PROJECT_ENV}")
    try:
        await mongodb_manager.connect()  # 初始化数据库连接
        logger.info("Application life cycle initialization successful")
        yield  # 应用运行期间
    except Exception as e:
        logger.error(f"Lifecycle initialization failed: {str(e)}")
        raise
    finally:
        try:
            await mongodb_manager.disconnect()  # 清理数据库连接
            logger.info("Application life cycle shutdown completed")
        except Exception as e:
            logger.error(f"An error occurred while closing the app: {str(e)}")
            raise