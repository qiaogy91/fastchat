#!/usr/bin/env python
# @Project ：fastchat 
# @File    ：logs.py
# @Author  ：qiaogy
# @Email   ：qiaogy@example.com
# @Date    ：2025/7/16 18:25
import os
import logging
from logging import handlers, Logger
from conf import SETTINGS


def get_logger(name: str) -> Logger:
    """
    单例日志器对象，logging 模块内部维护了一个全局的 Logger 字典，多次调用 `logging.getLogger(name) ` 会返回同一个 Logger 实例
    """

    # 1. 实例化日志器对象
    logger: Logger = logging.getLogger(name)
    logger.setLevel(SETTINGS.logger.level)

    # 2. 设置输出目标
    if not logger.handlers:
        base = os.path.dirname(os.path.dirname(__file__)) # 项目根

        # 1. 创建handler
        th: logging.StreamHandler = logging.StreamHandler()
        rf: handlers.RotatingFileHandler = handlers.RotatingFileHandler(
            filename=f"{base}/{SETTINGS.logger.root}/{name}.log",
            mode='a',
            maxBytes=300 * 1024 * 1024,  # 300M
            backupCount=10,
            encoding='utf-8'
        )
        # 2. 设置handler 日志级别
        th.setLevel(logging.DEBUG)
        rf.setLevel(logging.INFO)

        # 3. 设置handler 输出格式
        simple_formatter = logging.Formatter(
            fmt="{levelname:<9} {asctime} {filename:<20}|{lineno:>4} | {message}",
            datefmt="%Y-%m-%d %H:%M:%S",  # 固定长度时间，便于对齐
            style="{",
        )

        verbose_formatter = logging.Formatter(
            fmt="【{name:.20}】{levelname:<8} {asctime} {filename:<20}|{lineno:>4} | {message}",
            datefmt="%Y-%m-%d %H:%M:%S",
            style="{",
        )

        th.setFormatter(simple_formatter)
        rf.setFormatter(verbose_formatter)

        # 4. 将handler 附加到日志器对象中
        logger.addHandler(th)
        logger.addHandler(rf)

    return logger


if __name__ == '__main__':
    # 8. 调用日志器对象logger打印输出日志
    lg = get_logger('xxxxxxx')
    lg.info("这里是常规运行日志")
    lg.debug("开发人员在调试程序时自己手动打印的日志")
    lg.warning("这里是程序遇到未来会废弃的函数/方法时，输出的警告日志")
    lg.error("这里是程序发生错误时输出的日志")
    lg.critical("这是致命级别的日志，需要紧急修复的")

    # 多次调用实例化出来的日志对象，如果name相同，则得到的是同一个日志器对象（单例模式）
    logger1 = get_logger('dl')
    print(id(logger1), id(lg))
