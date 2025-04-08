#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：auth.py
@Author  ：晴天
@Date    ：2025-04-04 17:42:54
"""
from app.schemas.response.base import Base
from app.schemas.response.user import UserInfo


class RegisterResponse(Base):
    """ 注册响应模型 """
    code: int = 200
    message: str = '注册成功'
    data: UserInfo

    class Config:
        json_schema_extra = {
            "example": {
              "code": 200,
              "message": "注册成功",
              "data": {
                "email": "weqtian@outlook.com",
                "user_id": "52111890",
                "display_id": "1314520",
                "nickname": "晴天",
                "head_file_url": "https://s3-api.qingtian.dev/mqjc/prod/head/52111890/IMG_2378.jpeg",
                "gender": 2,
                "birthday": "1999-07-14",
                "is_active": True,
                "is_deleted": False,
                "create_time": 1743763826,
                "update_time": 1743763826,
                "create_date": "2025-04-04 18:50:26",
                "update_date": "2025-04-04 18:50:26",
                "create_by": "system",
                "last_midify_update_by": "system",
                "id": "67efb9729391a1875b905edf"
              }
            }
        }
