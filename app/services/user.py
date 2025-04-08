#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：user.py
@Author  ：晴天
@Date    ：2025-04-04 17:46:42
"""
from app.core.logger import logger
from app.exceptions.error_code import ErrorCode
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
        """
        注册用户
        :param user_data: 用户数据
        :return: 用户信息
        """
        email_is_exist = await self._repo.get_user_by_email(user_data.email)
        if email_is_exist:
            logger.error(f'该邮箱已注册: {user_data.email}')
            raise BusinessException(code=ErrorCode.USER_EMAIL_EXIST.value, message="该邮箱已注册")
        try:
            user_data.password = encrypt_password(user_data.password)
            user_info = {
                **user_data.model_dump(),
                "user_id": generate_user_id(),
                "display_id": generate_user_id()
            }
            logger.info(f"注册用户信息: {user_info}")
            # 用户信息入库
            user = await self._repo.create(user_info)

            return RegisterResponse(data=user)
        except Exception as e:
            logger.error(f"注册用户异常: {e}")
            raise BusinessException(code=ErrorCode.SERVER_ERROR.value, message="服务器内部异常")
