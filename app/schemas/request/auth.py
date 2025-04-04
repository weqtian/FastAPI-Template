#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：auth.py
@Author  ：晴天
@Date    ：2025-04-04 17:33:08
"""
from pydantic import BaseModel


class RegisterUser(BaseModel):
    """ 注册用户 """

    email: str
    password: str
    nickname: str
    head_file_url: str
    gender: int
    birthday: str

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
