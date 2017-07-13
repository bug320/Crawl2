# -*- coding:utf-8 -*-

import MySQLdb
import happybase
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import downloader
from const_var import *
download =downloader.Downloader()

class MySQL(object):
    def __init__(self,table,db,user="root",passwd="root",localhost="localhost"):
        self.table =table
        self.db =db
        self.user=user
        self.passwd =passwd
        self.localhost =localhost
        # self.conn= MySQLdb.connect(host=self.localhost,port = self.port,user=self.user,passwd=self.passwd,db =self.db)
        self.conn = MySQLdb.connect(host="localhost",user=user,passwd=passwd,db=db,charset='utf8')
        self.cur = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        pass
    def __len__(self):
        try:
            sql = "SELECT COUNT(*) FROM %s" % self.table
            self.cur.execute(sql)
            slen = self.cur.fetchall()
            # print type(slen[0]["COUNT(*)"])
            pass
        except Exception as e:
            print "can't not get the len :",e
            self.conn.rollback()
            return 0
            pass
        else:
            return slen[0]["COUNT(*)"]
            pass
        pass
    def close(self):
        self.cur.close()
        self.conn.close()
        pass
    def tables(self):
        self.cur.execute("SHOW TABLES")
        self.bug_tables = []
        for idict in self.cur.fetchall():
            self.bug_tables.append(idict.values()[0].encode('utf-8'))
        return self.bug_tables
        pass
    def create(self,table,sql):
        if table in self.tables():
            print "the table named %s have created in the database named %s" % (table,self.db)
            return
            pass
        else:
            try:
                self.cur.execute(sql)
                self.conn.commit()
                self.table = table
                # print self.table
                pass
            except Exception as e:
                print "Create the table is wrong !",e
                self.conn.rollback()
                pass
            else:
                print "Success to crete the table :  %s and change it as the defult table ",self.table
            pass
        pass
    def save(self,itDict):
        keys = ""
        values = ""

        for key, value in itDict.items():
            keys = keys + "," + key
            values = values + ",\"" + value + "\""
            pass
        keys = keys[1:]
        values = values[1:]
        keys += ",mysql,hbase"
        values += ',"1","0"'
        # print keys
        # print values
        # return

        try:
            sql = "SELECT url from %s where url = '%s' " % (self.table, itDict["url"])
            # print sql
            self.cur.execute(sql)
            p = self.cur.fetchall()
            if p == ():
                # print "p is empty"
                sql = "INSERT INTO %s( %s ) VALUES( %s )" % (self.table, keys, values)
                self.cur.execute(sql)
                self.conn.commit()
            else:
                print " %s have save into the mysql" % itDict["url"]
            # print p
            pass
        except Exception as e:
            self.conn.rollback()
            print "mysql error --- ", e
            # 这里不能返回 否则数据库就没有关闭
            pass
        pass
    def get(self,sql=None):
        try:
            sql = "SELECT * from %s" % self.table if not sql else sql
            self.cur.execute(sql)
            return self.cur.fetchall()
            pass
        except Exception as e:
            self.conn.rollback()
            # self.conn.commit()
            print "MySQL.get():",e
            pass
        else:
            pass
        pass
    def remove(self,sql):
        # todo: 暂时不需要
        pass
    def update(self,id,sql=None):
        # todo: 暂时默认更新 hbase 字段，用在存入hbase后跟新自身
        try:
            sql = "update  %s set hbase='1' where id = '%s' " % (MYSQL_TABLE,id) if not sql else sql
            # update user set username="name91" where userid=
            self.cur.execute(sql)
            self.conn.commit()
            pass
        except Exception as e:
            self.conn.rollback()
            print "MySQL.update():",e
            pass
        else:
            pass
        pass
    pass

class MyHbase(object):
    def __init__(self,table,localhost="127.0.0.1"):
        try:
            self.conn = happybase.Connection(host=localhost)
            if table not in self.conn.tables():
                self.conn.create_table("%s" % table, {"page": dict()})
                self.table = self.conn.table(table)
                print "create the table successful"
                pass
            else:
                self.table = self.conn.table(table)
                print "connect the table successful"
                pass
            pass
        except Exception as e:
            print "MySQL.__init__:",e
            pass
        pass
    def save(self,idict):
        for k,v in idict.iteritems():
            if k =='id':
                continue
                pass
            # print type(k),type(v)
            if k == 'inner_html_url':
                try:
                    soup = BeautifulSoup(download(idict["inner_html_url"]), HTMLPARSER)
                    pass
                except Exception as e:
                    print "Main error", e
                    pass
                else:
                    print "保留所有标签的文本"
                    stxt = [UnicodeDammit(string).unicode_markup.encode('utf-8') for string in soup.stripped_strings]
                    if stxt == []:
                        print "The stxt is None"
                        retxt = 'None'
                        ki = 'inner_html'
                        vi = retxt
                        # print "'page:%s'" % ki
                        # print "'%s'" % vi
                        self.table.put('%d' % idict['id'], {'page:%s' % ki: '%s' % vi})
                        # log.add(idict['id'])
                        pass
                    else:
                        retxt = reduce(lambda x, y: x + y + '\n', stxt)
                        ki = 'inner_html'
                        vi = retxt
                        # print "'page:%s'" % ki
                        # print "'%s'" % vi
                        self.table.put('%d' % idict['id'], {'page:%s' % ki: '%s' % vi})
                        # print retxt
                        #
                        # for i in stxt:
                        #     print i
                    pass
                pass
            else:
                # print "'page:%s'  :'%s' " % (k, v)
                self.table.put("%d"%idict['id'],{'page:%s'%k:'%s'%v})
                pass
            pass
        pass
    def get(self):
        return self.table.scan()
        pass
    pass
if __name__ == "__main__":
    hdb = MyHbase(HBASE_TABLE)
    print "Connect to hbase successful"
    print "Now the hbase has thoses tables:"
    print hdb.conn.tables()
    for row,idict in hdb.table.scan():
        print row
        for k,v in idict.iteritems():
            print k,v
    pass
#     mdb = MySQL(table="website3",db="bug320")
#     print "Succeful connect to mysql!"
#     print "the dbase named %s have those tables:" % mdb.db
#     for table in mdb.tables():
#         print table,",",
#     print ""
#     # 创建新表
#     newtable = "website3"
#     sql = r"""create TABLE %s(
#   id int(20) not null AUTO_INCREMENT,
#   url CHAR(225),
#   title VARCHAR(225),
#   org VARCHAR(225),
#   person VARCHAR (225),
#   post_time VARCHAR(40),
#   check_post VARCHAR(40),
#   inner_html_url VARCHAR(225),
#   mysql int(1),
#   hbase int(1),
#   PRIMARY KEY (id)
# )ENGINE= MYISAM CHARACTER SET utf8 ;""" % newtable
#     mdb.create(newtable,sql)
#     # 产看长度
#     print len(mdb)
#     sql = "select id,hbase from %s" % MYSQL_TABLE
#     resilt = mdb.get(sql)
#     # {}.iteritems()
#     for idict in resilt:
#         for k,v in idict.iteritems():
#             print "%s  %s" % (k,v)
#             # mdb.update(idict["id"])
#         # break
#     # print "Update:"
#     # resilt = mdb.get(sql)
#     # # {}.iteritems()
#     # for idict in resilt:
#     #     for k, v in idict.iteritems():
#     #         print "%s  %s" % (k, v)
#     #     break
#     mdb.close()
#     pass