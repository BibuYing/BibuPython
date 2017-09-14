# coding=utf-8

import time


def getNowTime():
    """
    获取当前时间戳
    :return: int时间戳
    """
    return int(time.time())


def getNowStrfTime(timeStyle=None):
    """
     获取当前格式化时间
    :param timeStyle: 格式
    :return: string 格式化时间
    """
    if not timeStyle:
        timeStyle = "%Y-%m-%d %H:%M:%S"
    # 不传时间即代表当前时间
    return time.strftime(timeStyle)


def timeToLong(timeStr, timeStyle):
    """
    时间转时间戳
    :param timeStr:
    :param timeStyle:
    :return:
    """
    timeTuple = time.strptime(timeStr, timeStyle)
    return int(time.mktime(timeTuple))


def formatTime(longTime, timeStyle=None):
    if not timeStyle:
        timeStyle = "%Y-%m-%d %H:%M:%S"
    return time.strftime(timeStyle, time.localtime(longTime))
