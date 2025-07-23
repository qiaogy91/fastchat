#!/usr/bin/env python
# @Project ：fastchat 
# @File    ：middleware.py
# @Author  ：qiaogy
# @Email   ：qiaogy@example.com
# @Date    ：2025/7/16 18:25
import time
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from common.logs import get_logger
from common.utils.auth import JWT
from conf import SETTINGS

logger = get_logger("middleware")


class RequestDuration(BaseHTTPMiddleware):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info("middleware RequestDuration 已加载")
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start = time.time()

        response = await call_next(request)

        duration = '{0:.2f}'.format((time.time() - start) * 1000)
        logger.info(f"path={request.url.path} timer={duration}ms status_code={response.status_code}")

        return response


class Authentication(BaseHTTPMiddleware):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info("middleware authentication 已加载")

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # 白名单，直接放行
        if request.url.path in SETTINGS.jwt.white_list.split(','):
            return await call_next(request)

        # 校验Token
        token = request.cookies.get("token", None)
        if not token:
            return JSONResponse(status_code=401, content={'code': 401, "detail": 'token not found'})

        try:
            payload = JWT.verify_token(token)  # 验证不通过，会抛出异常
            # 从payload 中提取uid，从数据库获取用户对象，赋值给 request.user = ins
            return await call_next(request)
        except Exception as e:
            logger.info(e.__str__)
            return JSONResponse(status_code=401, content={'code': 401, "detail": e.__str__()})


