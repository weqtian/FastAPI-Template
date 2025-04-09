#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：user_model.py
@Author  ：晴天
@Date    ：2025-04-04 17:46:42
"""
from app.core.logger import logger
from app.enums.status_code import StatusCode
from app.schemas.response.user import UserInfo
from app.schemas.request.auth import RegisterUser
from app.exceptions.custom import BusinessException
from app.utils.user_id_util import generate_user_id
from app.repositories.user_repo import UserRepository
from app.schemas.response.auth import RegisterResponse
from app.utils.encrypt_util import encrypt_password


class UserService:
    """ 用户服务 """

    def __init__(self, repo: UserRepository):
        self._repo = repo

    async def register(self, user_data: RegisterUser, request_info: dict = None) -> RegisterResponse:
        """
        注册用户
        :param user_data: 用户数据
         :param request_info: 请求信息
        :return: 用户信息
        """
        email_is_exist = await self._repo.get_user_by_email(user_data.email)
        if email_is_exist:
            logger.error(f'该邮箱已注册: {user_data.email}')
            raise BusinessException(
                code=StatusCode.EMAIL_ALREADY_REGISTERED.get_code(),
                message=StatusCode.EMAIL_ALREADY_REGISTERED.get_message()
            )
        try:
            user_data.password = encrypt_password(user_data.password)
            user_info = {
                **user_data.model_dump(),
                "user_id": generate_user_id(),
                "display_id": generate_user_id(),
                "create_ip": request_info.get("client_ip", None),
            }
            user = await self._repo.create(user_info)
            return RegisterResponse(data=UserInfo(**user))
        except Exception as e:
            logger.error(f"注册用户异常: {e}")
            raise BusinessException(
                code=StatusCode.SYSTEM_ERROR.get_code(),
                message=StatusCode.SYSTEM_ERROR.get_message()
            )
