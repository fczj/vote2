#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 10/9/18 5:04 PM
# @Author  : xiongzhibiao
# @Email   : xiongzhibiao@landmind.cn
# @File    : utils.py
# @Software: PyCharm
import time
import requests


def retry_func_when_retrun_is_none(retry_times=1, sleep_time=15):
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


def check_proxy(proxy):
    try:
        a = requests.get("https://www.baidu.com",
                         timeout=0.2,
                         proxies={'proxy':'http://'+proxy},
                         )
        if a.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print("代理失效：{}".format(proxy), e)
        return False


@retry_func_when_retrun_is_none(retry_times=10, sleep_time=100)
def get_proxy_mg(get_proxy_url):
    # proxy_num = int(sys.argv[1])
    # proxy_get_url = proxys_info[proxy_num]
    try:
        r = requests.get(get_proxy_url)
        print(r.text)
        r_json = r.json()
        if "RESULT" in r_json:
            result = r.json()['RESULT']
        else:
            result = r.json()['msg']
        ret = [i['ip'] + ':' + i['port'] for i in result]
        return ret
    except Exception as e:
        print("从蘑菇云获取代理失效", e)
        return None
