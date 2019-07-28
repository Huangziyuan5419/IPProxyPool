from gevent import monkey
from gevent.pool import Pool
from queue import Queue
import schedule
import time
from core.db.mongo_pool import MongoPool
from core.proxy_validate.httpbin_validator import check_proxy
from settings import MAX_SCORE, TEST_PROXIES_ASYNC_COUNT, TEST_PROXIES_INTERVAL


monkey.patch_all()


class ProxyTester(object):
    def __init__(self):
        self.mongo_pool = MongoPool()
        self.queue = Queue()
        self.coroutine_pool = Pool()

    def _check_callback(self, temp):
        self.coroutine_pool.apply_async(self._check_one_proxy, callback=self._check_callback)

    def run(self):
        # 检测所有ip可用性
        # 获取数据库的ip
        proxies = self.mongo_pool.find_all()
        # 遍历代理ip列表
        for proxy in proxies:
            # 把代理ip添加到队列中
            self.queue.put(proxy)
        # 开启异步检测
        for i in range(TEST_PROXIES_ASYNC_COUNT):
            # 通过异步回调 使用循环不停的执行
            self.coroutine_pool.apply_async(self._check_one_proxy, callback=self._check_callback)
        # 让当前线程，等待队列完成
        self.queue.join()

    def _check_one_proxy(self):
        # print(proxy)
        # 检测ip可用性
        # 从队列里面获取队列
        proxy = self.queue.get()
        proxy = check_proxy(proxy)
        # 如果可用  代理分数减掉1
        if proxy.speed == -1:
            proxy.score -= 1
            # 判断分数是否为零
            if proxy.score == 0:
                self.mongo_pool.delete_one(proxy)
            else:
                # 更新代理ip
                self.mongo_pool.update_one(proxy)
        else:
            # 如果代理可用， 就恢复代理的分数， 更新到数据库中
            proxy.score = MAX_SCORE
            self.mongo_pool.update_one(proxy)
        self.queue.task_done()

    @classmethod
    def start(cls):
        # 创建对象
        proxy_tester = cls()
        proxy_tester.run()
        # 每隔一定的时间执行一次
        schedule.every(TEST_PROXIES_INTERVAL).hours.do(proxy_tester.run)
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    # pt = ProxyTester()
    # pt.run()
    ProxyTester.start()


