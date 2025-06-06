#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：base.py
@Author  ：晴天
@Date    ：2025-04-04 21:18:24
"""


class BaseExceptions(Exception):
    """
    自定义异常基类

    code：业务状态码

    message：错误信息
    """
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(self.message)

