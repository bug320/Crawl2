# -*- coding:utf-8 -*-
import shelve
import html2text
import re
import newspaper
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
from const_var import  *
import downloader
import urlparse
download = downloader.Downloader()
xunlian = shelve.open("html_to_txt/zhang_suburl.she/cache.she", "c")
zhang = [1,2,7,12,13,16]
liu = [4,6,7,9,10,11,12,13,14,17,18,20,21,22,27,30,32,34,35,36,37,38]

feilds=[u'项目名称',u'采购编号',u'采购单位',u'招标公告发布日期', u'评标日期',u'中标公告发布日期',u'中标单位',u'中标金额']

def format_feild(uFild):
    if uFild== u'项目名称|招标项目名称' or uFild == u'项目名称' or uFild == u'招标项目名称':
        return u'项目名称'
        pass
    elif uFild== u'采购编号|招标编号|标书编号' or uFild == u'采购编号'or uFild == u'招标编号':
        return u'采购编号'
        pass
    elif uFild== u'采购单位|采购人名称|招标人|采购人' or uFild == u'采购单位' or uFild == u'采购人名称' or uFild == u'招标人' :
        return u'采购单位'
        pass
    elif uFild== u'招标公告发布日期|招标公告发出日期' or uFild == u'招标公告发布日期'or uFild == u'招标公告发出日期':
        return u'招标公告发布日期'
        pass
    elif uFild== u'评标日期' or uFild == u'评标日期':
        return u'评标日期'
        pass
    elif uFild== u"中标公告发布日期" or uFild == u'中标公告发布日期':
        return u'中标公告发布日期'
        pass
    elif uFild== u'中标单位|中标人|成交人' or uFild == u'中标单位'or uFild == u'中标人' or uFild == u'成交人':
        return u'中标单位'
        pass
    elif uFild== u'中标金额|成交总价|中标总价|投标总价|中标价|中标单价|成交金额' or uFild == u'中标金额'or uFild == u'成交总价'or uFild == u'中标总价'or uFild == u'投标总价':
        return u'中标金额'
        pass
    else:
        return None
        pass
    pass

def get_field(uFild):

    if uFild == u'项目名称':
        return u'项目名称|招标项目名称'
        pass
    elif uFild == u'采购编号':
        return u'采购编号|招标编号|标书编号'
        pass
    elif uFild == u'采购单位':
        return u'采购单位|采购人名称|招标人|采购人'
        pass
    elif uFild == u'招标公告发布日期':
        return u'招标公告发布日期|招标公告发出日期'
        pass
    elif uFild == u'评标日期':
        return u'评标日期'
        pass
    elif uFild == u'中标公告发布日期':
        return u'中标公告发布日期'
        pass
    elif uFild == u'中标单位':
        return u'中标单位|中标人|成交人'
        pass
    elif uFild == u'中标金额':
        return u'中标金额|成交总价|中标总价|投标总价|中标价|中标单价|成交金额'
        pass
    else:
        return None
        pass
    pass

    pass


def struct_html(html):
    tmpTxt = u''
    for line in html.split('\n'):
        for ufield in feilds:
            patter =get_field(ufield)
            if re.search(patter,line):
                if re.search(ur"地址|领取|通知书",line): pass
                # else:print line
                else:
                    tmpTxt += u"%s:%s\n" % (format_feild(patter),struct_format(patter,line))
                    txt = filed_get_once(tmpTxt)
                    # print txt
            pass
        pass
    return txt[:]
    pass

def struct_format(fmat,line):
    if line.find(u'：'):
        k = line.split(u'：')
        k = k[-1]
    elif line.find(u":"):
        k = line.split(u':')
        k = k[-1]
    else:
        k = line
    return k
    # k = re.findall(patter,line)
    # print k
    pass


def trySearch():
    partter=""
    string =u'成交人：河南威帆信息技术股份有限公司 \n 中标人: 河南中裕广恒科技股份有限公司'
    for line in string.split('\n'):
        if re.search(ur'成交人|中标人|', line):
            print line,

    pass


def getInnerPageURLs(url):
    links = []
    try:
        soup = BeautifulSoup(download(url),HTMLPARSER)
    except Exception as e:
        print "getInnerPageURLs():",e
        return None
    pass
    for string in soup.stripped_strings:
        # dammit = UnicodeDammit(string)
        # tmpurl = endUrlCmp.findall(dammit.unicode_markup)
        tmpurl = endUrlCmp.findall(string.encode('utf-8'))

        if tmpurl != [] and tmpurl not in links:
            links.append(tmpurl[0])
    # if DEFAULT_CRAWLER_ECHO: print "get inner html :", links
    return links

def run_txt():
    for i, v in xunlian.iteritems():
        # print type(v)
        url = getInnerPageURLs(v)[0]
        url = "%s%s" % (mainHTTP, url)
        art = newspaper.Article(url, language='zh')
        art.download()
        art.parse()
        if art.text == "" or art.text == None:
            d = html_to_txt(art.html)
        else:
            d = art.text[:]
        html_txt = re.sub("[+\.\!\_,$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）]+".decode("utf8"), " ".decode("utf8"), d)
        print "==============================  ", v
        txt = struct_html(html_txt)
        print txt
        # filed_get_once(txt)
        # break

        # print art.text[:]
        pass
    print "OK"
    pass

def filed_get_once(txt):
    fd_set = feilds[:]
    tmp =u''
    for fd in fd_set:
        i = txt.find(fd)
        if i !=-1:
            j = txt.find('\n',i)
            tmp += "%s\n" % txt[int(i):int(j)]
            pass
        else:
            tmp += "%s:null\n" % fd
        pass
    return tmp
    pass

def html_to_txt(html):
    h = html2text.HTML2Text()
    h.ignore_links = True
    return h.handle(html)
    pass

if __name__ == "__main__":
    run_txt()
    pass
    # v= 'http://www.hngp.gov.cn/henan/content?infoId=1494846098506930&channelCode=H610102&bz=0'
    # url = getInnerPageURLs(v)[0]
    # url = "%s%s" % (mainHTTP, url)
    # art = newspaper.Article(url, language='zh')
    # art.download()
    # art.parse()
    # if art.text == "" or art.text ==None:
    #     d = html_to_txt(art.html)
    # else:
    #     d = art.text
    # html_txt = re.sub("[+\.\!\/_,$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）]+".decode("utf8"), " ".decode("utf8"), d)
    # print "==============================  ", v
    # struct_html(html_txt)
    #
    # # print art.text[:]
    # # pass
    # pass