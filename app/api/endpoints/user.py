#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：user_service.py
@Author  ：晴天
@Date    ：2025-04-14 14:43:06
"""
from fastapi import APIRouter, Depends
from app.schemas.response import Response
# from app.schemas.request.user import Pagination
from app.schemas.security import DecodeTokenData
from app.services.user_service import UserService
from app.api.dependencies import get_current_user, get_user_service


user_router = APIRouter(prefix='/user', tags=['User'])


@user_router.get('/get-info', summary='获取用户信息', response_model=Response, response_model_exclude_none=True)
async def get_user_info(current_user: DecodeTokenData = Depends(get_current_user),
                        user_service: UserService = Depends(get_user_service)):
    """ 获取用户信息 """
    result = await user_service.get_user_info(user_id=current_user.user_id)
    return Response(data=result)


@user_router.get('/get-user-list', summary='获取用户列表', response_model=Response, response_model_exclude_none=True)
async def get_user_list(
        page: int = 1, page_size: int = 10, sort_by: int = 0, _: DecodeTokenData = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)):
    """ 获取用户列表 """
    result = await user_service.get_user_pagination_list(page=page, page_size=page_size, sort_by=sort_by)
    return Response(data=result)
