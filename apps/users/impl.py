#!/usr/bin/env python
# @Project ：fastchat 
# @File    ：impl.py
# @Author  ：qiaogy
# @Email   ：qiaogy@example.com
# @Date    ：2025/7/19 09:33
from apps.users.schema import *
from apps.users.models import User
from common.utils.encrypt import Hashing
from fastapi import HTTPException, status


class Impl:
    @staticmethod
    async def create_user(req: CreateUserReq) -> CreateUserRsp:
        try:
            req.password = Hashing.hash(req.password)
            user = await User.create(**req.model_dump())
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        return user

    @staticmethod
    async def get_user(req: GetUserReq) -> GetUserRSP:
        return await User.filter(id=req.uid).first()

    @staticmethod
    async def query_user(r: QueryUserReq) -> QueryUserRsp:
        offset = (r.page - 1) * r.size
        match r.search_type:
            case '1':
                ins = await User.filter(username__icontains=r.keyword).offset(offset).limit(r.size)

            case '2':
                ins = await User.filter(mobile__icontains=r.keyword).offset(offset).limit(r.size)
            case _:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='不支持的搜索类型')
        return ins

    @staticmethod
    async def delete_user(req: DeleteUserReq) -> DeleteUserRsp:
        ins = await Impl.get_user(GetUserReq(uid=req.uid))
        if not ins:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="no such user")

        await User.filter(id=req.uid).delete()
        return ins
