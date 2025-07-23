#!/usr/bin/env python
# @Project ：fastchat 
# @File    ：impl_test.py
# @Author  ：qiaogy
# @Email   ：qiaogy@example.com
# @Date    ：2025/7/19 10:50
import pytest
import pytest_asyncio
from apps.users.impl import Impl
from apps.users.schema import *
from conf import ORM_SETTINGS
from tortoise import Tortoise


# 测试函数必须以 test_ 开头
def test_add():
    result = 2 + 3
    assert result == 5, "add(2, 3) 应该等于 5"


# 异步fixture，用于测试函数执行前后的资源准备、清理
# autouse 表示这个函数是否应用给所有函数（权限）
@pytest_asyncio.fixture(autouse=True)
async def initialize_db():
    await Tortoise.init(config=ORM_SETTINGS)
    yield  # 前半部分运行前调用、后半部分运行后调用
    await Tortoise.close_connections()


# 标记函数为异步的，让pytest 去使用asyncio 去运行
@pytest.mark.asyncio
async def test_create_user():
    req = CreateUserReq(mobile="18192106881", username="user3", password='redhat.123', rpassword='redhat.123')
    obj = await Impl.create_user(req)
    print(obj)


@pytest.mark.asyncio
async def test_get_user():
    req = GetUserReq(uid=6)
    ins = await Impl.get_user(req)
    print(ins)


@pytest.mark.asyncio
async def test_query_user():
    req1 = QueryUserReq(search_type=1,keyword="user",page=1,size=3)
    req2 = QueryUserReq(search_type=2,keyword="181",page=1,size=3)
    ins = await Impl.query_user(req1)
    for user in ins:
        print(user.username)


@pytest.mark.asyncio
async def test_delete_user():
    req = DeleteUserReq(uid=6)
    ins = await Impl.delete_user(req)
    print(ins.username)