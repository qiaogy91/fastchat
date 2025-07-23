#!/usr/bin/env python
# @Project ：fastchat 
# @File    ：__init__.py.py
# @Author  ：qiaogy
# @Email   ：qiaogy@example.com
# @Date    ：2025/7/16 11:31
from fastapi import FastAPI
from conf import SETTINGS
from common.middleware import RequestDuration, Authentication
from common.exception import exception_handlers
from apps.users.api import router as user_router
from common.lifespan import liefspan

'''
初始化app、以及各种模块
'''


def get_app() -> FastAPI:
    # 实例化、异常处理函数
    app: FastAPI = FastAPI(title=SETTINGS.server.name, exception_handlers=exception_handlers, lifespan=liefspan)


    app.add_middleware(RequestDuration) # type: ignore
    app.add_middleware(Authentication) # type: ignore

    # 添加子路由
    app.include_router(user_router, prefix="/users", tags=["用户管理"])

    return app
