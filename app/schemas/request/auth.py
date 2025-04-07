#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：auth.py
@Author  ：晴天
@Date    ：2025-04-04 17:33:08
"""
from fastapi import status
from pydantic import BaseModel, field_validator
from app.utils.validation_util import data_validation
from app.exceptions.custom import ValidationException


class RegisterUser(BaseModel):
    """ 注册用户 """

    email: str
    password: str
    nickname: str
    head_file_url: str
    gender: int
    birthday: str

    @field_validator('email')
    def check_email(cls, v: str):
        """
        验证邮箱地址
        :param v: 邮箱地址
        :return: 通过验证的合法邮箱地址
        """
        if not v:
            raise ValidationException(code=status.HTTP_400_BAD_REQUEST, message='邮箱地址不能为空')
        if not data_validation.is_valid_email(v):
            raise ValidationException(code=status.HTTP_400_BAD_REQUEST, message='邮箱地址格式不正确')
        return v.lower()

    @field_validator('password')
    def check_password(cls, v: str):
        """
        验证密码
        :param v: 密码
        :return: 通过验证的合法密码
        """
        if not v:
            raise ValidationException(code=status.HTTP_400_BAD_REQUEST, message='密码不能为空')
        if not data_validation.check_string_length(v, min_length=6, max_length=40):
            raise ValidationException(code=status.HTTP_400_BAD_REQUEST, message='密码长度必须在6到40个字符之间')
        return v

    @field_validator('nickname')
    def check_nickname(cls, v: str):
        """
        验证昵称
        :param v: 昵称
        :return: 通过验证的合法昵称
        """
        if not v:
            raise ValidationException(code=status.HTTP_400_BAD_REQUEST, message='昵称不能为空')
        if not data_validation.check_string_length(v, min_length=2, max_length=20):
            raise ValidationException(code=status.HTTP_400_BAD_REQUEST, message='昵称长度必须在2到20个字符之间')
        return v

    @field_validator('head_file_url')
    def check_head_file_url(cls, v: str):
        """
        验证头像地址
        :param v: 头像地址
        :return: 通过验证的合法头像地址
        """
        if not v:
            raise ValidationException(code=status.HTTP_400_BAD_REQUEST, message='头像地址不能为空')
        return v

    @field_validator('gender')
    def check_gender(cls, v: int):
        """
        验证性别
        :param v: 性别
        :return: 通过验证的合法性别
        """
        if not v:
            raise ValidationException(code=status.HTTP_400_BAD_REQUEST, message='性别不能为空')
        if not  data_validation.is_valid_gender(v):
            raise ValidationException(code=status.HTTP_400_BAD_REQUEST, message='性别不合法')
        return v

    @field_validator('birthday')
    def check_birthday(cls, v: str):
        """
        验证生日
        :param v: 生日
        :return: 通过验证的合法生日
        """
        if not v:
            raise ValidationException(code=status.HTTP_400_BAD_REQUEST, message='生日不能为空')
        if not data_validation.is_valid_date(v):
            raise ValidationException(code=status.HTTP_400_BAD_REQUEST, message='生日格式不正确')
        return v


    class Config:
        json_schema_extra = {
            'example': {
                "email": "weqtian@outlook.com",
                "password": "111111",
                "nickname": "晴天",
                "gender": 2,
                "birthday": "1999-07-14",
                "head_file_url": "https://s3-api.qingtian.dev/mqjc/prod/head/52111890/IMG_2378.jpeg"
            }

        }
