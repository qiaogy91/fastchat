#!/usr/bin/env python
# @Project ：fastchat 
# @File    ：settings.py
# @Author  ：qiaogy
# @Email   ：qiaogy@example.com
# @Date    ：2025/7/16 12:10
from pydantic import Field
from pydantic_settings import BaseSettings



class DBSettings(BaseSettings):
    addr: str = Field(..., description="数据库地址")
    port: int = Field(..., description="数据库端口")
    user: str = Field(..., description="数据库用户")

    class Config:
        env_prefix = "DB_"  # 对应 .env 中的 DB_ 开头


class ServerSettings(BaseSettings):
    addr: str = Field(..., description="服务器监听地址")
    port: int = Field(..., description="服务器端口")

    class Config:
        env_prefix = "APP_"


class Settings(BaseSettings):
    db: DBSettings = DBSettings()
    server: ServerSettings = ServerSettings()

    class Config:
        env_file = ".env"  # 指定 .env 文件路径




TORTOISE_ORM = {
    "connections": {
        "default": {
            'engine': 'tortoise.backends.mysql',  # MySQL or Mariadb
            'credentials': {
                'host': os.environ.get('DB_HOST', '127.0.0.1'),
                'port': int(os.environ.get('DB_PORT', 3306)),
                'user': os.environ.get('DB_USER', 'root'),
                'password': os.environ.get('DB_PASSWORD', '123'),
                'database': os.environ.get('DB_DATABASE', 'fastchat'),
                'charset': os.environ.get('DB_CHARSET', 'utf8mb4'),
                'minsize': int(os.environ.get('DB_POOL_MINSIZE', 1)),  # 连接池中的最小连接数
                'maxsize': int(os.environ.get('DB_POOL_MAXSIZE', 5)),  # 连接池中的最大连接数
                "echo": bool(os.environ.get('DEBUG', True))  # 执行数据库操作时，是否打印SQL语句
            }
        }
    },
    'apps': {  # 默认所在的应用目录
        'models': {  # 数据模型的分组名
            'models': [],  # 模型所在目录文件的导包路径[字符串格式]
            'default_connection': 'default',  # 上一行配置中的模型列表的默认连接配置
        }
    },
    # 时区设置，为False 时表示不要使用系统时区，要使用当前指定的时区
    'use_tz': False,
    'timezone': os.environ.get('APP_TIMEZONE', 'Asia/Shanghai')
}
