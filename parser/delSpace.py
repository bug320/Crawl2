# -*- coding:utf-8 -*-
import re
if __name__ == '__main__':
    with open("字段名.txt","r") as file:
        aset= set()
        for line  in file.readlines():
            line = line.strip()
            aset.add(re.sub(r"[=\d\n\#]",'',line))
            # print line
            pass
        pass
    icount_name = set()   # 名称
    icount_no = set()     # 编号
    icount_time = set()   # 时间
    icount_org = set()    # 单位
    icount_money = set()  # 金额
    icount_place = set()  # 地点
    for i in aset:
        if re.search(r"项目",i):
            icount_name.add(i)
            pass
        if re.search(r"编号",i):
            icount_no.add(i)
            pass
        if re.search(r"日期|时间|期限",i):
            icount_time.add(i)
            pass
        if re.search(r"采购人|单位|代理机构|供应商|代表",i):
            icount_org.add(i)
            pass
        if re.search(r"金额|资金|估价|", i):
            icount_money.add(i)
            pass
        if re.search(r"地址|地点|位置",i):
            icount_place.add(i)
            pass
        print i
        pass
        # print i
    print len(aset)
    print "+++++++++"
    print len(icount_name)
    for i in icount_time:
        print i
    print "+++++++++"
    print len(icount_no)
    for i in icount_no:
        print i
    print "+++++++++"
    print len(icount_time)
    for i in icount_time:
        print i
    print "+++++++++"
    print len(icount_org)
    for i in icount_org:
        print i
    print "+++++++++"

    print len(icount_money)
    for i in icount_money:
        print i
    print "+++++++++"
    print len(icount_place)
    for i in icount_place:
        print i
    print "+++++++++"
    pass