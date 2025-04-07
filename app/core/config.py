#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：config.py
@Author  ：晴天
@Date    ：2025-04-03 18:46:36
"""
import os
from dotenv import load_dotenv
from functools import lru_cache
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings

# 基础路径
BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 检查配置文件是否存在
if not os.path.exists(os.path.join(BASE_DIR, ".env")):
    raise FileNotFoundError("配置文件不存在，请检查项目根目录下是否存在 .env 文件")
# 加载配置文件
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))
# 检查日志目录是否存在
if not os.path.exists(os.path.join(BASE_DIR, "logs")):
    os.makedirs(os.path.join(BASE_DIR, "logs"))


class Config(BaseSettings):
    """ 基础配置类 """

    #================================== 项目配置 ==================================#
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "FAstAPI-Template")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION", "1.0.0")
    PROJECT_DESCRIPTION: str = os.getenv("PROJECT_DESCRIPTION", "FAstAPI Template")
    PROJECT_HOST: str = os.getenv("PROJECT_HOST", "0.0.0.0")
    PROJECT_PORT: int = os.getenv("PROJECT_PORT", 8000)
    PROJECT_DEBUG: bool = os.getenv("PROJECT_DEBUG", False)
    PROJECT_RELOAD: bool = os.getenv("PROJECT_RELOAD", False)
    PROJECT_ENV: str = os.getenv("PROJECT_ENV", "development")
    PROJECT_DOCS_URL: str = os.getenv("PROJECT_DOCS_URL", "/docs")
    PROJECT_REDOC_URL: str = os.getenv("PROJECT_REDOC_URL", "/redoc")
    PROJECT_OPENAPI_URL: str = os.getenv("PROJECT_OPENAPI_URL", "/openapi.json")
    PROJECT_API_PREFIX: str = os.getenv("PROJECT_API_PREFIX", "/api")
    PROJECT_SECRET_KEY: str = os.getenv("PROJECT_SECRET_KEY", "secret_key")
    PROJECT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("PROJECT_ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    PROJECT_REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("PROJECT_REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 24 * 7))

    # ================================== 路径配置 ==================================#
    LOG_DIR: str = os.path.join(BASE_DIR, "logs")

    #================================== 日志配置 ==================================#
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_OUTPUT_FILE: bool = os.getenv('LOG_OUTPUT_FILE', True)
    LOG_FORMAT: str = ("<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                      "<level>{level: <8}</level> | "
                      "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
    #================================== 数据库配置 ==================================#
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = os.getenv("DB_PORT", 27017)
    DB_USER: str = quote_plus(os.getenv("DB_USER", "root"))
    DB_PASSWORD: str = quote_plus(os.getenv("DB_PASSWORD", "123456"))
    DB_NAME: str = os.getenv("DB_NAME", "fastapi_template")
    DB_URI: str = f'mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}?authSource=admin'


class DevelopmentConfig(Config):
    """ 开发环境配置 """

    PROJECT_DEBUG: bool = False
    PROJECT_RELOAD: bool = True
    LOG_LEVEL: str = "DEBUG"


class TestingConfig(Config):
    """ 测试环境配置 """

    PROJECT_DEBUG: bool = False
    PROJECT_RELOAD: bool = True
    LOG_LEVEL: str = "DEBUG"


class ProductionConfig(Config):
    """ 生产环境配置 """

    PROJECT_DEBUG: bool = False
    PROJECT_RELOAD: bool = False
    LOG_LEVEL: str = "WARNING"



@lru_cache()
def get_config() -> Config:
    """
    获取配置
    :return: Config
    """
    base_config = Config() # 获取基础配置
    if base_config.PROJECT_ENV == "development":
        return DevelopmentConfig()
    elif base_config.PROJECT_ENV == "testing":
        return TestingConfig()
    elif base_config.PROJECT_ENV == "production":
        return ProductionConfig()
    else:
        raise ValueError("Invalid environment variable")


config = get_config()


if __name__ == '__main__':
    print('日志路径: ', config.DB_URI)
