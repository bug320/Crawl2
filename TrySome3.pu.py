# -*- coding:utf-8 -*-
from  const_var import *
import downloader
import html2text
from bs4 import UnicodeDammit
def html_to_txt(html):
    h = html2text.HTML2Text()
    h.ignore_links = True
    return h.handle(html)
    pass

# ---|---|---|---
if __name__ == '__main__':
    url = "/webfile/jiaozuo/cgxx/jggg/webinfo/2017/07/1498553692194150.htm"
    # url = "/webfile/luoyang/zgxx/jggg/webinfo/2017/07/1498553690093831.htm"
    url = "%s%s" % (mainHTTP, url)
    html = downloader.Downloader()(url)
    dommit = UnicodeDammit(html)
    text = html_to_txt(dommit.unicode_markup)
    if re.search(r'-+\|+',text,re.DOTALL):
        print True
    # print text11
