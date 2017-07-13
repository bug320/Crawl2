# -*- coding:utf-8 -*-
# from GetPagerUrl import pageLog,pageShe
import re
import shelve
import downloader
import GetPagerUrl
from urlparse import urljoin
pageShe = shelve.open('html_cache/page_cache/page.she', "c")
pageLog = shelve.open('html_cache/page_cache/page_log.she',"c")

subpageShe = shelve.open('html_cache/subpage_cache/subpage.she',"c")
subpageLog = shelve.open('html_cache/subpage_cache/subpage_log.she',"c")

def subpaer_urls(seed_url):
    html = downloader.Downloader(cache=pageShe)
    urls = [re.findall(r'href="(.*)">', line)[0] for line in
            re.findall(r'<div class="List2">(.*?)</div>', html, re.DOTALL)[0].split('\n')
            if re.search(r'href', line)]
    return [urljoin(seed_url, url) for url in urls]
    pass

def page_no(url):
    return re.findall(r'pageNo=(\d+)',url)
    pass

def page_urls(seed_url,template,last_page_no=None):
    # try:
    if True:
        if not last_page_no:
            crawler = GetPagerUrl.GetPagerUrl(seed_url)
            url = crawler.lastPager_url()
            crawler = GetPagerUrl.GetPagerUrl(url)
            url = crawler.prePager_url()
            last_page_no = int(page_no(url)[0]) + 2
            pass
        pass
    # except Exception as e:
    #     print "page_urls",e
    #     return []
    #     pass
    return [template + str(i) for i in xrange(last_page_no)]
    pass


if __name__ == '__main__':
    # try:
    if True:
        seed_url = 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102'
        pageTemp = 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102&bz=0&pageSize=10&pageNo='
        for i,url in enumerate(page_urls(seed_url, pageTemp)):
            crawl = GetPagerUrl.GetPagerUrl(url)
            sub_urls= crawl.subpaer_urls()
            # subpageShe[str(i)] = sub_urls
            print sub_urls
            pass
        else:
            pageLog[str(i)] = url
        pass
    # except Exception as e:
    #     # pageLog[str(i)] = url
    #     print e
    #     pass


    # pageTemp = 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102&bz=0&pageSize=10&pageNo='
    # no = [pageTemp+str(i) for i in xrange(601)]
    # for n in no:
    #     print n
    pass

