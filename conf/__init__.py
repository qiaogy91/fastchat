#!/usr/bin/env python
# @Project ：fastchat 
# @File    ：__init__.py
# @Author  ：qiaogy
# @Email   ：qiaogy@example.com
# @Date    ：2025/7/16 12:55
from conf.settings import get_settings, get_orm_settings


SETTINGS = get_settings()
ORM_SETTINGS = get_orm_settings()
SMS_SETTINGS = SETTINGS.sms
REDIS_SETTINGS = SETTINGS.redis



if __name__ == '__main__':
   print(SETTINGS)