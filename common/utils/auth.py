#!/usr/bin/env python
# @Project ：fastchat 
# @File    ：auth.py
# @Author  ：qiaogy
# @Email   ：qiaogy@example.com
# @Date    ：2025/7/22 18:18
import uuid
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
from datetime import datetime, timedelta,timezone
from conf import SETTINGS


class JWT(object):
    JWTError = JWTError
    ExpiredSignatureError = ExpiredSignatureError

    @staticmethod
    def create_token(data: dict):
        # jwt payload
        now_time = datetime.now(timezone.utc) # JWT 要求使用UTC 时间
        payload = {
            "exp": now_time + timedelta(seconds=SETTINGS.jwt.expire), # 过期时间
            "iat": now_time, # 签发时间
            "nbf": now_time, # 生效时间（同签发时间)
            "jti": str(uuid.uuid4()) # JWT 的唯一标识
        }

        # request 中的用户信息字典（比如 {name: user1}）
        payload.update(data)


        return jwt.encode(payload, SETTINGS.jwt.key, algorithm=SETTINGS.jwt.algorithm)

    @staticmethod
    def verify_token(token: str) -> dict:
        return jwt.decode(token, SETTINGS.jwt.key, algorithms=SETTINGS.jwt.algorithm)

if __name__ == '__main__':
    tk = JWT.create_token({"name": "qiaogy"})
    print(tk)

    print(JWT.verify_token(tk))
