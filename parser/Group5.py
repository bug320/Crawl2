# -*- coding:utf-8 -*-
import downloader
import subUrl
# import Cache
import re
import html2text
# import newspaper
from bs4 import UnicodeDammit

#space = ''

from Group4 import  *

def xtext():
    fl = "thrid_group.txt"
    # 出错　http://www.hngp.gov.cn/henan/content?infoId=1498177911426372&channelCode=H760602&bz=0
    g4 = Group4(fl)
    cA = set()
    for i in g4.general()[1:]: # i是ＵＲＬ
        crawler = subUrl.SubCrawl(i)
        idict = crawler.getBaseInfo().next()
        iurl = idict[u"动态链接"]
        html = crawler.download(iurl)
        if isinstance(html, str):
            dommit = UnicodeDammit(html)
            html = dommit.unicode_markup
        text = html2text.html2text(html)
        ###
        # ur"～！＠＃￥％……＆×（）——＋｛｝｜：“《》？｀－＝【】、；‘，。／" 中文
        data = ur""
        newtext = ''
        for  line in text.split('\n')[1:]:
            if line == u'\n' or line == u'' or line == None or line == '\n' or line == '': continue
            if line.find(u'如下') != -1: continue
            # if re.search(ur"")
            # line = " ".join(filter(lambda x: x, line.split(' ')))
            line = line.replace(" ", '')
            line = line.replace(u"　", '')
            line = re.sub(ur"[～！＠＃￥％……＆×——＋｛｝｜：“？｀－＝【】；‘，。／]", " ", line)
            line = re.sub(ur"[\~\!\#\$\%\^\&\*\_\+\{\}\|\:\"\<\>\?\`\=\[\]\\\;\'\,\/]", " ", line)
            # line = re.sub(ur"[\d一二三四五六七八九十].?、", " ", line)
            # line = line.replaceAll(r"[' ']+"," ")
            line = " ".join(filter(lambda x: x, line.split(' ')))
            line.strip()
            line += '\n'
            newtext += (line)
            pass
        else:
            yield i,newtext
            # print "\n======", i
            # i 是　url
        ####
        pass
    pass

def getFirst(line,re,no):

    pass


if __name__ == '__main__':
    for url,text in xtext():
        for no,line in enumerate(text.split('\n')):
            if line == "\n" or line == u" " or line == " " :continue
            # line += '\n'
            if re.match(r' \n',line):
                continue
            else:
                for i in line.split(' '):
                    print i
                else:
                    print "++++++"
            pass
        else:
            print "===========" ,url
            pass
        pass
    pass