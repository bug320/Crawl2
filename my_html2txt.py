# -*- coding:utf-8 -*-
from const_var import  *
from bs4 import BeautifulSoup
import newspaper
from newspaper import Article
import shelve
import happybase
from dbs import save_to_db
from scrapely import Scraper
"""
z1,z2,z7,z12,z13,z16,
l10, l11, l12, l13, l14, l17, l18, l20, l21, l22, l27, l30, 
                                        l32, l34, l35, l36, l37, l38,l4, l6, l7,l9
                                        
"""

zhang = [1,2,7,12,13,16]
liu = [4,6,7,9,10,11,12,13,14,17,18,20,21,22,27,30,32,34,35,36,37,38]
# 标号-1才是正确的
hdb=save_to_db.MyHbase(HBASE_TABLE)

def GetTheURls():
    a_liu = []
    a_zhang = []
    html_liu = 'html_to_txt/liu.html'
    html_zhang = 'html_to_txt/zhang.html'
    html_liu = BeautifulSoup(open(html_liu), HTMLPARSER)
    html_zhang = BeautifulSoup(open(html_zhang), HTMLPARSER)
    for i in html_liu.find_all('a'):
        a_liu.append(i["href"].encode("utf-8"))
    for z in html_zhang.find_all('a'):
        a_zhang.append(z["href"].encode("utf-8"))

    she_zhang = shelve.open("html_to_txt/zhang_suburl.she/cache.she", "c")
    for id in (zhang):
        print a_zhang[id - 1]
        she_zhang[str(id)] = a_zhang[id - 1]
    she_zhang.close()

    she_liu = shelve.open("html_to_txt/liu_suburl.she/cache.she", "c")
    for id in (liu):
        print a_liu[id - 1]
        she_liu[str(id)] = a_liu[id - 1]
    she_liu.close()

    print len(liu) + len(zhang)
    pass

xunlian = shelve.open("html_to_txt/liu_suburl.she/cache.she", "c")



# if __name__ =="__main__":
#     s = Scraper()
#     data = {u"招标编号":u"郑财竞谈-2017-121号",
#             u"招标项目名称":u"郑州市招生考试办公室高考所需身份验证终端采购项目",
#             u"招标公告发出日期":u"2017年5月12日",
#             u"评标日期":u"2017年5月18日",
#             u"成交人":u"河南省高校新技术有限公司",
#             u"成交总价":u"730000元人民币",
#             u"采购单位":u"河南招标采购服务有限公司",
#             u"":u"",}
#     s.train("",)
#     pass

def grep(d):
    import re
    import string
    # from zhon.hanzi import punctuation
    string = re.sub("、", " ", d)
    string = re.sub("：", " ", string)
    for i, t in enumerate(string.split('\n')):
        if re.search(u'项目名称'.encode('utf-8'), t):
            print i,
            print t
            pass
        elif re.search(u'采购编号'.encode('utf-8'), t) or re.search(u'招标编号'.encode('utf-8'), t):
            print i,
            print t
            pass
        elif re.search(u'采购单位'.encode('utf-8'), t) or re.search(u'代理机构名称'.encode('utf-8'), t):
            print i,
            print t
            pass
        elif re.search(u'评标日期'.encode('utf-8'), t):
            print i,
            print t
            pass
        elif re.search(u'招标公告发布日期'.encode('utf-8'), t) or re.search(u'招标公告发出日期'.encode('utf-8'), t):
            print i,
            print t
            pass
        elif re.search(u'中标公告发布日期'.encode('utf-8'), t):
            print i,
            print t
            pass
        elif re.search(u'中标单位'.encode('utf-8'), t) or re.search(u'成交人'.encode('utf-8'), t):
            print i,
            print t
            pass
        elif re.search(u'中标金额'.encode('utf-8'), t) or re.search(u'成交总价'.encode('utf-8'), t):
            print i,
            print t
            pass
        else:
            pass
    pass
if __name__ =="__main__":
    count = 0
    for id in liu:
        id-=1
        count += 0
        # if count ==2 :continue
        for i,d in hdb.table.row("liu%s"%id).iteritems():
            # print i
            grep(d)
            pass

        print "===================================================="
        pass
    pass

# #save to hbase
# if __name__ =="__main__":
#     she_zhang = shelve.open("html_to_txt/zhang_suburl.she/cache.she", "r")
#     # she_liu = shelve.open("html_to_txt/liu_suburl.she/cache.she", "r")
#     for k,v in she_zhang.iteritems():
#         print k,v
#         art = Article(v)
#         art.download()
#         # print art.html
#         sub =  endUrlCmp.findall(art.html)[0]
#         url = "%s%s" % (mainHTTP,sub)
#         # xunlian = shelve.open("html_to_txt/liu_suburl.she/cache.she", "c")
#         a = Article(url, language='zh')
#         a.download()
#         a.parse()
#         print a.text
#         hdb.table.put("zhang%s" % k,{"page:txt2":"%s"%a.text})
#         #hdb.table.put("liu%s" % k,{"page:txt2":"%s"%a.text})
#         # break
#     # she_liu.close()f
#     she_zhang.close()
#     # url = 'http://www.hngp.gov.cn/webfile/zhengzhou/cgxx/jggg/webinfo/2017/05/1494846014710819.htm'

    pass


# from scrapely import Scraper
#
# if __name__ == "__main__":
#     s = Scraper()
#     url = 'http://www.hngp.gov.cn/webfile/nanyang/cgxx/jggg/webinfo/2017/06/1498177906630072.htm'
#     data = {u'项目名称':u'新野县第一、三高级中学配备多功能教学一体机设备采购项目',u'项目编号':u"XYGGZY-2017-102"}
#     s.train(url,data)
#     url2 = 'http://www.hngp.gov.cn/webfile/zhengzhou/cgxx/jggg/webinfo/2017/06/1498177906695206.htm'
#     # for i,v in s.scrape(url)[0]:
#     #     print i,v
#     #     pass
#     data = s.scrape(url2)[0]
#     for k,v in data.iteritems():
#         print k,data[k][0]
#     print "Ok"
#
#     pass

# import newspaper
# from newspaper import Article
# if __name__ == '__main__':
#     # newspaper.languages()
#     url ='http://www.hngp.gov.cn/webfile/nanyang/cgxx/jggg/webinfo/2017/06/1498177906630072.htm'
#     a = Article(url, language='zh')  # Chinese
#     a.download()
#     a.parse()
#     # print a.text[:]
#     # print a.title
#     # for i,t in enumerate(a.text.split('\n')):
#     #     print i, "--",t
#     print a.text
#     pass

