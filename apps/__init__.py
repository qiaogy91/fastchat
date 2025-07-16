#!/usr/bin/env python
# @Project ：fastchat 
# @File    ：__init__.py.py
# @Author  ：qiaogy
# @Email   ：qiaogy@example.com
# @Date    ：2025/7/16 11:31
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from conf import ORM_SETTINGS, SETTINGS
from common.middleware import request_duration
from common.exception import exception_handlers
from apps.users.api import router as user_router

'''
初始化app、以及各种模块
'''


def get_app() -> FastAPI:
    # 实例化、异常处理函数
    app: FastAPI = FastAPI(title=SETTINGS.server.name, exception_handlers=exception_handlers)

    # 注册配置到 app
    register_tortoise(
        app=app,
        config=ORM_SETTINGS,
        generate_schemas=False,  # 是否自动生成表结构
        add_exception_handlers=True,  # 是否启用自动异常处理
    )

    # 添加子路由
    app.include_router(user_router, prefix="/users", tags=["用户管理"])
    # 中间件
    middleware = app.middleware("http")
    middleware(request_duration)

    return app
