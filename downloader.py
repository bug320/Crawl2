#-*-coding:utf-8 -*-

import urlparse
import urllib2
import random
import time
from datetime import datetime, timedelta
import socket
from const_var import *
class Downloader:
    """the class for downloader 
    """
    def __init__(self, delay=DEFAULT_DELAY, header=DEFAULT_HEADER, proxies=None, num_retries=DEFAULT_RETRIES, timeout=DEFAULT_TIMEOUT, opener=None, cache=None,logqueue=None):
        """
        initialize the `Downloader` 　　　　　　　　	
        :param delay: set the time of the de lay	
        :param header: set the header for request　　　　 
        :param proxies: the proxies for the website　　　
        :param num_retries: the num for retries 　　　　　
        :param timeout: the timeout for socket         
        :param opener: urllib2.build_opener()　　　　　　　　　　　　　　
        :param cache: the cache object and it must have the __getitem__ and __setitem__ a
        """
        socket.setdefaulttimeout(timeout) # 设置socket的超时时间，来控制下载内容时的等待时间。
        self.throttle = Throttle(delay)   # 设置延时,避免爬的太快对服务器造成太大的影响而被封禁
        self.header = header              # 设置请求头
        self.proxies = proxies            # 设置代理
        self.num_retries = num_retries    # 设置 5XX 错误重新下载的尝试次数
        self.opener = opener              #　urllib2.build_opener()　默认设为　None 就好，反正我不想像自己在创建一个
        self.cache = cache                # 设置下载缓存的对象,必须有接口__getitem__ and __setitem__
        self.code = None
        self.logqueue = logqueue          # 记录断点

    def __call__(self, url):
        """
        can use the object for `Dowaloader` like a function call,and when call it,the __call__ is run
        so you can use as that:
            D = Download(...)
            html = D(url) #the url is the webpage which you want to download
        :param url:the url for download 
        :return: 
        """
        result = None                                                                      # 保存下载请求结果的结果
        if self.cache:
            try:
                result = self.cache[url]                                                   # 尝试从缓存中返回存储结果
            except KeyError:
                # url is not available in cache 
                pass
            else:
                if (not self.code) and (self.num_retries > 0 and 500 <= self.code < 600):
                    # server error so ignore result from cache and re-download
                    result = None
        if result is None:                                                                  # 如果在缓存中没有得到结果就重新爬
            # result was not loaded from cache so still need to download
            self.throttle.wait(url)                                                         # 设置下载时延
            proxy = random.choice(self.proxies) if self.proxies else None                   #代理设置
            headers = self.header                                                           #请求头设置
            result = self.download(url, headers, proxy=proxy, num_retries=self.num_retries) #下载网页
            if self.cache:                                                                  #以url为键值保存到缓存中
                # save result to cache
                self.cache[url] = result
        return result



    def download(self, url, headers, proxy, num_retries, data=None):
        """
        the fuction to request the webpage and download the html
        :param url: the url for the webpage to download 
        :param headers: the header for the webpage
        :param proxy: the proxy for the webpage
        :param num_retries: the retries numbers when download error 5XX
        :param data:the default data when download error 
        :return: return a dict such as the html
        """
        if DEFAULT_DOWNLOAD_ECHO: print 'Downloading:', url
        request = urllib2.Request(url, data, headers or {})
        opener = self.opener or urllib2.build_opener()
        if proxy:
            proxy_params = {urlparse.urlparse(url).scheme: proxy}
            opener.add_handler(urllib2.ProxyHandler(proxy_params))
        try:
            response = opener.open(request)
            html = response.read()
            self.code = response.code
        except Exception as e:
            print 'Download error:', str(e)
            html = ''
            if hasattr(e, 'code'):
                self.code = e.code
                if num_retries > 0 and 500 <= self.code < 600:
                    # retry 5XX HTTP errors
                    if self.logqueue: # 如果没有取消断点机制则记录断点
                        self.logqueue.push(url=url,code=self.code)
                        pass
                    return self._get(url, headers, proxy, num_retries-1, data)  #_get() 错误返回值，默认为 None
            else:
                self.code = None
        return html


# 这个 Throttle 时网上找到，实现了下载延时
class Throttle: 
    """Throttle downloading by sleeping between requests to same domain
    """
    def __init__(self, delay):
        """
        
        :param delay:  delay between downloads for each domain
        """
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}
        
    def wait(self, url):
        """Delay if have accessed this domain recently
        :param url: the url for domain
        """
        domain = urlparse.urlsplit(url).netloc
        # 主要是分析urlstring，返回一个包含5个字符串项目的元组：协议、位置、路径、查询、片段,这里返回 位置
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()

if __name__ == "__main__":
    """
    第一次运行结果，表示在是下载的　cache info 只是缓存的log不用管，表示链接　hbase 正常，一般只有第二遍才有，但是我这里因以前运行过，所以有没有都无所谓
    cache info :: the cache is alreay existed
    Downloading: http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102
    OK
    而已次再运行，表示是从数据直接返回的
    cache info :: the cache is alreay existed
    Downloading: http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102
    OK


    """
    url = 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102'
    download = Downloader()
    D2 = Downloader()
    # D2.logqueue.push(1.2)
    html = download(url)
    print "OK"
    #print html 这个注释去掉就可看见下载的网页的源代码

    # #测试断点缓存机制是否可以不受　Downloader 类在不同地方实例化的影响
    # D = Downloader()
    # D.logqueue.push(url="url1",code="code1")
    # D2 = Downloader()
    # D.logqueue.push(url="Url2",code="Code2")
    # D3  = Downloader()
    # D3.logqueue.show()
    # D4 = Downloader()
    # D4.logqueue.pop()
    # D.logqueue.show()


    pass

