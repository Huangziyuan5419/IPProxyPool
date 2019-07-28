import logging


# 最大分数
MAX_SCORE = 50

# 默认配置
LOG_LEVEL = logging.INFO  # 默认等级
LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s)'
LOG_DATEFMT = '%Y-%m-%d %H:%H:%S'
LOG_FILENAME = 'log.log'

# 测试ip代理超时时间
TEST_TIMEOUT = 10

# MongoDB数据库的url
MONGO_URL = 'mongodb://127.0.0.1:27017'

PROXIES_SPIDERS = [
    # 爬虫的全类名，路径： 模块.类名
    'core.proxy_spider.proxy_spiders.XiciSpider',
    'core.proxy_spider.proxy_spiders.KuaidailiSpider',
    'core.proxy_spider.proxy_spiders.Ip3366Spider',
    'core.proxy_spider.proxy_spiders.ProxylistpluSpider',
]

# 配置多长时间运行爬虫
RUN_SPIDERS_INTERVAL = 12

# 配置代理ip检测的异步熟练
TEST_PROXIES_ASYNC_COUNT = 10

# 配置多长时间检测ip可用性
TEST_PROXIES_INTERVAL = 2

# 获取代理ip的数量 越小可用性越高  随机性越差
PROXIES_MAX_COUNT = 2
