#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：status_code.py
@Author  ：晴天
@Date    ：2025-04-07 18:52:50
"""
from enum import Enum


class StatusCode(Enum):
    """
    状态码枚举

    用户模块： 10001 - 20000
    系统模块： 500
    """

    #================================== 用户模块 状态码：1001-2000  ==================================
    # 该邮箱已注册
    EMAIL_ALREADY_REGISTERED = (10001, '该邮箱已注册')
    # 邮箱格式不正确
    EMAIL_FORMAT_ERROR = (10002, '邮箱格式不正确')
    # 密码长度不符规定
    PASSWORD_LENGTH_NOT_MATCH = (10003, '密码长度不符规定')
    # 昵称长度不符规定
    NICKNAME_LENGTH_NOT_MATCH = (10004, '昵称长度不符规定')
    # 性别错误
    SEX_ERROR = (10005, '性别错误')
    # 用户名或密码错误
    USERNAME_OR_PASSWORD_ERROR = (10006, '用户名或密码错误')
    # 用户不存在
    USER_NOT_EXIST = (10007, '用户不存在')

    #================================== 系统状态码：500  ==================================
    # 系统错误
    SYSTEM_ERROR = (500, '服务内部错误')


if __name__ == '__main__':
    pass
    # print(StatusCode.EMAIL_ALREADY_REGISTERED.value)