#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：base.py
@Author  ：晴天
@Date    ：2025-04-04 19:19:37
"""
from pydantic import Field
from datetime import datetime
from app.core.logger import logger
from typing import Dict, Any, ClassVar
from app.enums.status_code import StatusCode
from beanie import Document, PydanticObjectId
from app.exceptions.custom import ServiceException


class BaseDocument(Document):
    """
    基础文档类，提供所有模型共用的字段和方法。

    该类定义了所有 MongoDB 文档模型的基础字段（如 ID、状态、时间戳等），并提供通用的序列化逻辑。
    子类可以通过继承此类的字段和方法，同时可选择是否调整字段顺序。
    """

    # 文档唯一标识符，使用 PydanticObjectId 类型，映射到 MongoDB 的 _id 字段
    id: PydanticObjectId = Field(
        default_factory=PydanticObjectId, alias="_id",  description="文档唯一标识符，自动生成的主键，对应 MongoDB 的 _id 字段")

    # 类变量：需要格式化的 datetime 字段列表，指定哪些字段需要转换为字符串格式
    datetime_fields_to_format: ClassVar[list[str]] = ["create_date", "last_modify_date"]
    # 类变量：是否强制字段排序，控制是否调整字段顺序（id 在前，子类字段次之，父类字段最后）
    enforce_field_order: ClassVar[bool] = False

    class Config:
        """Pydantic 配置类。

        定义 Pydantic 的序列化行为和类型处理规则。
        """
        json_encoders = {
            PydanticObjectId: str,  # 将 PydanticObjectId 转换为字符串，便于 JSON 序列化
        }
        arbitrary_types_allowed = True  # 允许使用任意类型（如 PydanticObjectId），避免类型检查错误

    class Settings:
        """
        Beanie 配置类。

        定义 Beanie ORM 的行为和 MongoDB 相关设置。
        """
        use_state_management = True  # 启用 Beanie 的状态管理功能，跟踪文档状态
        validate_on_save = True  # 在保存文档到 MongoDB 时自动验证数据有效性
        use_mongo_time = True  # 使用 MongoDB 的 ISODate 类型来存储 datetime 字段
        collection = "base"  # 设置默认的集合名称，子类可以覆盖此设置

    def model_serialize(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """
        自定义序列化方法，将模型数据转换为字典。

        :param include_sensitive: 是否包含敏感字段（如 password、access_token 等），默认为 False
        :return: 序列化后的数据字典
        :raises ServiceException: 如果序列化过程中发生异常，抛出服务内部异常
        """
        try:
            # 获取所有字段的原始数据，绕过 exclude=True 的限制
            data = self.__dict__.copy()

            # 如果不包含敏感字段，排除标记为 exclude=True 的字段
            if not include_sensitive:
                exclude_fields = {field for field, model_field in self.model_fields.items()
                                  if model_field.exclude}
                for field in exclude_fields:
                    data.pop(field, None)

            # 单独处理 id 字段，转换为字符串
            data["id"] = str(self.id) if self.id else None

            # 定义时间格式化函数
            def format_datetime(dt: datetime | None) -> str | None:
                return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else None

            # 格式化所有指定的 datetime 字段
            for field in self.datetime_fields_to_format:
                if field in data and data[field] is not None:
                    data[field] = format_datetime(data[field])

            return {"id": data['id'], **data}
        except Exception as e:
            logger.error(f"Serialization error: {str(e)}")
            raise ServiceException(code=StatusCode.SYSTEM_ERROR.get_code(),
                                   message=StatusCode.SYSTEM_ERROR.get_message())
