from pymongo import MongoClient
import pymongo
import random

from settings import MONGO_URL
from utils.log import logger
from domain import Proxy


class MongoPool(object):
    def __init__(self):
        # 建立数据库的链接
        self.client = MongoClient(MONGO_URL)
        # 获取要操作的集合
        self.proxies = self.client['proxies_pool']['proxies']

    def __del__(self):
        # 关闭连接
        self.client.close()

    def insert_one(self, proxy):
        '''
        实现插入功能
        :param proxy:
        :return:
        '''
        count = self.proxies.count_documents({'_id': proxy.ip})
        if count == 0:
            # 我们使用proxy.ip作为 MongoDB 的主键: _id
            dic = proxy.__dict__
            dic['_id'] = proxy.ip
            self.proxies.insert_one(dic)
            logger.info('插入新代理{}'.format(proxy))
        else:
            logger.warning('代理{}已经存在'.format(proxy))

    def update_one(self, proxy):
        """
        实现修改功能
        :param proxy:
        :return:
        """
        self.proxies.update_one({'_id': proxy.ip}, {'$set': proxy.__dict__})

    def delete_one(self, proxy):
        '''
        删除代理
        :param proxy:
        :return:
        '''
        self.proxies.delete_one({'_id': proxy.ip})
        logger.info('删除IP：{}'.format(proxy))

    def find_all(self):
        '''
        查询所以ip代理的功能
        :return:
        '''
        cursor = self.proxies.find()
        for item in cursor:
            # print(item)
            item.pop('_id')
            # print(item)
            proxy = Proxy(**item)
            yield proxy

    def find(self, conditions={}, count=0):
        '''
        实现查询功能
        :param conditions:
        :param count:
        :return:
        '''
        cursor = self.proxies.find(conditions, limit=count).sort([
            ('score', pymongo.DESCENDING), ('speed', pymongo.ASCENDING)
        ])
        # 准备列表，用于储存查询处理代理ip
        proxy_list = []
        # 遍历cursor
        for item in cursor:
            item.pop("_id")
            proxy = Proxy(**item)
            proxy_list.append(proxy)
        return proxy_list

    def get_proxies(self, protocol=None, domain=None, count=1, nick_type=2):
        '''
        实现根据协议类型和访问网站的域名，获取ip列表
        :param protocol: https  http
        :param domain: 域名
        :param count:数量
        :param nick_type: 默认高匿
        :return: 满足要求的代理
        '''
        # 定义查询条件
        conditions = {'nick_type': nick_type}
        # 根据协议，进行查询
        if protocol is None:
            # 如果没有传入协议类型，返回支持https 和http的代理ip
            conditions['protocol'] = 2
        elif protocol.lower() == 'http':
            conditions['protocol'] = {'$in': [0, 2]}
        else:
            conditions['protocol'] = {'$in': [1, 2]}
        if domain:
            conditions['disable_domains'] = {'#nin': [domain]}
        return self.find(conditions, count=count)

    def random_proxy(self, protocol=None, domain=None, count=1, nick_type=0):
        '''
        随机获取一个代理ip
        :param protocol:
        :param domain:
        :param nick_type:
        :return:
        '''
        proxy_list = self.get_proxies(protocol=protocol, domain=domain, count=count, nick_type=nick_type)
        return random.choice(proxy_list)

    def disable_domain(self, ip, domain):
        '''
        实现把指定的域名添加到指定的ip 的disable_domain列表中
        :param ip:
        :param domain:
        :return:
        '''
        if self.proxies.count_documents({'_id': ip, 'disable_domains': domain}):
            # 如果没有这个域名则添加
            self.proxies.update_one({'_id': ip}, {'$push': {'disable_domains': domain}})
            return True
        return False


if __name__ == '__main__':
    mongo = MongoPool()
    # proxy = Proxy('119.2.155.35', '8060')
    # # print(proxy)
    # mongo.insert_one(proxy)
    # proxy = Proxy('119.2.155.35', '8888')
    # mongo.update_one(proxy)
    # proxy = Proxy('119.2.155.35', '8888')
    # for i in mongo.find_all():
    #     print(i)
    # proxy = Proxy(**dic)
    # mongo.insert_one(proxy)
    # for proxy in mongo.find({'protocol': 2}, count=1):
    #     print(proxy)
    # for proxy in mongo.get_proxies():
    #     print(proxy)
    proxy = mongo.random_proxy()
    print(proxy)
