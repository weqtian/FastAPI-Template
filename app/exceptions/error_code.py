#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：error_code.py
@Author  ：晴天
@Date    ：2025-04-07 18:52:50
"""
from enum import Enum


class ErrorCode(Enum):
    """ 错误码 """
    USER_NOT_FOUND = 1001
    USER_PASSWORD_ERROR = 1002
    USER_EMAIL_EXIST = 1003

    SERVER_ERROR = 500

