#!/usr/bin/env python
# @Project ：fastchat 
# @File    ：models.py
# @Author  ：qiaogy
# @Email   ：qiaogy@example.com
# @Date    ：2025/7/16 16:33
from tortoise import models, fields


class User(models.Model):
    id = fields.IntField(pk=True, description='主键')
    username = fields.CharField(max_length=255, unique=True, description='账号')
    password = fields.CharField(max_length=255, description='密码')
    mobile = fields.CharField(max_length=15, index=True, description='手机', unique=True)
    created_time = fields.DatetimeField(auto_now_add=True, description='创建时间')
    updated_time = fields.DatetimeField(auto_now=True, description="更新时间")
    deleted_time = fields.DatetimeField(null=True, description="删除时间")

