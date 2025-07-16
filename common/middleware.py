#!/usr/bin/env python
# @Project ：fastchat 
# @File    ：middleware.py
# @Author  ：qiaogy
# @Email   ：qiaogy@example.com
# @Date    ：2025/7/16 18:25
import time
from fastapi import Request, Response
from common.logs import get_logger
from conf import SETTINGS


async def request_duration(request: Request, call_next) -> Response:
    logger = get_logger(SETTINGS.server.name)
    start = time.time()

    response = await call_next(request)

    duration = '{0:.2f}'.format((time.time() - start) * 1000)
    logger.info(f"path={request.url.path} timer={duration}ms status_code={response.status_code}")

    return response
