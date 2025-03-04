import json
import requests

N = '\033[0m'
W = '\033[1;37m'
B = '\033[1;34m'
M = '\033[1;35m'
R = '\033[1;31m'
G = '\033[1;32m'
Y = '\033[1;33m'
C = '\033[1;36m'

underline = "\033[4m"
line = "—————————————————"

agent = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def session(proxies, headers, cookie):
    r = requests.Session()
    r.proxies = proxies
    r.headers = headers
    r.cookies.update(json.loads(cookie))
    return r



