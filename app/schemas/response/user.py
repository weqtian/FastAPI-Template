#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：user.py
@Author  ：晴天
@Date    ：2025-04-08 14:18:48
"""
from pydantic import BaseModel


class UserInfo(BaseModel):
    id: str
    email: str
    user_id: str
    display_id: str
    nickname: str
    head_file_url: str
    gender: int
    birthday: str
    is_active: bool
    create_date: str
    last_modify_date: str
    create_by: str
    last_modify_by: str
