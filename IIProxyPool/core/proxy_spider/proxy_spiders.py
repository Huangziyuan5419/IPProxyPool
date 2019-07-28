import time
import random
import requests
from core.proxy_spider.base_spider import BaseSpider


class XiciSpider(BaseSpider):
    urls = ['https://www.xicidaili.com/nn/{}'.format(i) for i in range(1, 11)]
    group_xpath = '//*[@id="ip_list"]//tr[position()>1]'
    detail_xpath = {
        'ip': './/td[2]/text()',
        'port': './/td[3]/text()',
        'area': './/td[4]/a/text()',
    }


class Ip3366Spider(BaseSpider):
    urls = ['http://www.ip3366.net/free/?stype=1&page={}'.format(i) for i in range(1, 6)]
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    detail_xpath = {
        'ip': './/td[1]/text()',
        'port': './/td[2]/text()',
        'area': './/td[5]/text()'
    }


class KuaidailiSpider(BaseSpider):
    urls = ['https://www.kuaidaili.com/free/inha/{}'.format(i) for i in range(1, 6)]
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    detail_xpath = {
        'ip': './/td[1]/text()',
        'port': './/td[2]/text()',
        'area': './/td[5]/text()'
    }

    def get_page_from_url(self, url):
        # 随机等待一到三秒
        time.sleep(random.uniform(1, 3))
        return super().get_page_from_url(url)


class ProxylistpluSpider(BaseSpider):
    urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-{}'.format(i) for i in range(1, 6)]
    group_xpath = '//*[@id="page"]/table[2]//tr[position()>2]'
    detail_xpath = {
        'ip': './/td[2]/text()',
        'port': './/td[3]/text()',
        'area': './/td[5]/text()'
    }


# 66ip网页代理
class Ip66Spider(BaseSpider):
    pass


if __name__ == '__main__':
    spider = KuaidailiSpider()
    for proxy in spider.get_proxies():
        print(proxy)
    # spider = ProxylistpluSpider()
    # for proxy in spider.get_proxies():
    #     print(proxy)
    # url = 'http://www.66ip.cn/1.html'
    # headers = {
    #     'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 75.0.3770.142Safari / 537.36',
    #     'Cookie': '__jsluid_h=6c449316ac75b3a347f4490aae311189; __jsl_clearance=1564235923.903|0|WuYwexVhTQgQVyiX%2FNF98yTkGBU%3D; Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1564235927; Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4=1564236210',
    # }
    # response = requests.get(url, headers=headers)
    # print(response.status_code)
    # print(response.text)

