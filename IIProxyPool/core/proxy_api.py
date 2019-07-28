from flask import Flask
from flask import request
import json

from core.db.mongo_pool import MongoPool
from settings import PROXIES_MAX_COUNT


class ProxyApi(object):
    def __init__(self):
        self.app = Flask(__name__)
        # 创建数据库
        self.mongo_pool = MongoPool()

        @self.app.route('/random')
        def random():
            '''
                实现根据协议类型和域名， 提供随机的获取高可用代理ip服务
                可以通过 protocol 和 domain 参数对ip进行过滤
                protocol：当前请求的协议类型
                domain： 当前请求域名
            :return:
            '''
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')
            proxy = self.mongo_pool.random_proxy(protocol, domain, count=PROXIES_MAX_COUNT)
            if protocol:
                return '{}://{}:{}'.format(protocol, proxy.ip, proxy.port)
            else:
                return '{}:{}'.format(proxy.ip, proxy.port)

        @self.app.route('/proxies')
        def proxies():
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')
            proxies = self.mongo_pool.get_proxies(protocol, domain, count=PROXIES_MAX_COUNT)
            # proxies 是一个对象的列表，不能json序列化 ，需要转化为字典列表
            proxies = [proxy.__dict__ for proxy in proxies]
            # 返回json
            return json.dumps(proxies)

        @self.app.route('/disable_domain')
        def disable_domain():
            ip = request.args.get('ip')
            domain = request.args.get('domain')
            if ip is None:
                return "请提供ip参数"
            if domain is None:
                return "请提供domain参数"
            self.mongo_pool.disable_domain(ip, domain)
            return '{} 禁用域名 {} 成功'.format(ip, domain)

    def run(self):
        self.app.run('0.0.0.0', port=16888)

    @classmethod
    def start(cls):
        #        4. 实现start的类方法啊，用于通过类名，启动服务
        proxy_api = cls()
        proxy_api.run()


if __name__ == '__main__':
    # proxy_api = ProxyApi()
    # proxy_api.run()
    ProxyApi.start()
