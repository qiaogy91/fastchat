#!/usr/bin/env python
# @Project ：fastchat 
# @File    ：exception.py
# @Author  ：qiaogy
# @Email   ：qiaogy@example.com
# @Date    ：2025/7/16 18:25
from fastapi import Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from common.logs import get_logger
from common.response import Response
from conf import SETTINGS
from typing import Any

logger = get_logger(SETTINGS.server.name)


async def global_http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP Exception: {str(exc.detail)}")
    content = Response[Any].model_validate({
        "code": exc.status_code,  # 用户自定义异常码
        "status": "error",
        "data": str(exc.detail)
    }).model_dump()
    return JSONResponse(status_code=exc.status_code, content=content)


async def global_request_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Vlaidate Exception: {exc.errors()}")
    content = Response[Any].model_validate({
        "code": status.HTTP_400_BAD_REQUEST,
        "status": "error",
        "data": exc.errors()[0]
    }).model_dump()
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=content)


async def global_unknown_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unkown Exception: {exec.__str__()}")
    content = Response[Any].model_validate({
        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "status": "error",
        "data": exc.__str__()
    }).model_dump()
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=content)


exception_handlers = {
    # raise HTTPException(...) 时触发
    HTTPException: global_http_exception_handler,
    # 请求参数或请求体的 Pydantic 校验失败时，FastAPI 抛出 RequestValidationError，并自动触发
    RequestValidationError: global_request_exception_handler,
    # 其他任何异常，比如 1/0 ,并调用该函数处理
    Exception: global_unknown_exception_handler,
}
