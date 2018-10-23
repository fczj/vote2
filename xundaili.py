import requests
import threading
import time
from bs4 import BeautifulSoup
import random
import sys
from config import proxys_info
from utils import get_proxy_mg, check_proxy

proxies = {
    "http": None,
    "https": None,
}


def get_phone_num():
    num1 = [3, 4, 5, 8]
    num2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    sum_str = ""
    for i in range(9):
        sum_str += str(random.choice(num2))
    return "1" + str(random.choice(num1)) + sum_str


class Vote(threading.Thread):
    def __init__(self, proxy):
        threading.Thread.__init__(self)
        self.proxy = {
            "http": "http://" + proxy
        }
        self.vote_number = 1066
        self.token_url = "http://gcw.ynradio.com/seyy.php/Home/Vote/showPoll/pid/{}"
        self.vote_token = None
        self.vote_channel = None

    def get_token(self):
        time.sleep(random.randint(1,12))
        print(self.proxy, "开始获取token")
        channel_lst = [2,]
        for channel in channel_lst:
            token_url = self.token_url.format(channel)
            try:
                a = requests.get(token_url,
                                 proxies=self.proxy,
                                 timeout=20,
                                 )
                if a.status_code != 200:
                    continue
                soup = BeautifulSoup(a.text, "lxml")
                return soup.find('input', {'name': 'token'}).get('value'), channel
            except Exception as e:
                print(e)
            # 代理失效
            if not check_proxy(self.proxy):
                break
            time.sleep(0.8)

    def vote_to_person(self):
        time.sleep(random.randint(2,5))
        headers = {
            'Host': 'gcw.ynradio.com',
            'Proxy-Connection': 'keep-alive',
            'Content-Length': '74',
            'Accept': '*/*',
            'Origin': 'http://gcw.ynradio.com',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://gcw.ynradio.com/seyy.php/Home/Vote/showPoll/pid/{}'.format(self.vote_channel),
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

        data = {
            'pid': self.vote_channel,
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
                              timeout=150,
                              )
            print("=" * 20, r.text)
            return r.text
        except Exception as e:
            print(e)
            pass

    def run(self):
        for i in range(1):
            start_time = time.time()
            token = self.get_token()
            if token is None:
                print(self.proxy, "token获取失败")
                return
            self.vote_token, self.vote_channel = token
            print("第{}轮".format(i), self.proxy)
            vote_result = self.vote_to_person()
            run_time = time.time() - start_time
            sleep_time = random.randint(4,12)
            time.sleep(sleep_time)


if __name__ == "__main__":
    while True:
        proxys = get_proxy_mg(proxys_info[int(sys.argv[1])])
        #proxys = get_proxy_mg(proxys_info[0])
        if proxys is None:
            print("代理失效")
            break

        th_list = []
        for proxy in proxys:
            if not check_proxy({"http": "http://" + proxy}):
                proxys.remove(proxy)
            else:
                th_list.append(Vote(proxy))
        for t in th_list:
            t.start()
            time.sleep(2)
        #for t in th_list:
        #    t.join()
        time.sleep(30)


