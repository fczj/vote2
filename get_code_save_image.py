import requests
from recg import recognize_digit, recognize
import random
import os


def get_phone_num():
    num1 = [3, 4, 5, 8]
    num2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    sum_str = ""
    for i in range(9):
        sum_str += str(random.choice(num2))
    return "1" + str(random.choice(num1)) + sum_str


def check_code(proxy, code):
    check_url = "http://gcw.ynradio.com/seyy.php/home/vote/chkCodeGet?act=math"
    headers = {
        'Host': 'gcw.ynradio.com',
        'Proxy-Connection': 'keep-alive',
        'Content-Length': '74',
        'Accept': '*/*',
        'Origin': 'http://gcw.ynradio.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://gcw.ynradio.com/seyy.php/Home/Vote/showPoll/pid/1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    data = {
        'code': code
    }

    try:
        r = requests.post(check_url,
                          data=data,
                          headers=headers,
                          verify=False,
                          allow_redirects=False,
                          proxies={'proxy': 'http://' + proxy},
                          timeout=100,
                          )
        print("=" * 20, r.text)
        return r.text
    except Exception as e:
        print(e)
        raise e
        return None


def get_code_math(proxy):
    old_proxy = proxy
    proxy = {"http": "http:" + proxy}
    pic_name = get_phone_num()
    cheakcode_url = "http://gcw.ynradio.com/seyy/js/php/code_math.php?" + str(random.random())
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/55.0.2883.103 Safari/537.36',
        'Connection': 'keep-alive'}
    response2 = requests.get(url=cheakcode_url, headers=headers, proxies=proxy)
    with open(pic_name, 'wb') as fp:
        fp.write(response2.content)
    a = recognize(pic_name)
    print(pic_name)
    os.remove(pic_name)
    check_code(old_proxy, a)
    return a
