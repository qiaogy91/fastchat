#!/usr/bin/env python
# @Project ：fastchat 
# @File    ：settings.py
# @Author  ：qiaogy
# @Email   ：qiaogy@example.com
# @Date    ：2025/7/16 12:10
import os
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


ENV_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "etc", ".env")


class DBSettings(BaseSettings):
    addr: str = Field(..., description="数据库地址")
    port: int = Field(..., description="数据库端口")
    username: str = Field(..., description="数据库用户")
    password: str = Field(..., description="数据库密码")
    database: str = Field(..., description="数据库名称")
    chatset: str = Field(..., description="字符集")
    pool_minsize: int = Field(..., description="连接池中最小链接的数量")
    pool_maxsize: int = Field(..., description="连接池中最大链接的数量")
    echo: bool = Field(..., description="执行数据库操作时，是否打印SQL语句")


class ServerSettings(BaseSettings):
    env: str = Field(..., description="当前开发环境")
    name: str = Field(..., description="当前系统名称")
    addr: str = Field(..., description="服务器监听地址")
    port: int = Field(..., description="服务器端口")
    debug: bool = Field(..., description="是否开启调试")
    timezone: str = Field(..., description="时区")
    version: str = Field(..., description="当前系统版本")


class LoggerSettings(BaseSettings):
    level: int = Field(..., description="日志级别")
    root: str = Field(..., description="日志目录")


class SmsSettings(BaseSettings):
    max_length: int = Field(..., description="验证码最大长度")


class RedisSettings(BaseSettings):
    addr: str = Field(..., description="redis 地址")
    port: int = Field(..., description="redis 端口")
    db: int = Field(..., description="redis 数据库")
    username: str = Field(..., description="redis 用户")
    password: str = Field(..., description="redis 密码")


class JwtSettings(BaseSettings):
    key: str = Field(..., description="秘钥")
    algorithm: str = Field(..., description="算法")
    expire: int =Field(..., description="过期时间")
    white_list: str = Field(..., description="白名单地址无需认证")


class Settings(BaseSettings):
    db: DBSettings
    server: ServerSettings
    logger: LoggerSettings
    sms: SmsSettings
    redis: RedisSettings
    jwt: JwtSettings

    # env_file Working Directory 目录，也就是运行 python main.py 时所在的目录
    model_config = SettingsConfigDict(env_file_encoding="utf-8", env_nested_delimiter="__", env_file=ENV_FILE)



@lru_cache()
def get_settings() -> Settings:
    """
    :return:  lru_cache 能让函数的返回值自动缓存，从而避免重复计算。是官方推荐的单例构建装饰器
    """
    return Settings()


@lru_cache()
def get_orm_settings() -> dict:
    settings = get_settings()
    return {
        "connections": {
            # 每个KV 代表一个数据库实例的链接方式
            "default": {
                'engine': 'tortoise.backends.mysql',  # MySQL or Mariadb
                'credentials': {
                    'host': settings.db.addr,
                    'port': settings.db.port,
                    'user': settings.db.username,
                    'password': settings.db.password,
                    'database': settings.db.database,
                    'charset': settings.db.chatset,
                    'minsize': settings.db.pool_minsize,
                    'maxsize': settings.db.pool_maxsize,
                    "echo": settings.db.echo,
                }
            }
        },
        # 所有的模型目录
        'apps': {
            'models': {
                'models': ['apps.users.models', 'aerich.models'],  # 模型结构所在的文件路径，从main.py 同级目录开始
                'default_connection': 'default',  # 上一行配置中的模型列表的默认连接配置
            }
        },
        # 时区设置，为False 时表示不要使用系统时区，要使用当前指定的时区
        'use_tz': False,
        'timezone': settings.server.timezone
    }
