#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：mongodb_connet.py
@Author  ：晴天
@Date    ：2025-04-04 16:06:43
"""
from beanie import init_beanie
from app.models.user import User
from app.core.logger import logger
from app.core.config import config
from motor.motor_asyncio import AsyncIOMotorClient


class DataBaseManager:
    """ 数据库管理类 """

    def __init__(self):
        """ 初始化数据库连接 """
        self._client: AsyncIOMotorClient | None = None

    async def connect(self):
        """ 连接数据库 """
        try:
            logger.info("Starting MongoDB connection")
            self._client = AsyncIOMotorClient(config.DB_URI)
            await self._client[config.DB_NAME].command("ping")
            logger.info("MongoDB Connected Successfully")

            logger.info("Started Initializing Beanie Document Models")
            await init_beanie(database=self._client[config.DB_NAME], document_models=[User])
            logger.info("Finished Initializing Beanie Document Models")
        except Exception as e:
            logger.error(f"Connecting to MongoDB failed: {str(e)}")
            raise RuntimeError(f"Connecting to MongoDB failed: {str(e)}")

    async def disconnect(self):
        """ 关闭数据库连接 """
        try:
            if self._client:
                self._client.close()
                logger.info("Disconnected from MongoDB Successfully")
        except Exception as e:
            logger.error(f"Disconnecting from MongoDB failed: {str(e)}")


mongodb_manager = DataBaseManager()
