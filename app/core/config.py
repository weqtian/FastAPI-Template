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
from urllib.parse import quote_plus


class Config:
    """ 基础配置类 """

    def __init__(self):
        """ 初始化配置 """
        if not os.path.exists(Config.ENV_FILE):
            raise FileNotFoundError(f"环境变量文件 {Config.ENV_FILE} 不存在")
        if not os.path.exists(Config.LOG_DIR):
            os.makedirs(Config.LOG_DIR)
        load_dotenv(dotenv_path=Config.ENV_FILE)

    #================================== 项目配置 ==================================#
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "FAstAPI-Template")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION", "1.0.0")
    PROJECT_DESCRIPTION: str = os.getenv("PROJECT_DESCRIPTION", "FAstAPI Template")
    PROJECT_HOST: str = os.getenv("PROJECT_HOST", "0.0.0.0")
    PROJECT_PORT: str = os.getenv("PROJECT_PORT", 8000)
    PROJECT_DEBUG: bool = os.getenv("PROJECT_DEBUG", True)
    PROJECT_RELOAD: bool = os.getenv("PROJECT_RELOAD", True)
    PROJECT_ENV: str = os.getenv("PROJECT_ENV", "development")
    PROJECT_DOCS_URL: str = os.getenv("PROJECT_DOCS_URL", "/docs")
    PROJECT_REDOC_URL: str = os.getenv("PROJECT_REDOC_URL", "/redoc")
    PROJECT_OPENAPI_URL: str = os.getenv("PROJECT_OPENAPI_URL", "/openapi.json")
    PROJECT_API_PREFIX: str = os.getenv("PROJECT_API_PREFIX", "/api")
    PROJECT_SECRET_KEY: str = os.getenv("PROJECT_SECRET_KEY", "secret_key")
    PROJECT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("PROJECT_ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    PROJECT_REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("PROJECT_REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 24 * 7))

    #================================== 路径配置 ==================================#
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    LOG_DIR: str = os.path.join(BASE_DIR, "logs")
    ENV_FILE: str = os.path.join(BASE_DIR, ".env")

    #================================== 日志配置 ==================================#
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_OUTPUT_FILE: bool = os.getenv('LOG_OUTPUT_FILE', True)
    LOG_FORMAT: str = ("<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                      "<level>{level: <8}</level> | "
                      "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
    #================================== 数据库配置 ==================================#
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", 27017)
    DB_USER: str = quote_plus(os.getenv("DB_USER", "root"))
    DB_PASSWORD: str = quote_plus(os.getenv("DB_PASSWORD", "123456"))
    DB_NAME: str = os.getenv("DB_NAME", "fastapi_template")
    DB_URI: str = f'mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}?authSource=admin'


class DevelopmentConfig(Config):
    """ 开发环境配置 """


class TestingConfig(Config):
    """ 测试环境配置 """


class ProductionConfig(Config):
    """ 生产环境配置 """


def get_config() -> Config:
    """
    获取配置
    :return: Config
    """
    if Config.PROJECT_ENV == "development":
        return DevelopmentConfig()
    elif Config.PROJECT_ENV == "testing":
        return TestingConfig()
    elif Config.PROJECT_ENV == "production":
        return ProductionConfig()
    else:
        raise ValueError("Invalid environment variable")


config = get_config()


if __name__ == '__main__':
    pass
    # config = get_config()
    # print('基础路径: ', config.BASE_DIR)
    # print('日志路径: ', config.DB_URI)
