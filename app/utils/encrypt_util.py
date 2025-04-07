#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：encrypt_util.py
@Author  ：晴天
@Date    ：2025-04-07 18:10:15
"""
import bcrypt


def encrypt_password(password):
    """
    对密码进行加密
    :param password: 待加密的密码
    :return: 密文
    """
    password = password.encode('utf-8')  # 将密码编码为字节
    salt = bcrypt.gensalt()  # 生成一个随机的盐值
    hashed_password = bcrypt.hashpw(password, salt)  # 使用盐值对密码进行哈希计算
    return hashed_password.decode('utf-8')  # 将加密后的密码转换为字符串格式并返回


def verify_password(password, hashed_password):
    """
    验证密码是否匹配
    :param password: 明文密码
    :param hashed_password: 密文密码
    :return: True/False
    """
    password = password.encode('utf-8')  # 将输入的密码编码为字节
    hashed_password = hashed_password.encode('utf-8')  # 将加密后的密码编码为字节
    return bcrypt.checkpw(password, hashed_password)

