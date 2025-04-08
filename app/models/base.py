#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：base.py
@Author  ：晴天
@Date    ：2025-04-04 19:19:37
"""
from datetime import datetime
from typing import Dict, Any, ClassVar
from pydantic import Field, model_serializer
from beanie import Document, PydanticObjectId


class BaseDocument(Document):
    """基础文档类，提供所有模型共用的字段和方法"""

    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id", description="文档唯一标识符")
    is_active: bool = Field(default=True, description="记录是否激活，True 表示激活，False 表示禁用")
    is_deleted: bool = Field(default=False, description="记录是否逻辑删除，True 表示已删除，False 表示未删除")
    create_time: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000), description="记录创建时间戳（毫秒）")
    create_date: datetime = Field(default_factory=datetime.now, description="记录创建日期时间，ISODate 类型")
    create_by: str = Field(default="system", description="记录创建者标识")
    last_modify_by: str = Field(default="system", description="最后修改者标识")
    last_modify_time: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000), description="最后修改时间戳（毫秒）")
    last_modify_date: datetime = Field(default_factory=datetime.now, description="最后修改日期时间，ISODate 类型")

    # 使用 ClassVar 注解，明确这是一个类变量而非字段
    datetime_fields_to_format: ClassVar[list[str]] = ["create_date", "last_modify_date"]

    class Config:
        """Pydantic 配置"""
        json_encoders = {PydanticObjectId: str}  # 将 PydanticObjectId 转换为字符串
        arbitrary_types_allowed = True  # 允许任意类型

    @model_serializer
    def serialize_model(self) -> Dict[str, Any]:
        """
        自定义序列化方法，格式化 datetime 字段并处理脱敏
        :return: 序列化后的数据字典
        """
        # 获取基础数据，排除原始 以及 使用 mode='json' 避免递归调用 serialize_model
        data = self.model_dump(mode="json", exclude={"id"})
        data["id"] = str(self.id) if self.id else None

        # 定义时间格式化函数
        def format_datetime(dt: datetime | None) -> str | None:
            return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else None

        # 格式化所有指定的 datetime 字段
        for field in self.datetime_fields_to_format:
            if field in data and data[field] is not None:
                data[field] = format_datetime(data[field])

        return data

    class Settings:
        """Beanie 配置"""
        use_state_management = True  # 启用状态管理
        validate_on_save = True  # 保存时自动验证
