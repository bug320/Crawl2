# -*- coding:utf-8 -*-
import downloader
from urlparse import urljoin
import re
import shelve


pageLog = shelve.open('html_cache/page_cache/page_log.she',"c")

subpageShe = shelve.open('html_cache/subpage_cache/subpage.she',"c")
subpageLog = shelve.open('html_cache/subpage_cache/subpage_log.she',"c")

innerpageShe = shelve.open('html_cache/innerpage_cache/innerpage.she',"c")
innerpageLog = shelve.open('html_cache/innerpage_cache/innerpage_log.she',"c")

class GetUrl(object):
    __logs = set() # 记录断点
    __urls = set() # 去重集合
    def __init__(self,seed_url,cache=None) :
        self.seed_url = seed_url
        self.html = ""
        self.text = ""
        self.cache = cache
        # self.__ns = newspaper.Article()
        pass
    def download(self):
        if self.cache and self.seed_url in self.cache.keys():
            self.html = self.cache[self.seed_url]
            print "Get",self.seed_url,"from cache..."
            pass
        else:
            self.html = downloader.Downloader()(self.seed_url)
            self.cache[self.seed_url] = self.html
            print "Download",self.seed_url,"..."

            pass
        pass
    def praser(self):
        return
        pass
    @classmethod
    def logs(cls):
        return cls.__logsl
        pass
    @classmethod
    def urls(cls):
        return cls.__urls
    pass

class GetPagerUrl(GetUrl):
    pageShe = shelve.open('html_cache/page_cache/page.she', "c")
    def __init__(self,seed_url,cache=pageShe):
        GetUrl.__init__(self,seed_url,cache)
        self.download()
        pass
    def subpaer_urls(self,html=None):
        html = html if html else self.html
        urls = [re.findall(r'href="(.*)">', line)[0] for line in
                re.findall(r'<div class="List2">(.*?)</div>', html, re.DOTALL)[0].split('\n')
                if re.search(r'href', line)]
        return [ urljoin(self.seed_url,url) for url in urls]
        pass

    def firstPager_url(self,html=None):
        html = html if html else self.html
        urls =  [re.findall(r'href="(.*)">', line)[0] for line in
                re.findall(r'<li class="firstPage">(.*?)</li>', html, re.DOTALL)[0].split('\n')
                if re.search(r'href', line)]
        return urljoin(self.seed_url,urls[0]) if urls else  None
        # < li class ="firstPage" >
        # < / li >
        pass
    def prePager_url(self,html=None):
        html = html if html else self.html
        urls =  [re.findall(r'href="(.*)">', line)[0] for line in
                re.findall(r'<li class="prePage">(.*?)</li>', html, re.DOTALL)[0].split('\n')
                if re.search(r'href', line)]
        return urljoin(self.seed_url,urls[0]) if urls else  None
        # < li class ="firstPage" >
        # < / li >
        pass
    def nextPager_url(self,html=None):
        html = html if html else self.html
        urls =  [re.findall(r'href="(.*)">', line)[0] for line in
                re.findall(r'<li class="nextPage">(.*?)</li>', html, re.DOTALL)[0].split('\n')
                if re.search(r'href', line)]
        return urljoin(self.seed_url,urls[0]) if urls else  None


        # < li class ="nextPage" >
        # < a href = "ggcx?appCode=H60&channelCode=0102&bz=0&pageSize=10&pageNo=2" > 下一页 < / a >
        # < / li >
        pass

    def lastPager_url(self,html=None):
        html = html if html else self.html
        urls = [re.findall(r'href="(.*)">', line)[0] for line in
                re.findall(r'<li class="lastPage">(.*?)</li>', html, re.DOTALL)[0].split('\n')
                if re.search(r'href', line)]
        return urljoin(self.seed_url,urls[0]) if urls else  None


        # < li class ="lastPage"
        # < a href = "ggcx?appCode=H60&channelCode=0102&bz=0&pageSize=10&pageNo=2" > 下一页 < / a >
        # < / li >
        pass

    def currentPage_no(self,html=None):
        html = html if html else self.html
        nos = [re.findall(r"\d+", line)[0] for line in
                re.findall(r'<li class="currentPage">(.*?)</li>', html, re.DOTALL)[0].split('\n') if
                re.search(r"\d+", line)]
        return nos[0] if nos else  None


    def pageNo(self,url=None):
        url = url if url else self.seed_url
        no = re.findall(r"pageNo=(\d+)", url)
        if no:
            return no[0]
        else:
            return None
        pass

    def __call__(self,log_url=None,root=None):
        try:
            tmp = self.lastPager_url()
            crawler = GetPagerUrl(tmp)
            firstPage, nextPage, lastPage = crawler.firstPager_url(), crawler.nextPager_url(), crawler.lastPager_url()
            mainUrl = log_url if log_url else firstPage
            nroot = 0
            while True:
                nroot += 1
                crawler = GetPagerUrl(mainUrl)
                no = crawler.currentPage_no()
                yield no,crawler.subpaer_urls()
                mainUrl = crawler.nextPager_url()
                pass
                if mainUrl == lastPage or mainUrl == nextPage:
                    pageLog[str(no)] = mainUrl
                    break
                if nroot == root:
                    pageLog[str(no)] = mainUrl
                    break
            pass
        except Exception as e:
            no = crawler.pageNo(mainUrl)
            pageLog[str(no)] = mainUrl
            pass
        return



        pass

if __name__ == "__main__":
    # pageShe.close()
    seed_url = 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102'
    url580 = 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102&bz=0&pageSize=10&pageNo=598'
    url4 = 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102&bz=0&pageSize=16&pageNo=4'
    url7 = 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102&bz=0&pageSize=10&pageNo=7'
    url12 = 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102&bz=0&pageSize=20&pageNo=12'
    url19 = 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102&bz=0&pageSize=10&pageNo=19'

    crawlPager = GetPagerUrl(seed_url=seed_url)
    # crawlPager2 = GetPagerUrl(seed_url=url7)
    # print crawlPager2.currentPage_no(),crawlPager2.html
    for no,urls in crawlPager(url19):
        print no
        for url in urls:
            print url
    GetPagerUrl.pageShe.close()
    pass