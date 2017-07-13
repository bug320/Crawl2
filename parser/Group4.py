# -*- coding:utf-8 -*-
import downloader
import subUrl
# import Cache
import re
import html2text
# import newspaper
from bs4 import UnicodeDammit

# re.compile("<P.*?>(.*)</P>",re.S).findall(page)
# resulst = re.sub('<.*?>|&nbsp;|&yen;','',string[0])

class Group4(object):
    def __init__(self,gorupFile):
        self.goup = []
        with open(gorupFile) as file:
            for line in file.readlines():
                if line == "0\n":
                    self.goup.append([line])
                    no = 0
                    pass
                elif line == '1\n':
                    self.goup.append([line])
                    no = 1
                    # print line
                    pass
                elif line == '2\n':
                    self.goup.append([line])
                    no = 2
                    pass
                elif line == '3\n':
                    self.goup.append([line])
                    no = 3
                    pass
                else:
                    if re.search("http", line):
                        self.goup[no].append(line.split("\n")[0])
                    pass
                pass
            pass

        pass
    def has_feibiao(self):
        # 废标
        return self.goup[0]
        pass
    def has_packed(self):
        return self.goup[1]
        # 带有包
        pass

    def has_table(self):
        # 表格带有
        return self.goup[2]
        pass
    def general(self):
        # 一般格式
        return self.goup[3]
        pass
    pass

if __name__ == '__main__':
    fl = "thrid_group.txt"
    g4 = Group4(fl)
    # for i in g4.has_feibiao():
    #     print i
    #     pass
    cA = set()
    for i in g4.general()[1:]:
        crawler = subUrl.SubCrawl(i)
        idict = crawler.getBaseInfo().next()
        iurl = idict[u"动态链接"]
        html = crawler.download(iurl)
        if isinstance(html,str):
            dommit = UnicodeDammit(html)
            html = dommit.unicode_markup
        text = html2text.html2text(html)
        # print text
        # print i
        # break
        # if len > 10:
        # print text
        # for ii in re.findall(ur"[一二三四五六七八九十][一二三四五六七八九]*[、:：\.\u3000\xa0\*](.*?)[\n:：\u3000\xa0\*]",text):
        #     print ii
        # else:
        #     print "－－－－－－"
        #     print i

        if True:
            # print "<===========", i
            # for ii in re.findall(ur'^[1一][：:、\.\u3000\xa0\*](.*?)[\n:：\*]',text,re.DOTALL):
            # for ii in re.findall(ur"[一二三四五六七八九十][一二三四五六七八九]?[、:：\.\u3000\xa0\*](.*?)[\n:：\u3000\xa0\*]", text):
            for ii in re.findall(ur"(.*)[:：].*\n", text):
                if len(ii) < 22 and re.search(ur"\D\W",ii) and not re.search(ur"[azAZ]",ii):
                    ii = ii.replace(' ', '')
                    ii = ii.replace(u' ', '')
                    # ii = ii.strip()
                    ii = re.sub(ur'[\s；;\(\)（）\\\d\.\．一二三四五六七八九十、\u3000\xa0\*]','',ii)
                    # ii = ii.strip()
                    d =  ii.find(':')
                    if d == -1 : d =ii.find(u'：')
                    if d != -1 : ii = ii[:d]

                    cA.add(ii)
                    # if ii == u"项目信息":
                    print ii
                    # print "==========>"
            else:
                for ii in re.findall(ur"^[\s\d]\.?[\d]?[:：、\u3000\xa0\*\t]*(.*?)[\n:：\u3000\xa0\*]",text):
                    if len(ii) < 22 and re.search(ur"\D\W", ii) and not re.search(ur"[azAZ]", ii):
                        cA.add(ii)
                        # if ii == u"项目信息":
                        print ii
                else:
                    print "==========>",i
                    pass

            # break
    print len(cA)
    for i in cA:
        print i,"=====",len(i)
        pass
    pass