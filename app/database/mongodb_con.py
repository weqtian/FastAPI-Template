#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FastAPI-Template
@File    ：mongodb_connect.py
@Author  ：晴天
@Date    ：2025-04-04 16:06:43
"""
from typing import Optional
from beanie import init_beanie
from app.core.logger import logger
from app.core.config import config
from app.models.user_model import User
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError


class DatabaseManager:
    """ 管理 MongoDB 数据库连接和初始化，优化性能和可靠性。 """

    def __init__(self, uri: str = config.DB_URI, db_name: str = config.DB_NAME):
        """ 初始化数据库管理器，设置连接参数。 """
        self._uri: str = uri  # MongoDB 连接 URI
        self._db_name: str = db_name  # 数据库名称
        self._client: Optional[AsyncIOMotorClient] = None  # MongoDB 客户端实例
        self._database: Optional[AsyncIOMotorDatabase] = None  # MongoDB 数据库实例

    async def _initialize_beanie_odm(self):
        """ 初始化 Beanie ODM 模型。"""
        try:
            logger.info("Start initializing Beanie ODM")
            await init_beanie(
                database=self._database,
                document_models=[User],
                allow_index_dropping=False,  # 防止意外删除索引
                recreate_views=True,  # 确保视图一致性
            )
            logger.info("Beanie ODM initialization successful")
        except Exception as e:
            logger.error(f"Beanie ODM initialization failed: {str(e)}")
            raise

    async def connect(self) -> None:
        """ 建立 MongoDB 连接并初始化 Beanie ODM。 """
        logger.info(f"Start connecting to the MongoDB database: {self._db_name}")
        try:
            # 配置连接池和超时设置以优化性能
            self._client = AsyncIOMotorClient(
                self._uri,
                maxPoolSize=config.DB_MAX_CONNECTIONS,  # 最大连接池大小
                minPoolSize=1,  # 最小连接池大小
                serverSelectionTimeoutMS=5000,  # 服务器选择超时
                connectTimeoutMS=10000,  # 连接超时
                socketTimeoutMS=30000,  # 套接字超时
            )
            self._database = self._client[self._db_name]
            await self._database.command("ping")  # 验证连接是否成功
            logger.info("MongoDB connection successful")

            # 初始化 Beanie ODM
            await self._initialize_beanie_odm()
        except (ServerSelectionTimeoutError, ConfigurationError) as e:
            logger.error(f"MongoDB connection failure: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"An unknown error occurred during database initialization: {str(e)}")
            raise

    async def disconnect(self) -> None:
        """优雅地关闭 MongoDB 连接。"""
        if self._client is not None:
            try:
                self._client.close()
                logger.info("MongoDB connection closed")
            except Exception as e:
                logger.error(f"Failed to close MongoDB connection: {str(e)}")
                raise


# 创建单例数据库管理器
mongodb_manager = DatabaseManager()
