#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：pagination.py
@Author  ：晴天
@Date    ：2025-04-14 15:46:07
"""
from pydantic import BaseModel
from typing import Any, Dict, List



class PaginationResult(BaseModel):
    """ 分页查询结果类型 """

    list: List[Dict[str, Any]]
    total: int
    page: int
    page_size: int