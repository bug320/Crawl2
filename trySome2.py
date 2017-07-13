# -*- coding:utf-8 -^-

import re
test = u"三、发布公告媒体及日期\n媒体日期:2017年6月23日在《安阳市政府采购网》、《河南省政府采购网》、《中国采购与招标网》发布了公告。\n2017年6月23日发布了公告。\n"

# show_time_one_line = False
show_time_re = [ur"媒体",ur"时间|日期|期限"]
def isTrue(patters,line):
    for p in patters:
        if re.search(p,line) == None:
            return False
    return True
    pass

def del_show_time(txt,line):
    if len(line) <=0:return None
    snext = txt.find(line)+len(line)+1
    enext = txt[snext:].find(u'\n')
    if enext == -1:return None
    else:enext += snext
    stxt = txt[snext:enext]
    date = re.findall(ur'\d+年\d+月\d+日',stxt)
    if date == [] or date == None :return None
    else:return date[0]
    pass
def isLineOff(line):
    sline = line +'\n'
    # if re.search(ur"日期\n",sline):
    if re.search(ur"[媒体|时间|日期|期限][:：]{0,1}\n",sline):
        return True
    else:return False
    pass

def isOnlyName(patter,line):
    sline = line +'\n'
    # print sline
    p =ur"%s|[:：]{0,1}\n" % patter
    if re.search(p,sline) == None:
        return False
    else:return True
    pass

if __name__ == "__main__":
    # for line in test.split('\n'):
    #     # print line
    #     # if re.search(ur"时间|日期|期限",line)!=None and re.search(ur"媒体",line)!=None:
    #     if isTrue(show_time_re,line):
    #     # if True:
    #         if isLineOff(line):
    #             # print line
    #             print u"招标公告发布日期:%s\n" % del_show_time(test,line)
    #
    #     pass
    pa =ur"时间|日期|期限"
    line = "时间:d"
    print isOnlyName(pa,line)
    print ur"%s|[:：]{0,1}\n" % show_time_re[1]
    pass