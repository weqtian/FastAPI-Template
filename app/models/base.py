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
from beanie import Document, PydanticObjectId
from app.exceptions.custom import ServiceException


class BaseDocument(Document):
    """基础文档类，提供所有模型共用的字段和方法。

    该类定义了所有 MongoDB 文档模型的基础字段（如 ID、状态、时间戳等），并提供通用的序列化逻辑。
    子类可以通过继承此类的字段和方法，同时可选择是否调整字段顺序。
    """

    # 文档唯一标识符，使用 PydanticObjectId 类型，映射到 MongoDB 的 _id 字段
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id",  description="文档唯一标识符，自动生成的主键，对应 MongoDB 的 _id 字段")

    # 记录激活状态，True 表示记录有效，False 表示记录被禁用
    is_active: bool = Field(default=True, description="记录是否激活，True 表示激活（有效），False 表示禁用")

    # 逻辑删除标志，True 表示记录已被删除（软删除），False 表示未删除
    is_deleted: bool = Field(default=False, description="记录是否逻辑删除，True 表示已删除（软删除），False 表示未删除")

    # 创建时间戳，以毫秒为单位，用于记录创建的精确时间
    create_time: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000), description="记录创建时间戳（毫秒），表示记录创建的精确时间")

    # 创建日期时间，使用 ISODate 格式，便于人类阅读和查询
    create_date: datetime = Field(default_factory=datetime.now, description="记录创建日期时间，ISODate 格式，便于人类阅读和查询")

    # 创建者标识，记录是谁创建了这条记录，默认值为 "system"
    create_by: str = Field(default="system", description="记录创建者标识，表示创建此记录的用户或系统，默认值为 'system'")

    # 最后修改者标识，记录最后修改此记录的用户或系统
    last_modify_by: str = Field(default="system", description="最后修改者标识，表示最后修改此记录的用户或系统，默认值为 'system'")

    # 最后修改时间戳，以毫秒为单位，记录最后一次修改的精确时间
    last_modify_time: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000), description="最后修改时间戳（毫秒），表示记录最后一次修改的精确时间")

    # 最后修改日期时间，使用 ISODate 格式，记录最后修改的时间
    last_modify_date: datetime = Field(default_factory=datetime.now, description="最后修改日期时间，ISODate 格式，表示记录最后修改的时间")

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

    def model_serialize(self) -> Dict[str, Any]:
        """
        自定义序列化方法，将模型数据转换为字典。

        该方法支持两种序列化行为：
        1. 默认行为（enforce_field_order=False）：保持字段定义顺序。
        2. 排序行为（enforce_field_order=True）：id 在首位，子类专有字段次之，BaseDocument 其他字段最后。
        同时处理 datetime 字段格式化、id 转换为字符串，并包含异常处理。

        :return: 序列化后的数据字典
        :raises ServiceException: 如果序列化过程中发生异常，抛出服务内部异常
        """
        try:
            # 获取基础序列化数据，排除 id 字段（稍后单独处理）
            data = self.model_dump(exclude={"id"})
            data["id"] = str(self.id) if self.id else None  # 将 PydanticObjectId 转换为字符串

            # 定义时间格式化函数，将 datetime 对象转换为指定格式的字符串
            def format_datetime(dt: datetime | None) -> str | None:
                return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else None

            # 格式化所有指定的 datetime 字段
            for field in self.datetime_fields_to_format:
                if field in data and data[field] is not None:
                    data[field] = format_datetime(data[field])

            # 如果子类启用了字段排序
            if self.enforce_field_order:
                # 获取 BaseDocument 的字段名
                base_fields = set(BaseDocument.model_fields.keys())
                # 获取当前类的所有字段名（包括继承的和专有的）
                all_fields = set(self.model_fields.keys())
                # 计算子类的专有字段
                child_fields = all_fields - base_fields
                # BaseDocument 的字段中排除 id
                base_fields_excluding_id = base_fields - {"id"}

                # 分离字段
                id_data = {"id": data.get("id")}  # id 单独提取，确保在首位
                child_data = {k: v for k, v in data.items() if k in child_fields}  # 子类专有字段
                base_data_excluding_id = {k: v for k, v in data.items() if k in base_fields_excluding_id}  # BaseDocument 其他字段

                # 合并字段，确保 id 在首位，子类字段次之，BaseDocument 其他字段最后
                return {**id_data, **child_data, **base_data_excluding_id}

            # 默认行为：不调整字段顺序，直接返回序列化数据
            return data

        except Exception as e:
            # 记录序列化错误日志并抛出自定义异常
            logger.error(f"Serialization error: {str(e)}")
            raise ServiceException(code=500, message="服务内部异常")

    class Settings:
        """Beanie 配置类。

        定义 Beanie ORM 的行为和 MongoDB 相关设置。
        """
        use_state_management = True  # 启用 Beanie 的状态管理功能，跟踪文档状态
        validate_on_save = True  # 在保存文档到 MongoDB 时自动验证数据有效性
        use_mongo_time = True  # 使用 MongoDB 的 ISODate 类型来存储 datetime 字段
        collection = "base"  # 设置默认的集合名称，子类可以覆盖此设置