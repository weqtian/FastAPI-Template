#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：FAstAPI-Template 
@File    ：main.py
@Author  ：晴天
@Date    ：2025-04-03 18:42:10
"""
import uvicorn
from app.core.config import config
from app.app_factory import create_app


app = create_app()


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host=config.PROJECT_HOST,
        port=config.PROJECT_PORT,
        reload=config.PROJECT_RELOAD,
        use_colors=True
    )
