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

    用户模块：10001 - 20000
    系统模块：500 - 999
    通用模块：400 - 499（基于 HTTP 状态码的通用错误）
    """

    # ================================== 通用模块 状态码：400-499 ==================================
    # 成功（基于 HTTP 200，但这里用作业务成功标记）
    SUCCESS = (200, "OK")
    # 请求参数错误（HTTP 400）
    BAD_REQUEST = (400, "请求参数错误")
    # 未授权（HTTP 401）
    UNAUTHORIZED = (401, "未授权，请登录")
    # 禁止访问（HTTP 403）
    FORBIDDEN = (403, "禁止访问，权限不足")
    # 资源不存在（HTTP 404）
    NOT_FOUND = (404, "资源不存在")
    # 请求方法不支持（HTTP 405）
    METHOD_NOT_ALLOWED = (405, "请求方法不支持")
    # 请求过于频繁（HTTP 429）
    TOO_MANY_REQUESTS = (429, "请求过于频繁，请稍后再试")

    # ================================== 用户模块 状态码：10001-20000 ==================================
    # 该邮箱已注册
    EMAIL_ALREADY_REGISTERED = (10001, "该邮箱已注册")
    # 邮箱格式不正确
    EMAIL_FORMAT_ERROR = (10002, "邮箱格式不正确")
    # 密码长度不符规定
    PASSWORD_LENGTH_NOT_MATCH = (10003, "密码长度不符规定")
    # 昵称长度不符规定
    NICKNAME_LENGTH_NOT_MATCH = (10004, "昵称长度不符规定")
    # 性别错误
    SEX_ERROR = (10005, "性别错误")
    # 用户名或密码错误
    USERNAME_OR_PASSWORD_ERROR = (10006, "用户名或密码错误")
    # 用户不存在
    USER_NOT_EXIST = (10007, "用户不存在")
    # 用户已被禁用
    USER_DISABLED = (10008, "用户已被禁用")
    # 验证码错误
    CAPTCHA_ERROR = (10009, "验证码错误")
    # 验证码已过期
    CAPTCHA_EXPIRED = (10010, "验证码已过期")
    # 邮箱未注册
    EMAIL_NOT_REGISTERED = (10011, "邮箱未注册")
    # Header缺少 Authorization字段
    HEADER_MISSING_AUTHORIZATION = (10016, "Header缺少 Authorization字段")
    # Token 无效
    TOKEN_INVALID = (10012, "Token 无效")
    # Token 已过期
    TOKEN_EXPIRED = (10013, "Token 已过期")
    # 请使用access类型的Token进行访问
    TOKEN_TYPE_ERROR = (10014, "请使用access类型的Token进行访问")
    # 用户已存在
    USER_ALREADY_EXIST = (10015, "用户已存在")

    # ================================== 系统模块 状态码：500-999 ==================================
    # 系统错误（HTTP 500）
    SYSTEM_ERROR = (500, "服务内部错误")
    # 数据库操作失败
    DATABASE_ERROR = (501, "数据库操作失败")
    # 服务不可用（HTTP 503）
    SERVICE_UNAVAILABLE = (503, "服务暂时不可用")
    # 文件上传失败
    FILE_UPLOAD_ERROR = (510, "文件上传失败")
    # 文件大小超过限制
    FILE_SIZE_EXCEEDED = (511, "文件大小超过限制")
    # 配置错误
    CONFIG_ERROR = (520, "系统配置错误")
    # 第三方服务错误
    THIRD_PARTY_ERROR = (530, "第三方服务调用失败")

    # ================================== 方法扩展（可选） ==================================
    def get_code(self) -> int:
        """获取状态码"""
        return self.value[0]

    def get_message(self) -> str:
        """获取状态消息"""
        return self.value[1]


if __name__ == "__main__":
    # 示例用法
    # print(StatusCode.EMAIL_ALREADY_REGISTERED.value)  # (10001, '该邮箱已注册')
    # print(StatusCode.EMAIL_ALREADY_REGISTERED.get_code())  # 10001
    # print(StatusCode.EMAIL_ALREADY_REGISTERED.get_message())  # 该邮箱已注册
    pass