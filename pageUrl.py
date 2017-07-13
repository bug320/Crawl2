# -*- coding:utf -*-
import downloader
import urlparse
# import shelve
import re
import Cache
HTML_CACHE = Cache.Cache()
# HTML_CACHE['id'] = 'HTML'
sub_path = 'html_cache/page_cache/subpage_she.she'
page_path = 'html_cache/page_cache/page_she.she'

Download = downloader.Downloader()


def page_no(url):
    return re.findall(r'pageNo=(\d+)',url)
    pass
class PageCrawl(object):
    def __init__(self,seed_url,template):
        self.html =""
        self.seed_url =seed_url
        self.template =template
        # self.cache = None
        pass
    def download(self,url,cache=HTML_CACHE):
        if cache == None:
            self.html = Download(url)
            # print "Download without Cache..."
            pass
        else:
            if cache[url] == None:
                self.html = Download(url)
                cache[url] = self.html
                # print "Save into Cache..."
                pass
            else:
                self.html =  cache[url]
                # print "Get from Cache..."
                pass
            pass
        return self.html
        pass

    def get_pre_url(self,html):
        html = html if html else self.html
        urls = [re.findall(r'href="(.*)">', line)[0] for line in
                re.findall(r'<li class="prePage">(.*?)</li>', html, re.DOTALL)[0].split('\n')
                if re.search(r'href', line)]
        return urlparse.urljoin(self.seed_url, urls[0]) if urls else  None
        pass

    def get_last_url(self,html):
        html = html if html else self.html
        urls = [re.findall(r'href="(.*)">', line)[0] for line in
                re.findall(r'<li class="lastPage">(.*?)</li>', html, re.DOTALL)[0].split('\n')
                if re.search(r'href', line)]
        return urlparse.urljoin(self.seed_url, urls[0]) if urls else  None
        pass

    def get_sub_urls(self):
        # try:
        if True:
            for i, url in enumerate(self.get_page_urls()):
                print "download %s.. " % (i+1)
                html = self.download(url)
                # cache.sync()
                urls = [re.findall(r'href="(.*)">', line)[0] for line in
                        re.findall(r'<div class="List2">(.*?)</div>', html, re.DOTALL)[0].split('\n')
                        if re.search(r'href', line)]
                # urls = []
                # if sub_she:sub_she[str(i + 1)] = urls;sub_she.sync()
                yield [urlparse.urljoin(self.seed_url, url) for url in urls]
                # return [1]
                pass
            else:
                # if sub_she:
                #     sub_she.sync()
                #     sub_she.close()
                #     pass
                pass
            pass
        # except Exception as e:
        #     print "get_sub_urls:e:",e
        #     pass
        # finally:
        #     # if cache:
        #     #     cache.sync()
        #     #     cache.close()
        #     pass
        pass

    def get_page_urls(self,template=None):
        # return [1,2,3]
        template = template if template else self.template
        # try:
        if True:
            url = self.get_last_url(self.download(self.seed_url,cache=None))
            url = self.get_pre_url(self.download(url,cache=None))
            tmp = page_no(url)

            if tmp:
                last_page_no = int(tmp[0]) +1
                return [template + str(u + 1) for u in xrange(last_page_no)]
            else:
                print "None"
                return []
            pass
        # except Exception as e:
        #     print "get_page_urls",e
        #     return []
        #     pass
        pass
    pass

if __name__ == '__main__':
    seed_url = 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102'
    pageTemp = 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102&bz=0&pageSize=10&pageNo='
    crawler = PageCrawl(seed_url,pageTemp)
    for i,u in enumerate(crawler.get_sub_urls()):
        print i
        for url in u:
            print url
            crawler.download(url)
        # break
    print len(HTML_CACHE)
    # # # # HTML_CACHE.sync()
    # # # for i,v in HTML_CACHE.iteritems():
    # # #     print i,v
    # # pass
    # # # HTML_CACHE = Cache.Cache()
    # print "OK"
    # HTML_CACHE['url'] = '\'\''
    # if HTML_CACHE:
    #     print "True"
    # else:
    #     print "False"
    # print len(HTML_CACHE)
    # crawler = PageCrawl(seed_url, pageTemp)
    # CH = Cache.Cache()
    # for i in crawler.get_page_urls():
    #     html = crawler.download(i,cache=None)
    #     # print html
    #     #   CH[id] = html
    #     break
    #     pass
    #
    # for k,v in HTML_CACHE.iteritems():
    #     print k
    #     print v
    #     del HTML_CACHE[k]

    # print not HTML_CACHE == None

    pass