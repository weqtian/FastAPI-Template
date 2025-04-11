#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：user_model.py
@Author  ：晴天
@Date    ：2025-04-04 17:46:42
"""
from app.core.logger import logger
from typing import Dict, Any, Callable
from app.utils.date_util import date_util
from app.core.security import jwt_manager
from app.enums.status_code import StatusCode
from app.schemas.security import DecodeTokenData
from app.exceptions.custom import BusinessException
from app.repositories.user_repo import UserRepository
from app.utils.encrypt_util import encrypt_password, verify_password
from app.utils.user_id_util import generate_user_id, generate_display_id
from app.schemas.request.auth import RegisterUser, LoginUser


class AuthService:
    """ 用户服务 """

    def __init__(self, repo: UserRepository):
        self._repo = repo

    @staticmethod
    async def _generate_unique_id(generate_func: Callable[[], str], check_func: Callable[[str], Any],
                                  id_name: str, max_attempts: int = 5) -> str:
        """
        生成唯一的 ID
        :param generate_func: 生成 ID 的函数
        :param check_func: 检查 ID 是否存在的函数
        :param id_name: ID 的名称（用于日志和错误信息）
        :param max_attempts: 最大重试次数
        :return: 唯一的 ID
        """
        for _ in range(max_attempts):
            new_id = generate_func()
            if not await check_func(new_id):
                return new_id
            logger.info(f'{id_name}:{new_id} 已存在，重新生成')
        logger.error(f'无法生成唯一的 {id_name}')
        raise BusinessException(
            code=StatusCode.SYSTEM_ERROR.get_code(),
            message=StatusCode.SYSTEM_ERROR.get_message()
        )

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
        user_data.password = encrypt_password(user_data.password)
        user_id = await self._generate_unique_id(
            generate_func=generate_user_id,
            check_func=self._repo.get_user_by_id,
            id_name='user_id',
        )
        display_id = await self._generate_unique_id(
            generate_func=generate_display_id,
            check_func=self._repo.get_user_by_id,
            id_name='display_id',
        )
        user_info = {
            **user_data.model_dump(),
            "user_id": user_id,
            "display_id": display_id,
            "create_ip": request_info.get("client_ip", None),
            'create_by': user_id,
        }
        try:
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

    async def logout(self, current_user: DecodeTokenData):
        """
        退出登录
        :param current_user: 当前用户
        :return: 用户信息
        """
        try:
            await self._repo.update_user_by_id(current_user.user_id, {
                'last_modify_by': current_user.user_id, 'last_modify_time': date_util.get_now_timestamp(),
                'last_modify_date': date_util.now(), 'access_token': None, 'refresh_token': None
            })
            return True
        except Exception as e:
            logger.error(f"退出登录异常: {e}")
            raise BusinessException(code=StatusCode.SYSTEM_ERROR.get_code(),
                                    message=StatusCode.SYSTEM_ERROR.get_message())
