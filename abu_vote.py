import random
import requests
from bs4 import BeautifulSoup
from abu import proxies, auth


def swith_ip():
    new_ip = requests.get("http://proxy.abuyun.com/switch-ip", proxies=proxies, auth=auth)
    print("已经切换IP",new_ip)

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
                          proxies=proxies,
                          auth=auth,
                          timeout=120,
                          )
        print(r.text)
        return r.text
    except Exception as e:
        return "失败"

def get_token():
    token_url = "http://gcw.ynradio.com/seyy.php/Home/Vote/showPoll/pid/{}"
    channel_lst = [2, ]
    for channel in channel_lst:
        # token_url = token_url.format(channel)
        try:
            token_url = "http://gcw.ynradio.com/seyy.php/home/Vote/showPollPage/pid/1/sid/0"
            a = requests.get(token_url,
                             proxies=proxies,
                             timeout=10,
                             auth=auth,
                             )
            if a.status_code != 200:
                continue
            soup = BeautifulSoup(a.text, "lxml")
            return soup.find('input', {'name': 'token'}).get('value'), channel
        except Exception as e:
            print(e)
            return False, False


def get_phone_num():
    num1 = [3, 4, 5, 8]
    num2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    sum_str = ""
    for i in range(9):
        sum_str += str(random.choice(num2))
    return "1" + str(random.choice(num1)) + sum_str


def test():
    while True:
        token, channel = get_token()
        if not token:
            swith_ip()
            continue

        token_info = {
            'token': token,
            'channel': channel,
            'phone': get_phone_num(),
        }
        vote_result = vote_to_person(token_info)
        if "成功" not in vote_result:
            swith_ip()

if __name__ == "__main__":
    test()
