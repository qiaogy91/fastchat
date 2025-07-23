#!/usr/bin/env python
# @Project ：fastchat 
# @File    ：schema.py
# @Author  ：qiaogy
# @Email   ：qiaogy@example.com
# @Date    ：2025/7/16 18:08
from fastapi import UploadFile, Form, File
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from pydantic import BaseModel, Field, model_validator, ConfigDict
from pydantic_core import PydanticCustomError
from apps.users.models import User
from typing import Literal


class CreateUserReq(BaseModel):
    mobile: str = Field(pattern='^1[3-9]\d{9}', description='手机号')
    username: str = Field(max_length=30, description='用户名')
    password: str = Field(min_length=6, max_length=16, description='密码')
    rpassword: str = Field(min_length=6, max_length=16, description='密码')

    model_config = ConfigDict(extra="ignore")  # 当传入的字典中有 模型未定义的额外字段 时的处理方式，ignore 表示忽略

    @model_validator(mode="after")  # 在所有字段完成基础的校验后执行
    def check_password(self):
        # 两次输入的密码校验
        if self.password != self.rpassword:
            raise PydanticCustomError(
                'password_mismatch',  # 自定义错误类型
                '两次密码不一致'  # 错误提示
            )
        return self  # 返回修改后结果


class GetUserReq(BaseModel):
    uid: int = Field(..., description="用户ID")


class QueryUserReq(BaseModel):
    search_type: Literal['1', '2'] = Field(description="查询类型,1=用户名，2=手机号", default='1')
    keyword: str = Field(description="关键字", default="")
    page: int = Field(description="第几页", default=1)
    size: int = Field(description="页大小", default=20)


class DeleteUserReq(BaseModel):
    uid: int = Field(..., description="用户ID")


class LoginReq(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")

class LoginRsp(BaseModel):
    username: str = Field(..., description="用户名")
    token: str = Field(..., description="jwt token")



class UploadFileReq(BaseModel):
    username: str
    file: UploadFile

    @classmethod
    def as_form(cls, username:str=Form(...), file:UploadFile=File(...)):
        return cls(username=username, file=file)

class UploadFileRsp(BaseModel):
    username: str
    filename: str


CreateUserRsp = pydantic_model_creator(User, name="CreateUserRsp", exclude=("password",))
GetUserRSP = pydantic_model_creator(User, name="GetUserRSP", exclude=("password",))
QueryUserRsp = pydantic_queryset_creator(User, name="QueryUserRsp", exclude=("password",))
DeleteUserRsp = pydantic_model_creator(User, name="DeleteUserRsp", exclude=("password",))
