#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：user.py
@Author  ：晴天
@Date    ：2025-04-14 17:09:27
"""
from typing import Optional, List, Any, Dict
from app.enums.status_code import StatusCode
from pydantic import BaseModel, field_validator
from app.exceptions.custom import ValidationException


class Pagination(BaseModel):
    """ 分页信息 """

    page: int = 1
    page_size: int = 10
    sort_by: Optional[int] = 0

    @field_validator("page")
    def validate_page(cls, v: int):
        """
        验证页码
        :param v: 页码
        :return: 页码
        """
        if v < 1:
            return 1
        return v

    @field_validator("page_size")
    def validate_page_size(cls, v: int):
        """
        验证每页数量
        :param v: 每页数量
        :return: 每页数量
        """
        if 1 < v > 100:
            raise ValidationException(code=StatusCode.PAGE_SIZE_ERROR.get_code(),
                                      message=StatusCode.PAGE_SIZE_ERROR.get_message())
        return v

    @field_validator("sort_by")
    def validate_sort_by(cls, v: List[str]):
        """
        验证排序方式
        :param v: 排序方式
        :return: 排序方式
        """
        if v not in [0, 1]:
            raise ValidationException(code=422, message="排序方式错误：0或1")
        return v
