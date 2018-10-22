import requests
import threading
import time
from bs4 import BeautifulSoup
from utils import retry_func_when_retrun_is_none
import random
import sys
from config import proxys_info


import random

proxies = {
  "http": None,
  "https": None,
}

def get_phone_num():
    num1  = [3,4,5,8]
    num2 = [0,1,2,3,4,5,6,7,8,9]
    sum_str = ""
    for i in range(9):
        sum_str += str(random.choice(num2))

    return "1"+str(random.choice(num1)) + sum_str


def check_proxy(proxy):
    try:
        a = requests.get("https://www.baidu.com",
                         timeout=0.2,
                         proxies=proxy,
                )
        if a.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print("代理失效", e)
        return False

class Vote(threading.Thread):
    def __init__(self, proxy):
        threading.Thread.__init__(self)
        self.proxy = {
            "http": "http://"+proxy
        }
        self.vote_number = 1066	#li
        self.token_url = "http://gcw.ynradio.com/seyy.php/Home/Vote/showPoll/pid/{}"
        self.vote_token = None
        self.vote_channel = None

    def get_token(self):
        print(self.proxy,"开始获取token")
        channel_lst = [2,]
        for channel in channel_lst:
            token_url = self.token_url.format(channel)
            try:
                # a = requests.get("http://gcw.ynradio.com/seyy.php/Home/Vote/showPoll/pid/1",
                a = requests.get(token_url,
                                 proxies=self.proxy,
                                 timeout=300,
                                 )
                if a.status_code != 200:
                    continue
                soup = BeautifulSoup(a.text, "lxml")
                return soup.find('input', {'name': 'token'}).get('value'), channel
            except Exception as e:
                print(e)
                pass
            if not check_proxy(self.proxy):
                break
            time.sleep(0.8)

    def vote_to_person(self):
        headers = {
            'Host': 'gcw.ynradio.com',
            'Proxy-Connection': 'keep-alive',
            'Content-Length': '74',
            'Accept': '*/*',
            'Origin': 'http://gcw.ynradio.com',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Content-Type':'application/x-www-form-urlencoded',
            'Referer': 'http://gcw.ynradio.com/seyy.php/Home/Vote/showPoll/pid/1',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

        data = {
            'pid': 2,
            'candidates[]': self.vote_number,
            'token': self.vote_token,
            'phonenum': get_phone_num(),
        }

        try:
            r = requests.post("http://gcw.ynradio.com/seyy.php/home/vote/votePostPhone",
                              data=data,
                              headers=headers,
                              verify=False,
                              allow_redirects=False,
                              proxies=self.proxy,
                              timeout=300,
                            )
            print("="*200)
            print(r.text)
            print("="*200)
            return r.text
        except Exception as e:
            print(e)
            pass

    def run(self):
        time.sleep(random.random())
        for i in range(5):
            # start_time = time.time()
            token = self.get_token()
            if token is None:
                print(self.proxy, "token获取失败")
                return
            self.vote_token, self.vote_channel = token
            print("第{}轮".format(i),self.proxy)
            vote_result = self.vote_to_person()
            time.sleep(1)
            # if vote_result is None:
            #     return
            # elif "成功" not in vote_result:
            #     return
            # else:
            #     print("投票成功", vote_result)

@retry_func_when_retrun_is_none(retry_times=10, sleep_time=15)
def get_proxy_mg():
    # proxy_num = int(sys.argv[1])
    # proxy_get_url = proxys_info[proxy_num]
    proxy_get_url = proxys_info[0]
    try:
        r = requests.get(proxy_get_url)
        r_json = r.json()
        if "RESULT" in r_json:
            result = r.json()['RESULT']
        else:
            result = r.json()['msg']
        ret = [i['ip']+':'+i['port'] for i in result]
        return ret
    except Exception as e:
        return None

if __name__ == "__main__":
    while True:
        proxys = get_proxy_mg()
        print(proxys)
        for proxy in proxys:
            check_proxy({"http":"http://"+proxy})
        #proxys = ["115.223.237.1:9000"]
        #check_proxy({"http":"http://"+proxys[0]})
        th_lst = []
        if proxys is None:
            print("代理失效")
            break
        for proxy in proxys:
            th_lst.append(Vote(proxy))
            time.sleep(2)
        for th in th_lst:
            th.start()
            time.sleep(2)
            #th.join()
        break


