#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：user.py
@Author  ：晴天
@Date    ：2025-04-04 17:46:42
"""
from app.core.logger import logger
from app.schemas.request.auth import RegisterUser
from app.exceptions.custom import BusinessException
from app.utils.user_id_util import generate_user_id
from app.repositories.user_repo import UserRepository
from app.schemas.response.auth import RegisterResponse
from app.utils.encrypt_util import encrypt_password, verify_password


class UserService:
    """ 用户服务 """

    def __init__(self, repo: UserRepository):
        self._repo = repo

    async def register(self, user_data: RegisterUser) -> RegisterResponse:
        """ 注册用户 """

        user = await self._repo.create({**user_data.model_dump(), "user_id": "52111890", "display_id": "1314520"})
        return RegisterResponse(data=user)
