#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：logger.py
@Author  ：晴天
@Date    ：2025-04-04 16:02:59
"""
import sys
import os.path
from loguru import logger as loguru_logger
from app.core.config import get_config


class Logger:
    """ 日志类 """

    def __init__(self):
        """ 初始化日志 """
        self._logger = loguru_logger
        self._logger.remove()
        self._config = get_config()
        self._setup_logger()


    def _setup_logger(self):
        """ 初始化日志 """
        # 添加控制台日志
        self._logger.add(sys.stderr, format=self._config.LOG_FORMAT, level=self._config.LOG_LEVEL)
        # 添加文件日志
        if self._config.LOG_OUTPUT_FILE:
            # 按天轮转日志文件
            app_log_file = os.path.join(self._config.LOG_DIR, 'app_{time:YYYY-MM-DD}.log')
            self._logger.add(
                app_log_file,  # 日志文件路径
                format=self._config.LOG_FORMAT,  # 日志格式
                level=self._config.LOG_LEVEL,  # 日志级别
                rotation="00:00",  # 每天午夜
                compression="zip",  # 压缩旧文件
                retention="30 days",  # 保留30天
                encoding="utf-8",  # 文件编码
                diagnose=True,  # 诊断日志
            )

            # 添加错误日志单独保存
            error_log_file = os.path.join(self._config.LOG_DIR, 'error_{time:YYYY-MM-DD}.log')
            self._logger.add(
                error_log_file,
                format=self._config.LOG_FORMAT,
                level="ERROR",  # 仅捕获ERROR及以上级别
                rotation="00:00",  # 每天午夜
                compression="zip",  # 压缩旧文件
                retention="30 days",  # 保留30天
                encoding="utf-8",
                diagnose=True
            )


    def get_logger(self):
        """
        获取日志实例
        :return: 获取日志对象
        """
        return self._logger


logger = Logger().get_logger()
