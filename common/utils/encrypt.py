#!/usr/bin/env python
# @Project ：fastchat 
# @File    ：encrypt.py
# @Author  ：qiaogy
# @Email   ：qiaogy@example.com
# @Date    ：2025/7/18 18:10
from passlib.context import CryptContext


class Hashing:
    @staticmethod
    def hash(password: str) -> str:
        return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)

    @staticmethod
    def verify(raw_password: str, hash_password: str):
        return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(raw_password, hash_password)


if __name__ == '__main__':

    c1 = Hashing.hash("redhat")
    c2 = Hashing.hash("redhat")
    print(f'{c1}\n{c2}')
    v = Hashing.verify("redhat", c2)
    print(v)