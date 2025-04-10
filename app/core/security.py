#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：security.py
@Author  ：晴天
@Date    ：2025-04-10 16:14:30
"""
from typing import Dict, Any
from app.core.logger import logger
from app.core.config import config
from datetime import datetime, timedelta
from jwt import encode, decode, PyJWTError
from app.enums.status_code import StatusCode
from app.exceptions.custom import AuthException
from app.schemas.security import DecodeTokenData, TokenData


class JWTManager:
    """ JWT管理类 """

    def __init__(self):
        """ 初始化 """
        self.secret_key = config.PROJECT_SECRET_KEY
        self.algorithm = config.PROJECT_ALGORITHM

    def create_token(self, data: Dict[str, Any]) -> TokenData:
        """
        创建token
        :param data: 数据
        :return: TokenData
        """
        copy_data = data.copy()
        access_token_expire = datetime.now() + timedelta(days=config.PROJECT_ACCESS_TOKEN_EXPIRE_DAYS)
        refresh_token_expire = datetime.now() + timedelta(days=config.PROJECT_REFRESH_TOKEN_EXPIRE_DAYS)
        copy_data.update({"exp": access_token_expire, "type": "access"})
        access_token = encode(payload=copy_data, key=self.secret_key, algorithm=self.algorithm)
        copy_data.update({"exp": refresh_token_expire, "type": "refresh"})
        refresh_token = encode(payload=copy_data, key=self.secret_key, algorithm=self.algorithm)

        return TokenData(
            access_token=access_token,
            token_type="bearer",
            refresh_token=refresh_token,
            expire=int(access_token_expire.timestamp() * 1000),
            user_id=data.get("user_id"),
            nickname=data.get("nickname")
        )

    def decode_token(self, token: str) -> DecodeTokenData:
        """
        解析token
        :param token: token
        :return: DecodeTokenData
        """
        try:
            payload = decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload is None or payload.get("user_id") is None:
                raise AuthException(code=StatusCode.TOKEN_INVALID.get_code(), message=StatusCode.TOKEN_INVALID.get_message())
            return DecodeTokenData(**payload)
        except PyJWTError as e:
            logger.error('Token decode failed: {}'.format(e))
            raise AuthException(code=StatusCode.TOKEN_INVALID.get_code(), message='Token validation failed')


jwt_manager = JWTManager()
