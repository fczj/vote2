import requests
import threading
import time
from bs4 import BeautifulSoup
from utils import retry_func_when_retrun_is_none
import random
import sys

print("获取token时间")
start = time.time()
proxy = {"http":"http:150.129.193.40:80"}
cheakcode_url = "http://gcw.ynradio.com/seyy.php/Home/Vote/showPoll/pid/1"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/55.0.2883.103 Safari/537.36', 'Connection':'keep-alive'}
a = requests.get(url=cheakcode_url, headers=headers,proxies=proxy)
soup = BeautifulSoup(a.text, "lxml")
a = soup.find('input', {'name': 'token'}).get('value')
print(time.time() - start)

