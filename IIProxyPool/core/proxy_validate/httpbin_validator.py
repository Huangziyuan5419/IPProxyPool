import time
import requests
import json

from utils.http import get_request_headers
from settings import TEST_TIMEOUT
from utils.log import logger
from domain import Proxy


def check_proxy(proxy):
    '''
    用于检查指定代理ip
    :param proxy:
    :return:
    '''
    proxies = {
        'http': 'http://{}:{}'.format(proxy.ip, proxy.port),
        'https': 'https://{}:{}'.format(proxy.ip, proxy.port),
    }
    # 测试代理ip
    http, http_nick_type, http_speed = __check_http_proxies(proxies)
    https, https_nick_type, https_speed = __check_http_proxies(proxies, False)
    if http and https:
        proxy.protocol = 2
        proxy.nick_type = https_nick_type
        proxy.speed = https_speed
    elif http:
        proxy.protocol = 0
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif https:
        proxy.protocol = 1
        proxy.nick_type = https_nick_type
        proxy.speed = https_speed
    else:
        proxy.protocol = -1
        proxy.nick_type = -1
        proxy.speed = -1
    return proxy


# 测试http类型
def __check_http_proxies(proxies, is_http=True):
    # 匿名程度
    nick_type = -1
    # 响应速度
    speed = -1
    if is_http:
        test_url = 'http://httpbin.org/get'
    else:
        test_url = 'https://httpbin.org/get'
    # 获取开始时间
    start = time.time()
    try:
        # 发送请求
        response = requests.get(test_url, headers=get_request_headers(), proxies=proxies, timeout=TEST_TIMEOUT)
        # 请求成功
        if response.ok:
            # 计算速度
            speed = round(time.time() - start, 2)  # 保留两位小数
            dic = json.loads(response.text)
            # 匿名程度
            # 获取来源的ip：orgin
            origin = dic['origin']
            proxy_connection = dic['headers'].get('Proxy-Connection', None)
            if ',' in origin:
                # 如果 响应的orgin有 ',' ,就是透明代理
                nick_type = 2
            elif proxy_connection:
                # 如果 响应的origin有proxy_connection  ,就是匿名代理
                nick_type = 1
            else:
                # 高匿代理
                nick_type = 0
            return True, nick_type, speed
        return False, nick_type, speed
    except Exception as e:
        # logger.exception(e)
        return False, nick_type, speed


if __name__ == '__main__':
    proxy = Proxy('221.2.155.35', '8060')
    print(check_proxy(proxy))