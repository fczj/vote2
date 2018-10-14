#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 10/11/18 4:16 PM
# @Author  : xiongzhibiao
# @Email   : xiongzhibiao@landmind.cn
# @File    : test.py
# @Software: PyCharm

import random

def get_phone_num():
    num1  = [3,4,5,8]
    num2 = [0,1,2,3,4,5,6,7,8,9]
    sum_str = ""
    for i in range(9):
        sum_str += str(random.choice(num2))

    return "1"+str(random.choice(num1)) + sum_str
for i in range(10):
    print(get_phone_num())
