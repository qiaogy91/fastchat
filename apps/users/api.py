#!/usr/bin/env python
# @Project ：fastchat 
# @File    ：api.py
# @Author  ：qiaogy
# @Email   ：qiaogy@example.com
# @Date    ：2025/7/16 18:08
import time

from fastapi import APIRouter, status, Depends
from fastapi import Response as fastPonse

from apps.users.schema import *
from apps.users.impl import Impl
from fastapi.exceptions import HTTPException
from common.response import Response, ResponseBuilder
from common.utils.auth import JWT

from common.utils.encrypt import Hashing

router: APIRouter = APIRouter()


@router.post('/register', response_model=Response[CreateUserRsp])
async def create(req: CreateUserReq):
    # 1. 判断手机号是否已经注册
    users = await Impl.query_user(QueryUserReq(search_type=2, keyword=req.mobile))
    if users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户手机重复")

    # 添加用户数据
    ins = await Impl.create_user(req)
    return ResponseBuilder.ok(ins)


@router.post('/login', response_model=Response[LoginRsp])
async def login(req: LoginReq, response: fastPonse):
    user = await Impl.query_user(QueryUserReq(search_type="1", keyword=req.username))
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="没有该用户")

    try:
        verify = Hashing.verify(req.password, user[0].password)
        if verify:
            # 增加header
            token = JWT.create_token({"username": user[0].username})
            response.set_cookie("token", token)

            rsp = LoginRsp(username=user[0].username, token=token)
            return ResponseBuilder.ok(rsp)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='账号或密码错误')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.__str__())


# # Depends() 会自动把 URL 查询参数（比如 /users/?search_type=2&keyword=foo&page=1&size=10）映射到 UserQueryReq 实例。
@router.get("/", response_model=Response[QueryUserRsp])
async def query(req: QueryUserReq = Depends()):
    ins = await Impl.query_user(req)
    return ResponseBuilder.ok_list(ins)


@router.get("/{uid}", response_model=Response[GetUserRSP])
async def get(req: GetUserReq = Depends()):
    ins = await Impl.get_user(req)
    return ResponseBuilder.ok(ins)



@router.post("/upload", response_model=Response[UploadFileRsp])
async def upload(req: UploadFileReq=Depends(UploadFileReq.as_form)):
    rsp = UploadFileRsp(username=req.username, filename=req.file.filename)
    return ResponseBuilder.ok(rsp)