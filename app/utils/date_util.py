#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：date_util.py
@Author  ：晴天
@Date    ：2025-04-10 18:15:39
"""
from typing import Optional
from datetime import datetime, timezone, timedelta


class DateUtil:
    """
    日期时间工具类
    """

    # 常用格式模板
    DEFAULT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    DEFAULT_DATE_FORMAT = "%Y-%m-%d"
    DEFAULT_TIME_FORMAT = "%H:%M:%S"
    ISO_FORMAT = "%Y-%m-%dT%H:%M:%S%z"

    @staticmethod
    def now(tz: Optional[timezone] = None) -> datetime:
        """
        获取当前时间，可指定时区
        :param tz: 时区对象
        :return: 当前时间
        """
        return datetime.now(tz)

    @staticmethod
    def utc_now() -> datetime:
        """
        获取当前UTC时间
        :return: 当前UTC时间
        """
        return datetime.now(timezone.utc)

    @staticmethod
    def format_datetime(dt: datetime, format_str: str = DEFAULT_DATETIME_FORMAT) -> str:
        """
        格式化日期时间
        :param dt: 日期时间对象
        :param format_str: 格式化字符串 默认: "%Y-%m-%d %H:%M:%S"
        :return: 格式化后的日期时间字符串
        """
        return dt.strftime(format_str)

    @staticmethod
    def parse_datetime(date_str: str, format_str: str = DEFAULT_DATETIME_FORMAT) -> datetime:
        """
        解析日期时间字符串
        :param date_str: 日期时间字符串
        :param format_str: 格式化字符串 默认: "%Y-%m-%d %H:%M:%S"
        :return: 日期时间对象
        """
        return datetime.strptime(date_str, format_str)

    @staticmethod
    def to_iso_format(dt: datetime) -> str:
        """
        转换为ISO格式
        :param dt: 日期时间对象
        :return: ISO格式字符串
        """
        return dt.strftime(DateUtil.ISO_FORMAT)

    @staticmethod
    def get_time_diff(start: datetime, end: datetime, unit: str = "seconds") -> float:
        """
        计算时间差，可选单位：seconds, minutes, hours, days
        :param start: 开始时间
        :param end: 结束时间
        :param unit: 时间单位 默认: seconds
        :return: 时间差 (单位：秒)
        """
        diff = end - start
        if unit == "minutes":
            return diff.total_seconds() / 60
        elif unit == "hours":
            return diff.total_seconds() / 3600
        elif unit == "days":
            return diff.total_seconds() / 86400
        return diff.total_seconds()

    @staticmethod
    def add_time(dt: datetime, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0) -> datetime:
        """
        增加时间
        :param dt: 日期时间对象
        :param days: 天数
        :param hours: 小时数
        :param minutes: 分钟数
        :param seconds: 秒数
        :return: 增加后的日期时间对象
        """
        return dt + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

    @staticmethod
    def subtract_time(dt: datetime, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0) -> datetime:
        """
        减少时间
        :param dt: 日期时间对象
        :param days: 天数
        :param hours: 小时数
        :param minutes: 分钟数
        :param seconds: 秒数
        :return: 减少后的日期时间对象
        """
        return dt - timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

    @staticmethod
    def is_weekend(dt: datetime) -> bool:
        """
        判断是否为周末
        :param dt: 日期时间对象
        :return: 是否为周末
        """
        return dt.weekday() >= 5

    @staticmethod
    def get_now_timestamp() -> int:
        """
        获取当前时间戳
        :return: 当前时间戳
        """
        return int(datetime.now().timestamp() * 1000)

    @staticmethod
    def get_start_of_day(dt: datetime) -> datetime:
        """
        获取当天开始时间
        :param dt: 日期时间对象
        :return: 当天开始时间
        """
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def get_end_of_day(dt: datetime) -> datetime:
        """
        获取当天结束时间
        :param dt: 日期时间对象
        :return: 当天结束时间
        """
        return dt.replace(hour=23, minute=59, second=59, microsecond=999999)

    @staticmethod
    def get_start_of_month(dt: datetime) -> datetime:
        """
        获取当月开始时间
        :param dt: 日期时间对象
        :return: 当月开始时间
        """
        return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def get_end_of_month(dt: datetime) -> datetime:
        """
        获取当月结束时间
        :param dt: 日期时间对象
        :return: 当月结束时间
        """
        next_month = dt.replace(day=28) + timedelta(days=4)
        return next_month - timedelta(days=next_month.day)

    @staticmethod
    def get_start_of_year(dt: datetime) -> datetime:
        """
        获取当年开始时间
        :param dt: 日期时间对象
        :return: 当年开始时间
        """
        return dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def get_end_of_year(dt: datetime) -> datetime:
        """
        获取当年结束时间
        :param dt: 日期时间对象
        :return: 当年结束时间
        """
        return dt.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)


date_util = DateUtil()


if __name__ == '__main__':
    pass
    # current = DateUtil.now()
    # print(f"当前时间: {DateUtil.format_datetime(current)}")
    #
    # utc_time = DateUtil.utc_now()
    # print(f"UTC时间: {DateUtil.format_datetime(utc_time)}")
    #
    # print(f"仅日期: {DateUtil.format_datetime(current, DateUtil.DEFAULT_DATE_FORMAT)}")
    #
    # future = DateUtil.add_time(current, days=1, hours=2)
    # print(f"一天两小时后: {DateUtil.format_datetime(future)}")
    #
    # diff = DateUtil.get_time_diff(current, future, "hours")
    # print(f"时间差(小时): {diff:.2f}")
    #
    # print(f"是周末吗: {DateUtil.is_weekend(current)}")
    #
    # start = DateUtil.get_start_of_day(current)
    # end = DateUtil.get_end_of_day(current)
    # print(f"当天开始: {DateUtil.format_datetime(start)}")
    # print(f"当天结束: {DateUtil.format_datetime(end)}")
    # print(f'当月开始时间: {DateUtil.get_start_of_month(current)}')
    # print(f'当月结束时间: {DateUtil.get_end_of_month(current)}')
    # print(f'当年开始时间: {DateUtil.get_start_of_year(current)}')
    # print(f'当年结束时间: {DateUtil.get_end_of_year(current)}')
    # print(f'当前时间戳: {DateUtil.get_now_timestamp()}')
