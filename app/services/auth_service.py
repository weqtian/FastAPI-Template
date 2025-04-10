#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：user_model.py
@Author  ：晴天
@Date    ：2025-04-04 17:46:42
"""
from typing import Dict, Any
from datetime import datetime
from app.core.logger import logger
from app.utils.date_util import date_util
from app.core.security import jwt_manager
from app.enums.status_code import StatusCode
from app.exceptions.custom import BusinessException
from app.utils.user_id_util import generate_user_id
from app.repositories.user_repo import UserRepository
from app.utils.encrypt_util import encrypt_password, verify_password
from app.schemas.request.auth import RegisterUser, LoginUser


class AuthService:
    """ 用户服务 """

    def __init__(self, repo: UserRepository):
        self._repo = repo

    async def register(self, user_data: RegisterUser, request_info: dict = None) -> Dict[str, Any]:
        """
        注册用户
        :param user_data: 用户数据
         :param request_info: 请求信息
        :return: 用户信息
        """
        email_is_exist = await self._repo.get_user_by_email(user_data.email)
        if email_is_exist:
            logger.error(f'该邮箱已注册: {user_data.email}')
            raise BusinessException(code=StatusCode.EMAIL_ALREADY_REGISTERED.get_code(),
                                    message=StatusCode.EMAIL_ALREADY_REGISTERED.get_message())
        try:
            user_data.password = encrypt_password(user_data.password)
            user_id = generate_user_id()
            display_id = generate_user_id()
            user_info = {
                **user_data.model_dump(),
                "user_id": user_id,
                "display_id": display_id,
                "create_ip": request_info.get("client_ip", None),
                'create_by': user_id,
            }
            user = await self._repo.create(user_info)
            return user
        except Exception as e:
            logger.error(f"注册用户异常: {e}")
            raise BusinessException(code=StatusCode.SYSTEM_ERROR.get_code(),
                                    message=StatusCode.SYSTEM_ERROR.get_message())

    async def login(self, user_data: LoginUser) -> Dict[str, Any]:
        """
        登录
        :param user_data: 用户数据
        :return: 用户信息
        """
        user = await self._repo.get_user_by_email(user_data.email, True)
        if not user:
            logger.error(f'该邮箱未注册: {user_data.email}')
            raise BusinessException(code=StatusCode.EMAIL_NOT_REGISTERED.get_code(),
                                    message=StatusCode.EMAIL_NOT_REGISTERED.get_message())
        password_verify = verify_password(user_data.password, user.get('password', None))
        if not password_verify:
            logger.error(f'账号密码错误: {user_data.email}')
            raise BusinessException(code=StatusCode.USERNAME_OR_PASSWORD_ERROR.get_code(),
                                    message=StatusCode.USERNAME_OR_PASSWORD_ERROR.get_message())
        try:
            payload = {'user_id': user.get('user_id'), 'nickname': user.get('nickname')}
            token = jwt_manager.create_token(payload)
            await self._repo.update_user_by_id(user.get('user_id'), {
                'last_modify_by': user.get('user_id'), 'last_modify_time': date_util.get_now_timestamp(),
                'last_modify_date': date_util.now(), 'access_token': token.access_token, 'refresh_token': token.refresh_token
            })
            return token.model_dump()
        except Exception as e:
            logger.error(f"登录用户异常: {e}")
            raise BusinessException(code=StatusCode.SYSTEM_ERROR.get_code(),
                                    message=StatusCode.SYSTEM_ERROR.get_message())
