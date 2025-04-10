#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：security.py
@Author  ：晴天
@Date    ：2025-04-10 16:24:46
"""
from pydantic import BaseModel, Field


class TokenData(BaseModel):
    """ token数据 """

    access_token: str = Field(..., description="访问token")
    token_type: str = Field(..., description="token类型")
    refresh_token: str = Field(..., description="刷新token")
    expire: int = Field(..., description="过期时间")
    user_id: str = Field(..., description="用户id")
    nickname: str = Field(..., description="用户昵称")



class DecodeTokenData(BaseModel):
    """ token解码数据 """

    user_id: str = Field(..., description="用户id")
    nickname: str = Field(..., description="用户昵称")
