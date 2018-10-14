#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 10/9/18 5:04 PM
# @Author  : xiongzhibiao
# @Email   : xiongzhibiao@landmind.cn
# @File    : utils.py
# @Software: PyCharm
import time


def retry_func_when_retrun_is_none(retry_times=1, sleep_time=0):
    def decorator(func):
        def wrapper(*args, **kwargs):
            local_times = retry_times
            while local_times > 0:
                ret = func(*args)
                if ret is not None:
                    return ret
                local_times = local_times - 1
                time.sleep(sleep_time)
        return wrapper
    return decorator



