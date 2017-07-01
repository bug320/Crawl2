# -*- coding:utf-8 -*-
import shelve
import html2text
import re
import newspaper
from bs4 import BeautifulSoup
from const_var import  *
import downloader
import xlrd
download = downloader.Downloader()
xunlian = shelve.open("html_to_txt/zhang_suburl.she/cache.she", "c")
zhang = [1,2,7,12,13,16]
liu = [4,6,7,9,10,11,12,13,14,17,18,20,21,22,27,30,32,34,35,36,37,38]

feilds=[u'项目名称',u'采购编号',u'采购单位',u'招标公告发布日期', u'评标日期',u'中标公告发布日期',u'中标单位',u'中标金额']
ncol = 8


# def trySearch():
#     partter=""
#     string =u'成交人：河南威帆信息技术股份有限公司 \n 中标人: 河南中裕广恒科技股份有限公司'
#     for line in string.split('\n'):
#         if re.search(ur'成交人|中标人|', line):
#             print line,
#
#     pass
#

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




# 读取一张表格,获得所有标准字段的别名,并生成用于 re.search() 的 正则表达式
class FormatHtml(object):
    def __init__(self,name_fields):
        # self.url = url
        self.name_fields = name_fields[:] # 标准字段
        self.bynames = dict(zip(self.name_fields, self.name_fields))  # 标注字段对应别名的 re 表达式,以标准字段为 key 值
        pass
    def setBynameFromExcel(self,excel):
        data = xlrd.open_workbook(excel)
        table = data.sheets()[0]
        for col in xrange(ncol):
            # if count != 2 :continue
            bynames = table.col_values(col+1)[1:]
            self.setByname(bynames[0], filter(lambda x: x != u'', bynames[1:]))
            pass
        pass
    def setByname(self, name, byname):
        for bn in (byname):
            if bn == u'' : continue
            if name not in self.name_fields:
                pass
            else:
                self.bynames[name] += u'|%s' % bn
                # print self.bynames[name]
                pass
            pass
        pass
    def getByNameField(self):
        return self.bynames
        pass
    def getNameFromByName(self,byname):
        if byname.find('|'):
            return byname.split('|')[0]
            pass
        else:
            return byname
            pass
        pass
    pass
class StructHtml(object):
    def __init__(self,fh):
        self.fh = fh
        # self.html = html
        self.format_txt = ""
        pass

    def struct_format(self,fmat, line):
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
    def struct_html(self,html):
        tmpTxt = u''
        for line in html.split('\n'):
            for name ,byname in fh.bynames.iteritems():
                if re.search(byname,line):
                    if re.search(ur"地址|领取|通知书", line):
                        pass
                    # elif re.search(ur'[:：]\n', line):
                    #     pass
                    else:
                        tmpTxt += u"%s:%s\n" % (name,self.struct_format(byname, line))
                        pass
                    pass
            pass
        return self.filed_get_once(tmpTxt)
        pass

    def filed_get_once(self,txt):
        fd_set = feilds[:]
        tmp = u''
        for fd in fd_set:
            i = txt.find(fd)
            if i != -1:
                j = txt.find('\n', i)
                tmp += "%s\n" % txt[int(i):int(j)]
                pass
            else:
                tmp += "%s:null\n" % fd
            pass
        return tmp
        pass
    def html_to_txt(self,html):
        h = html2text.HTML2Text()
        h.ignore_links = True
        return h.handle(html)
        pass

    def getSruct(self,text,html):
        # for i, v in xunlian.iteritems():
        #     # print type(v)
        #     url = getInnerPageURLs(v)[0]
        #     url = "%s%s" % (mainHTTP, url)
        #     art = newspaper.Article(url, language='zh')
        #     art.download()
        #     art.parse()
        if text == "" or text == None:
            d = self.html_to_txt(html)
        else:
            d = text
        html_txt = re.sub("[+\.\!\_,$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）]+".decode("utf8"), " ".decode("utf8"), d)
        print "==============================  ", v
        txt = self.struct_html(html_txt)
        self.format_txt = txt
        print self.format_txt
        pass


    pass






if __name__ == "__main__":

    fh = FormatHtml(name_fields=feilds)
    fh.setBynameFromExcel('ex001.xlsx')
    sh = StructHtml(fh)
    for i, v in xunlian.iteritems():
        # print type(v)
        url = getInnerPageURLs(v)[0]
        url = "%s%s" % (mainHTTP, url)
        art = newspaper.Article(url, language='zh')
        art.download()
        art.parse()
        sh.getSruct(art.text,art.html)
    pass