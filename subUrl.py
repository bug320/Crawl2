# -*- coding:utf-8 -*-
import re
import Cache
import pageUrl
import downloader
import html2text
import newspaper
from bs4 import UnicodeDammit
HTML_CACHE = Cache.Cache()
Download = downloader.Downloader()
mainHTTP = "http://www.hngp.gov.cn"
def xsub_urls():
    seed_url = 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102'
    pageTemp = 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102&bz=0&pageSize=10&pageNo='
    crawler = pageUrl.PageCrawl(seed_url, pageTemp)
    for i, u in enumerate(crawler.get_sub_urls()):
        yield u
    pass

"""

<div class="BorderEEE BorderRedTop" style="min-height:400px;">
        <h1 class="TxtCenter Padding10 BorderEEEBottom Top5">周口市城市管理局污泥临时堆放场建设项目竞争性谈判中标公示</h1>

        <div class="TxtRight Padding5">发布机构：<span class="Blue">周口市政府采购中心</span> &nbsp;&nbsp;发布人：<span
                class="Blue">采购中心</span>&nbsp;&nbsp;发布日期：
            <span class="Blue">2017-07-04 14:41</span>&nbsp;&nbsp;访问次数：<span
                    class="Blue">26</span>
        </div>

        <div class="Content BorderTopDot" id="watermarklogo">

            <div id="content"></div>
        </div>
    </div>

"""

class SubCrawl(object):
    def __init__(self,url):
        self.url = url
        self.html = self.download(self.url)
        pass

    def download(self, url, cache=HTML_CACHE):
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
                self.html = cache[url]
                # print "Get from Cache..."
                pass
            pass
        return self.html
        pass

    def getBaseInfo(self):
        # patter = ur' <div class="BorderEEE BorderRedTop" style="min-height:400px;">(.*？)<div class="Content BorderTopDot" id="watermarklogo">'
        patter = r'<div class="TxtRight Padding5">(.*?)</div>'
        info = re.findall(patter,self.html,re.DOTALL)
        info = info[0] if info else None
        """
        发布机构：<span class="Blue">周口市政府采购中心</span> &nbsp;&nbsp;发布人：<span
                class="Blue">采购中心</span>&nbsp;&nbsp;发布日期：
            <span class="Blue">2017-07-04 14:41</span>&nbsp;&nbsp;访问次数：<span
                    class="Blue">26</span>
                    
        发布机构 发布人 发布日期 访问次数
        """
        # (*.?) <span class="Blue"> (.*?) </span>
        patter = r'(.*?)<span.*?>(.*?)</span.*?>'
        # for line in info.split('\n'):
        #     print line,"|"
        # print type(info)
        # infos = re.findall(patter,info.encode('utf-8'),re.DOTALL)
        keys= [u"发布机构",u"发布人",u"发布日期",u"访问次数",u"动态链接"]
        values = []
        for i,v in re.findall(patter,info,re.DOTALL):
            values.append(v)
        v = re.findall(r'\$\.get\(\"(.*\.htm)',self.html)[0]
        # urlparse.urljoin(self.url,v)
        v = u"%s%s" % (mainHTTP,v)
        values.append(v)
        # print v
        yield dict(zip(keys,values))

        pass
    pageUrl

class InnerCrawl(object):
    def __init__(self,url):
        self.url = url
        self.art = newspaper.Article(self.url, language='zh')
        self.art.download()
        self.html = self.art.html
        self.praser()
        self.text = self.art.text
        if self.text =="" or self.text == None:
            self.praser()
        pass

    def download(self, url, cache=HTML_CACHE):
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
                self.html = cache[url]
                # print "Get from Cache..."
                pass
            pass
        return self.html
        pass
    def praser(self):
        self.text = self.html_to_txt(self.html)
        print "Prase by myself"
        pass

    def html_to_txt(self,html):
        h = html2text.HTML2Text()
        h.ignore_links = True
        return h.handle(html)
        # self.text = Document(self.html)
        pass
    pass

def showClass(htm_cls):
    print "废标"
    for i in htm_cls[0]:
        print i
    print "================"
    print "有包"
    for i in htm_cls[1]:
        print i
    print "================"
    print "带表格"
    for i in htm_cls[2]:
        print i
    print "================"
    print "单一"
    for i in htm_cls[3]:
        print i
    print "================"
    pass

if __name__ == '__main__':
    patter = ur'[一][.｜ |、]{0,1}(.*?)[：|:|\n]'
    html_class=[[0],[1],[2],[3]] # 0,废标　１,有包　２,带表格 ３　单一　
    feibiao_patter = ur"废标|流标|取消|采购失败"
    group_patter = ur"[包\d?|阶段|标段|项目A][\d+|:|：|\n|一]"
    has_table = r'TD|td'

    for urls in xsub_urls():
        for url in urls:
            # print "==============", url
            crawler = SubCrawl(url)
            for idict in  crawler.getBaseInfo():
                iurl = idict[u"动态链接"]
                icrawler = InnerCrawl(iurl)
                if re.search(has_table,icrawler.html,re.DOTALL):
                    # 带表格
                    html_class[2].append(crawler.url)
                    # continue  # 暂时不做处理,以后把转成文本　存到　.text 中就可以把这句注释掉
                    pass
                if re.search(feibiao_patter, icrawler.text, re.DOTALL):
                    # 废标
                    html_class[0].append(crawler.url)
                    pass
                elif re.search(group_patter, icrawler.text, re.DOTALL):
                    # 有包
                    html_class[1].append(crawler.url)
                    pass
                    pass
                else:
                    # 单一
                    html_class[3].append(crawler.url)
                    pass

                # break
                pass
            # break
            pass
        # break
        pass
    showClass(html_class)
    pass


    # for urls in xsub_urls():
    #     for url in urls:
    #         print "==============", url
    #         crawler = SubCrawl(url)
    #         for idict in  crawler.getBaseInfo():
    #             iurl = idict[u"动态链接"]
    #             icrawler = InnerCrawl(iurl)
    #             rf = re.findall(patter,icrawler.text)
    #
    #             for i,t in enumerate(rf):
    #                 print i,t
    #                 pass
    #             if re.search(ur"废标|流标|取消",icrawler.text):
    #                 print "废标"
    #                 pass
    #             else:
    #                 # print "==============", url
    #                 # print icrawler.text[:200]
    #                 print None
    #
    #             # break
    #             pass
    #         # break
    #         pass
    #     # break
    #     pass