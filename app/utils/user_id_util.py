#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：user_id_util.py
@Author  ：晴天
@Date    ：2025-04-07 17:28:59
"""
import time
import random
import socket
import hashlib



def get_server_id():
    # 可以返回服务器的唯一标识符，例如主机名的一部分
    return str(socket.gethostname()).encode('utf-8')


def generate_user_id() -> str:
    """
    生成用户ID
    :return: 返回用户ID
    """
    # 获取当前时间的微秒时间戳
    timestamp = int(time.time() * 1_000_000)  # 转为微秒
    # 生成随机数字，增加到8位
    random_digits = random.randint(10000000, 99999999)

    # 拼接时间戳、随机数和服务器标识符信息
    server_id = get_server_id()
    unique_string = f"{timestamp}{random_digits}{server_id}"

    # 计算SHA256哈希并转为数字
    hash_object = hashlib.sha256(unique_string.encode())
    hash_hex = hash_object.hexdigest()

    # 截取前10位作为用户ID
    user_id = int(hash_hex, 16) % 10 ** 10  # 取模确保ID为10位数字

    return str(user_id)


if __name__ == '__main__':
    pass
    # print('host_id: ', get_server_id().decode('utf-8'))
    # print('user_id: ', generate_user_id())