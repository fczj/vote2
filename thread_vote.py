from queue import Queue
import threading
from utils import get_proxy_mg, check_proxy
from config import proxys_info
import time
import random
import requests
from bs4 import BeautifulSoup
from abu import  *

proxy_queue = Queue(1)
token_queue = Queue(1)


def vote_to_person(token_info):
    token_url = "http://gcw.ynradio.com/seyy.php/Home/Vote/showPoll/pid/{}"
    headers = {
        'Host': 'gcw.ynradio.com',
        'Proxy-Connection': 'keep-alive',
        'Content-Length': '74',
        'Accept': '*/*',
        'Origin': 'http://gcw.ynradio.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://gcw.ynradio.com/seyy.php/Home/Vote/showPoll/pid/{}'.format(2),
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    data = {
        'pid': 2,
        'candidates[]': 1066,
        'token': token_info['token'],
        'phonenum': get_phone_num(),
    }

    try:
        r = requests.post("http://gcw.ynradio.com/seyy.php/home/vote/votePostPhone",
                          data=data,
                          headers=headers,
                          verify=False,
                          allow_redirects=False,
                          # proxies={"http": "http://"+token_info['proxy']},
                          proxies = proxies,
                          auth = auth,
                          timeout=150,
                          )
        print(r.text)
        return r.text
    except Exception as e:
        print(e)
        pass


def get_token(proxy):
    print("开始获取token", proxy)
    token_url = "http://gcw.ynradio.com/seyy.php/Home/Vote/showPoll/pid/{}"
    channel_lst = [2, ]
    for channel in channel_lst:
        token_url = token_url.format(channel)
        try:
            token_url = "http://gcw.ynradio.com/seyy.php/home/Vote/showPollPage/pid/1/sid/0"
            a = requests.get(token_url,
                             # proxies={"http": "http://"+proxy},
                             proxies = proxies,
                             timeout=20,
                             auth = auth,
                             )
            if a.status_code != 200:
                continue
            soup = BeautifulSoup(a.text, "lxml")
            return soup.find('input', {'name': 'token'}).get('value'), channel
        except Exception as e:
            print(e)
            return None, None


def get_phone_num():
    num1 = [3, 4, 5, 8]
    num2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    sum_str = ""
    for i in range(9):
        sum_str += str(random.choice(num2))
    return "1" + str(random.choice(num1)) + sum_str


class ProxyGenerate(threading.Thread):
    def __init__(self, get_channel):
        threading.Thread.__init__(self)
        self.get_proxy_url = proxys_info[get_channel]

    @staticmethod
    def add_proxy_to_queue(proxy):
        proxy_queue.put(proxy)

    def run(self):
        while True:
            print("=开始获取代理")
            proxys = get_proxy_mg(self.get_proxy_url)
            print(proxys, "="*50)
            if proxys is None:
                time.sleep(200)
                continue
            else:
                for proxy in proxys:
                    proxy_info_with_time = {
                        'proxy': proxy,
                        'times': 0,
                    }
                    self.add_proxy_to_queue(proxy_info_with_time)
            time.sleep(60)


class TokenGenerate(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            proxy = proxy_queue.get()
            print("获取到的proxy", proxy)
            if not check_proxy(proxy['proxy']):
                continue
            if proxy['times'] == 5:
                continue
            phone = get_phone_num()
            try:
                token, channel = get_token(proxy['proxy'])
            except Exception as e:
                continue
            print()
            token_info = {
                'proxy': proxy['proxy'],
                'token': token,
                'channel': channel,
                'phone': phone,
                'times': proxy['times'] + 1,
            }
            token_queue.put(token_info)


class Vote(threading.Thread):
    def __init__(self, token_info):
        threading.Thread.__init__(self)
        self.token_info = token_info

    def run(self):
        vote_result = vote_to_person(self.token_info)
        if vote_result is not None:
            proxy_info_with_time = {
                'proxy': self.token_info['proxy'],
                'times': self.token_info['times'],
            }
            if "成功" not in vote_result:
                proxy_info_with_time['times'] = 5
            proxy_queue.put(proxy_info_with_time)



def test():
    proxy = "A"
    token, channel = get_token(proxy)
    print(token, channel)

    token_info = {
        'proxy': proxy,
        'token': token,
        'channel': channel,
        'phone': get_phone_num(),
        # 'code_math': get_code_math(proxy)
    }
    vote_to_person(token_info)

def start():
    a = ProxyGenerate(0)
    a.start()
    b = TokenGenerate()
    b.start()


if __name__ == "__main__":
    test()
    # start()
    # while True:
    #     token_info = token_queue.get()
    #     t = Vote(token_info)
    #     t.start()
    #     # t.join()
    #
    # proxys = get_proxy_mg(proxys_info[1])
    # for proxy in proxys:
    #     test(proxy)
