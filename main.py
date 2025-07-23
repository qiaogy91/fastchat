#!/usr/bin/env python
# @Project ：fastchat 
# @File    ：main.py
# @Author  ：qiaogy
# @Email   ：qiaogy@example.com
# @Date    ：2025/7/16 11:31
import uvicorn
from apps import get_app
from conf import SETTINGS

app = get_app()

if __name__ == '__main__':
    print(SETTINGS.model_dump())
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
