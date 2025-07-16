#!/usr/bin/env python
# @Project ：fastchat 
# @File    ：api.py
# @Author  ：qiaogy
# @Email   ：qiaogy@example.com
# @Date    ：2025/7/16 18:08


from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException


router: APIRouter = APIRouter()


@router.get("/")
async def get_user(name: str)-> dict:
    try:
        print(xxxx)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=ex.__str__())
    return {"data": "get user test"}
