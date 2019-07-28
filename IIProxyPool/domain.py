from settings import MAX_SCORE


class Proxy(object):
    def __init__(self, ip, port, protocol=-1, nick_type=-1, speed=-1, area=None, score=MAX_SCORE, disable_domains=None):
        # 代理ip
        self.ip = ip
        # 代理IP端口
        self.port = port
        # 代理ip支持的协议类型
        self.protocol = protocol
        # 代理匿名程度 高匿：0，匿名：1，透明：2
        self.nick_type = nick_type
        # 代理ip的速度
        self.speed = speed
        # 代理ip的地区
        self.area = area
        # 代理ip的分数
        self.score = score
        # 不可用域名列表，有些代理ip在某些域名下不可用，但是其他域名下可用
        self.disable_domains = disable_domains

    def __str__(self):
        # 返回数据字符串
        return str(self.__dict__)
