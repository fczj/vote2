import requests
import re
from PIL import Image
proxy = {"http":"http:150.129.193.40:80"}
cheakcode_url = "http://gcw.ynradio.com/seyy/js/php/code_math.php?0.5414765450760557"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/55.0.2883.103 Safari/537.36', 'Connection':'keep-alive'}
response2 = requests.get(url=cheakcode_url, headers=headers,proxies=proxy)
with open('code.jpg','wb') as fp:
    fp.write(response2.content)
img=Image.open('code.jpg')
img.show()

