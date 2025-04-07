#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：validation_util.py
@Author  ：晴天
@Date    ：2025-04-07 14:57:36
"""
import re
import datetime
from typing import Optional


class ValidationUtil:
    """数据验证工具类"""

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        验证邮箱地址是否合法
        Args:
            email: 需要验证的邮箱地址
        Returns:
            bool: 是否为合法邮箱地址
        """
        if not isinstance(email, str):
            return False

        # 邮箱正则表达式
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email.strip()))

    @staticmethod
    def check_string_length(text: str, min_length: int = 0, max_length: Optional[int] = None) -> bool:
        """
        验证字符串长度是否在指定范围内
        Args:
            text: 需要验证的字符串
            min_length: 最小长度（包含）
            max_length: 最大长度（包含），可选
        Returns:
            bool: 长度是否符合要求
        """
        if not isinstance(text, str):
            return False

        length = len(text.strip())
        if length < min_length:
            return False
        if max_length is not None and length > max_length:
            return False
        return True

    @staticmethod
    def is_valid_gender(gender: int) -> bool:
        """
        验证性别是否合法（支持中文和英文）
        Args:
            gender: 需要验证的性别
        Returns:
            bool: 是否为合法性别值
        """
        if not gender and isinstance(gender, int):
            return False
        valid_genders = [1, 2]
        return gender in valid_genders

    @staticmethod
    def is_valid_date(date_str: str, date_format: str = "%Y-%m-%d") -> bool:
        """
        验证日期字符串是否合法
        Args:
            date_str: 需要验证的日期字符串
            date_format: 日期格式，默认为 "%Y-%m-%d" (如 2025-04-07)
        Returns:
            bool: 是否为合法日期
        """
        if not isinstance(date_str, str):
            return False

        date_str = date_str.strip()

        # 先用正则表达式初步验证格式
        date_pattern = r'^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$'
        if not re.match(date_pattern, date_str):
            return False

        try:
            # 尝试将字符串转换为日期对象，验证是否是真实存在的日期
            datetime.datetime.strptime(date_str, date_format)
            return True
        except ValueError:
            # 处理非法日期，如 2023-02-30
            return False




data_validation = ValidationUtil()


# 使用示例
if __name__ == "__main__":
    # print(data_validation.is_valid_email("test@example.com"))  # True
    # print(data_validation.is_valid_email("invalid_email"))  # False
    # print(data_validation.check_string_length("test", min_length=3, max_length=5))  # True
    # print(data_validation.check_string_length("test", min_length=3, max_length=2))  # False
    # print(data_validation.is_valid_gender(1))  # True
    # print(data_validation.is_valid_gender(3))  # False
    # print(data_validation.is_valid_date("2024-02-29"))  # True (2024是闰年)
    # print(data_validation.is_valid_date("2023-13-01"))  # False (月份非法)
    pass