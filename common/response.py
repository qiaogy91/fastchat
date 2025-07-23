#!/usr/bin/env python
# @Project ：fastchat 
# @File    ：response.py
# @Author  ：qiaogy
# @Email   ：qiaogy@example.com
# @Date    ：2025/7/19 23:13
from typing import Generic, TypeVar, List, Optional, Any
from pydantic import BaseModel


T = TypeVar("T")  # 泛型参数，用于 data 字段类型推导


class Response(BaseModel, Generic[T]):
    code: int = 200
    status: str = "success"
    data: Optional[T] = None


class ResponseList(BaseModel, Generic[T]):
    code: int = 200
    status: str = "success"
    data: List[T] = []


class ResponseBuilder:
    @staticmethod
    def ok(data: Any = None) -> Response[Any]:
        return Response[Any].model_validate({"status": "success", "data": data})

    @staticmethod
    def ok_list(data: List[Any]) -> ResponseList[Any]:
        return ResponseList[Any].model_validate({"status": "success", "data": data})