# 打猴子补丁
from gevent import monkey
from gevent.pool import Pool
# 专门做动态导入的包
import importlib
import schedule
import time
from settings import PROXIES_SPIDERS
from core.proxy_validate.httpbin_validator import check_proxy
from core.db.mongo_pool import MongoPool
from utils.log import logger
from settings import RUN_SPIDERS_INTERVAL


monkey.patch_all()


class RunSpider(object):
    def __init__(self):
        # 创建mongopool对象
        self.mongo_pool = MongoPool()
        # 创建协程池
        self.coroutine_pool = Pool()

    def get_spider_from_settings(self):
        '''
        根据配置文件获取爬虫对象列表，
        :return:
        '''
        # 遍历文件爬虫的全类名
        for full_class_name in PROXIES_SPIDERS:
            # 获取模块名和类名
            module_name, class_name = full_class_name.rsplit('.', maxsplit=1)
            # print(full_class_name.rsplit('.', maxsplit=1))
            # 根据模块名导入模块
            module = importlib.import_module(module_name)
            # 根据类名，从模块中获取类
            cls = getattr(module, class_name)
            spider = cls()
            # print(spider)
            yield spider

    def run(self):
        #  根据配置文件获取爬虫对象列表，
        spiders = self.get_spider_from_settings()
        for spider in spiders:
            # 异步调用执行的方法
            self.coroutine_pool.apply_async(self._execute_one_spider_task, args=(spider,))
        # 调用协程的join，让当前线程等待 协程的任务完成
        self.coroutine_pool.join()

    def _execute_one_spider_task(self, spider):
        # 用于处理爬虫的方法
        try:
            # 遍历爬虫对象的方法
            for proxy in spider.get_proxies():
                # print(proxy)
                # 检测代理可用性
                proxy = check_proxy(proxy)
                # 如果speed不为-1 就说明可用
                if proxy.speed != -1:
                    self.mongo_pool.insert_one(proxy)
        except Exception as ex:
            logger.exception(ex)

    @classmethod
    def start(cls):
        rs = RunSpider()
        rs.run()

        # 每间隔多长时间进行一次执行
        # settings里面配置
        schedule.every(RUN_SPIDERS_INTERVAL).hours.do(rs.run)
        while True:
            # 检测时间  每隔一秒钟检查一次是否到了时间
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    # rs = RunSpider()
    # rs.run()
    # 测试schedle
    # def task():
    #     print('hehe')
    # schedule.every(2).seconds.do(task)
    # while True:
    #     # 检测
    #     schedule.run_pending()
    #     time.sleep(1)
    RunSpider.start()
