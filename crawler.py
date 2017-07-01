#-*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import urlparse
from const_var import *
import downloader
import shelve
from  dbs import save_to_db

download=downloader.Downloader()

class Crawler(object):
    def __init__(self,seed_url):
        self.seed_url=seed_url
        self.pshe = shelve.open(PAGER_PATH)
        pass
    def close(self):
        self.pshe.sync()
        self.pshe.close()
        pass
    # 根据 page_url 获取每一页的 subpage_url
    def getEachPageUrls(self,link):
        """
        获取link的所有目的链接,并返该租连接的列表
        :param link: 
        :return: 
        """
        try:
            result = []
            soup = BeautifulSoup(download(link),HTMLPARSER)
            # class ="BorderBlue NoBorderTop Padding5"
            # list2 = soup.find("div", attrs={"class": "BorderBlue NoBorderTop Padding5"}).find("div",attrs={"class": "List2"})
            list2 = soup.find("div",attrs={"class": "List2"})
            for a in list2.find_all('a'):
                suburl = urlparse.urljoin(link, a['href'].encode('utf-8'))
                result.append(suburl)
                # print suburl
            return result
            pass
        except Exception as e:
            print "getEachPageUrls():",e
            return None
            pass
    # 返回全部的  page_url 在一个数组里
    def loop_crawl(self,link=None):
        firstUrl ,nextURl,lastUrl = self.getLimitURLs()
        currentUrl = firstUrl if not link else link

        while True:
            if currentUrl == nextURl or currentUrl == lastUrl:
                if DEFAULT_CRAWLER_ECHO : print "log::",currentUrl
                log_key = pageNo.findall(currentUrl)[0]
                log_she = shelve.open(LOG_PATH,"c")
                log_she[log_key]=currentUrl
                # print type(currentUrl),type(log_key)
                log_she.sync()
                log_she.close()
                break
                pass
            try:
                soup = BeautifulSoup(download(currentUrl),HTMLPARSER)
                pass
            except  Exception as e:
                print "In function Crawler.crawl_loop:",e
                print "log::", currentUrl
                log_key = pageNo.findall(currentUrl)[0]
                log_she = shelve.open(LOG_PATH, "c")
                log_she[log_key] = currentUrl
                # print type(currentUrl),type(log_key)
                log_she.sync()
                log_she.close()
                return
                pass
            else:
                pshe_key=pageNo.findall(currentUrl)[0]
                self.pshe[pshe_key]=(currentUrl,pageNo.findall(currentUrl)[0],self.getEachPageUrls(currentUrl))
                self.pshe.sync()
                yield   pageNo.findall(currentUrl)[0],self.getEachPageUrls(currentUrl)
                currentUrl = self.nextURL(soup)
                # print currentUrl
                pass
            pass
        pass

    def getBaseInfo(self,link):
        attr = [link]  # url,title=0,?,org=2,person=3,post_time=4,check_post=5 ,inner_html_url=6 #2 不知道是啥,添加完后要删掉
        keys = ["url", "title","org", "person", "post_time", "check_post", "inner_html_url"]  # 但是输出时不一定按这个顺序
        # print soup.prettify()
        try:
            soup = BeautifulSoup(download(link), HTMLPARSER)
        except Exception as e:
            print "getBaseInfo :", e
            return None
            pass
        else:
            attr.append(soup.find("h1", attrs={"class": "TxtCenter Padding10 BorderEEEBottom Top5"}).string.encode(
                "utf-8"))  # class="TxtCenters
            # print link
            # print "attr[0]",type(attr[0])
            attr.append(string.string for string in soup.find_all("span", attrs={"class": "Blue"}))
            i = 0
            for zstring in soup.find_all("span", attrs={"class": "Blue"}):
                i += 1
                # if str(type(zstring)) == "<type 'generator'>":
                attr.append(zstring.string.encode("utf-8"))
                # print zstring.string.encode("utf-8")
                # print "atr[%s]"  % i ,
                # print type(attr[i])
                pass
            inner_url = self.getInnerPageURLs(soup)[0][0]
            # print "inner_1",inner_url
            inner_url = inner_url.encode("utf-8")
            # print "inner_1", inner_url
            inner_url = "%s%s" % (mainHTTP, inner_url)
            # print "inner_1", inner_url
            # print "inner_url_log:",inner_url
            del attr[2]  # 执行后 title=0,org=1,person=2,time=3  # 原来的 [2] 不知道是啥
            attr.append(inner_url)
            if len(attr) == 8:
                del attr[2]
                pass
            result = dict(zip(keys, attr))
            return result
            # print "attr[2] = ",attr[2],"type = ",type(attr[2])
            # print attr[-1]
            #
            #
            # print "mov log", len(attr)
            # isi = 0
            # for at in attr:
            #     print isi,
            #     print at
            #     isi += 1
            #
            #
            # print type(result)
            # print result.keys()
            # print result.values()
            # for i in result.keys():
            #     print "key=",i,"value=",result[i]
            # pass
        pass

    def getInnerPageURLs(self,soup):
        links = []
        for string in soup.stripped_strings:
            dammit = UnicodeDammit(string)
            tmpurl = endUrlCmp.findall(dammit.unicode_markup)
            if tmpurl != [] and tmpurl not in links:
                links.append(tmpurl)
        if DEFAULT_CRAWLER_ECHO :print "get inner html :", links
        return links

    def lastURL(self,soup):
        return urlparse.urljoin(self.seed_url,soup.find("li", attrs={"class": "lastPage"}).find("a")["href"].encode("utf-8")) if soup else None
        pass
    def nextURL(self,soup):
        return urlparse.urljoin(self.seed_url,soup.find("li", attrs={"class": "nextPage"}).find("a")["href"].encode("utf-8")) if soup else None
        pass
    def firstURL(self,soup):
        return urlparse.urljoin(self.seed_url,soup.find("li", attrs={"class": "firstPage"}).find("a")["href"].encode("utf-8")) if soup else None
        pass
    def getLimitURLs(self):
        """
        获取为尾页状态下的 首页连接,下一页链接,和尾页链接的 tuple
        :return: (firstUrls,nextUrl,lastUrls)
        """
        try:
            # result =[]
            seed_url = self.seed_url
            download = downloader.Downloader()
            # 下载初始网页找到尾页状态下的：首页,下一页,和尾页的 URL
            soup = BeautifulSoup(download(seed_url), HTMLPARSER)
            # 获取尾页临时尾页
            tmpURL = self.lastURL(soup)
            # 下载临时尾页
            soup = BeautifulSoup(download(tmpURL),HTMLPARSER)
            # 获取尾页状态下的下一页的 url 和 页数
            nextPageUrl = self.nextURL(soup)
            # 获取尾页状态下的首页的 url 和 页数
            firstPageUrl = self.firstURL(soup)
            # 获取尾页状态下的尾页的 url 和 页数
            lastPageURL = soup.find("li", attrs={"class": "lastPage"}).find("a")["href"].encode('utf-8')
            lastPageURL = urlparse.urljoin(seed_url, lastPageURL)
            return (firstPageUrl, nextPageUrl, lastPageURL)
            pass
        except Exception as e:
            print "getPageURLs : %s ",e
            return  (None,None,None)
            pass
        pass
    pass


if __name__ == "__main__":
    seed_url = 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102'
    url580 = 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102&bz=0&pageSize=10&pageNo=598'
    url4 = 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102&bz=0&pageSize=16&pageNo=4'
    crawl = Crawler(seed_url)
    print "PageUrls info:"
    print "count:", len(crawl.pshe)
    for p_no, tuple_ps in crawl.pshe.iteritems():
        print "\tthe Number %s info", p_no
        print "\tpageUrl:", tuple_ps[0]
        print "\tsubpageUrls:"
        count = 0
        for s in tuple_ps[1]:
            count += 1
            print "\t\t%s,%s" % (count, s)
    # seed_url = 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102'
    # url580 = 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102&bz=0&pageSize=10&pageNo=598'
    # url4 = 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102&bz=0&pageSize=16&pageNo=4'
    # crawl = Crawler(seed_url)
    # mdb = save_to_db.MySQL(table=MYSQL_TABLE,db=MYSQL_DBASE,user=MYSQL_USER,passwd=MYSQL_PASSWD,localhost=MYSQL_HOST)
    # 3 "Connect to MySQl success!"
    # hdb = save_to_db.MyHbase(HBASE_TABLE)
    # print "Connect to MySQl success!"
    # # result = crawl.getEachPageUrls(seed_url);
    # # temp = set()
    # # for i,u in enumerate(result):
    # #     print i,u
    # #     temp.add(u)
    # #     pass
    # # print len(temp)
    # try:
    #     for i, u in crawl.loop_crawl(link=None):
    #         print "page:",i,
    #         print  "subpahe:",u
    #         # count = 0
    #         # for url in u:
    #         #     count += 1
    #         #     print count, url, "is being crwal..."
    #         #     result = crawl.getBaseInfo(url)
    #         #     mdb.save(result)
    #         #     for idict in mdb.get():
    #         #         hdb.save(idict)
    #         #         mdb.update(idict["id"])
    #         #         pass
    #         # # break
    #         # pass
    #     else:
    #         print "PageUrls info:"
    #         print "count:",len(crawl.pshe)
    #         for p_no,tuple_ps in crawl.pshe.iteritems():
    #             print "\tthe Number %s info",p_no
    #             print "\tpageUrl:",tuple_ps[0]
    #             print "\tsubpageUrls:"
    #             count = 0
    #             for s in tuple_ps[1]:
    #                 count +=1
    #                 print "\t\t%s,%s" %(count,s)
    #
    #         pass
    #     pass
    #
    # except Exception as e:
    #     print "the end url PageNo", i
    #     print "in main:",e
    #     pass
    # print "the end url PageNo",i
    # mdb.close()
    # print
    # log_she = shelve.open(LOG_PATH, "r")
    # print "after the crawler ,the log url is : "
    # before_i = str(int(i)-1)
    # next_i = str(int(i)+1)
    # for ilog in [before_i,i,next_i]:
    #     if log_she.has_key(ilog):
    #         print ilog,log_she[ilog]
    #         # del log_she[ilog]
    #     else:
    #         print ilog,"None"
    # log_she.close()
    pass