import requests
from utils.http import get_request_headers
from lxml import etree
from domain import Proxy


class BaseSpider(object):
    # 代理ip网址的URL
    urls = []
    # 分组xpath，包含代理ip信息标签列表的xpath
    group_xpath = ''
    # 组内的xpath，获取代理ip详情信息xpath
    detail_xpath = {}

    # 提供初始方法，传入url列表...
    def __init__(self, urls=[], group_xpath='', detail_xpath={}):
        if urls:
            self.urls = urls
        if group_xpath:
            self.group_xpath = group_xpath
        if detail_xpath:
            self.detail_xpath = detail_xpath

    def get_page_from_url(self, url):
        response = requests.get(url, headers=get_request_headers())
        return response.content

    def get_first_from_list(self, lis):
        # 如果列表中有元素就返回 没有就返回空
        return lis[0] if len(lis) != 0 else ''

    def get_proxies_from_page(self, page):
        '''解析页面'''
        element = etree.HTML(page)
        # 获取包含代理ip信息的标签列表
        trs = element.xpath(self.group_xpath)
        # 遍历trs  获取ip
        for tr in trs:
            ip = self.get_first_from_list(tr.xpath(self.detail_xpath['ip']))
            port = self.get_first_from_list(tr.xpath(self.detail_xpath['port']))
            area = self.get_first_from_list(tr.xpath(self.detail_xpath['area']))
            proxy = Proxy(ip, port, area=area)
            yield proxy

    def get_proxies(self):
        # 对外提供获取代理ip的方法
        for url in self.urls:
            page = self.get_page_from_url(url)
            proxies = self.get_proxies_from_page(page)
            yield from proxies


if __name__ == '__main__':
    config = {
        'urls': ['http://www.ip3366.net/free/?stype=1&page={}'.format(i) for i in range(1, 4)],
        'group_xpath': '//*[@id="list"]/table/tbody/tr',
        'detail_xpath': {
            'ip': './/td[1]/text()',
            'port': './/td[2]/text()',
            'area': './/td[5]/text()'
        }
    }
    spider = BaseSpider(**config)
    for proxy in spider.get_proxies():
        print(proxy)
