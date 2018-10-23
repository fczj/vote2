from requests.auth import HTTPProxyAuth


# 代理服务器
proxyHost = "proxy.abuyun.com"
proxyPort = "9010"

# 代理隧道验证信息
proxyUser = "H20Y0IHNGLT61C2P"
proxyPass = "4D6AA0C617EA0604"

proxies = {
            "http": proxyHost + ":" + proxyPort
           }
auth = HTTPProxyAuth(proxyUser, proxyPass)


# import requests
# a = requests.get("http://proxy.abuyun.com/current-ip",proxies=proxies,auth=auth)
# print(a.text)