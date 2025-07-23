#!/usr/bin/env python
# @Project ：fastchat 
# @File    ：lifespan.py
# @Author  ：qiaogy
# @Email   ：qiaogy@example.com
# @Date    ：2025/7/21 20:23 

from contextlib import asynccontextmanager
from fastapi import FastAPI
from conf import ORM_SETTINGS, REDIS_SETTINGS
from common.logs import get_logger
from tortoise import Tortoise, connections
from tortoise.contrib.fastapi import tortoise_exception_handlers
from redis import asyncio as aioredis
import logging

logger = get_logger("liefspan")


async def init_mysql(app: FastAPI):
    # Tortoise 默认使用名为 tortoise.db_client 的logger 来输出日志，且输出的日志级别的 DEBUG
    # 因此只要在 Tortoise 初始化之前实例化一个logger 并设置级别为 DEBUG 就可实现打印SQL
    # 而此处 get_logger() 获取到的是有两个 handler 的logger（文件、控制台），因此需要一并设置级别
    sql_logger = get_logger("tortoise.db_client")
    sql_logger.setLevel(logging.DEBUG)
    for handler in sql_logger.handlers:
        handler.setLevel(logging.DEBUG)

    # 初始化ORM
    await Tortoise.init(ORM_SETTINGS)

    # 注册异常处理器
    for exp_type, endpoint in tortoise_exception_handlers().items():
        app.exception_handler(exp_type)(endpoint)

    logger.info("mysql 已链接")


async def close_mysql(app: FastAPI):
    await connections.close_all()
    logger.info("mysql 已关闭")


async def init_redis(app: FastAPI):
    redis = await aioredis.from_url(
        f"redis://{REDIS_SETTINGS.username}:{REDIS_SETTINGS.password}@{REDIS_SETTINGS.addr}:{REDIS_SETTINGS.port}/"
        f"{REDIS_SETTINGS.db}",
        decode_responses=True)

    if await redis.ping():  # ping 结果为布尔值
        app.state.redis = redis
        logger.info("redis 已链接")


async def close_redis(app: FastAPI):
    await app.state.redis.close()  # 关闭连接
    logger.info("Redis 已关闭")


@asynccontextmanager
async def liefspan(app: FastAPI):
    await init_mysql(app)
    await init_redis(app)

    yield
    await close_mysql(app)
    await close_redis(app)
