import requests
import re
import js2py

url = 'http://www.66ip.cn/1.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
}
session = requests.Session()
session.headers = headers
response = session.get(url)
# cookies = response.headers['Set-Cookie'].split(';')[0]
# print(cookies)
res = re.findall('<script>(.*?)</script>', response.text)[0]
# print(response.status_code)
# print(response.text)
# print(res)
js = res.replace('{eval(', '{code=(')
# print(js)
context = js2py.EvalJs()
context.execute(js)
# print(context.code)
cookie_code = re.findall("document.(cookie=.+)\+';Expires=Sat,", context.code)[0]
# print(cookie_code)
cookie_code = re.sub(r"var\s+(\w+)=document.*?firstChild.href", r"var \1='http://www.66ip.cn'", cookie_code)
# print(cookie_code)
c = context.execute(cookie_code)
# print(context.cookie)
cook = context.cookie.split('=')
session.cookies.set(cook[0],cook[1])
session.get(url)
# print(session.cookies)

#获取cookies字典
cookies = requests.utils.dict_from_cookiejar(session.cookies)

r = requests.get(url, headers=headers, cookies=cookies)
print(r.status_code)
print(r.content.decode('gbk'))