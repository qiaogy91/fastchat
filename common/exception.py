#!/usr/bin/env python
# @Project ：fastchat 
# @File    ：exception.py
# @Author  ：qiaogy
# @Email   ：qiaogy@example.com
# @Date    ：2025/7/16 18:25
'''
目前有2种类型错误：
1. 没有按照要求传递指定参数，通常FastAPI 会返回 JSON 格式的错误
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
2. 用户参数传递正确，但是服务器内部运行异常，服务端直接返回纯文本 Internal Server Error

'''

from fastapi import Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from common.logs import get_logger
from conf import SETTINGS

logger = get_logger(SETTINGS.server.name)


async def global_http_exception_handler(request: Request, ex: HTTPException) -> JSONResponse:
    """ 服务内部异常
    :param request: 请求体对象
    :param ex: 异常对象
    :return:
    """
    logger.error(f"发生异常：{ex.detail}")  # 服务端内部异常需要记录下日志

    return JSONResponse(status_code=200, content={
        'code': ex.status_code,
        'msg': ex.detail,
        'status': 'Failed'
    })


async def gloabl_request_exception_handler(request: Request, ex: RequestValidationError) -> JSONResponse:
    """ 请求参数校验异常
    :param request: 请求体对象
    :param ex: 异常对象
    :return:
    """
    return JSONResponse(status_code=200, content={
        'code': status.HTTP_400_BAD_REQUEST,
        'msg': ex.errors()[0],
        'status': 'Failed'
    })



exception_handlers = {
    HTTPException: global_http_exception_handler,
    RequestValidationError: gloabl_request_exception_handler
}
