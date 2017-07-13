# -*- coding:utf -*-
import MySQLdb
from bs4 import UnicodeDammit
from bs4 import BeautifulSoup
CACHE_ = "Crawler"
page_cache = 'page_cache'

class Cache(object):
    def __init__(self,table =page_cache,db=CACHE_,user='root',passwd='root',localhost='127.0.0.1'):
        self.table =table
        self.db =db
        self.user=user
        self.passwd =passwd
        self.localhost =localhost
        # self.conn= MySQLdb.connect(host=self.localhost,port = self.port,user=self.user,passwd=self.passwd,db =self.db)
        self.conn = MySQLdb.connect(host="localhost",user=user,passwd=passwd,db=db,charset='utf8')
        self.cur = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        try:
            self.cur.execute("show tables")
            idcit = self.cur.fetchall()
            # print idcit
            idcit = idcit[0] if idcit else None
            if idcit:
                if self.table in idcit.values():
                    create = False
                    # print "NO"
                else:
                    print idcit.values()
                    # print "OK"
                    create = True
            else:
                create = True
            if create:
                sql = "CREATE TABLE %s (id VARCHAR(225) NOT NULL,html TEXT ,PRIMARY KEY (id))DEFAULT CHARSET=utf8 " % (self.table)
                self.cur.execute(sql)
                self.conn.commit()
            print "connect to table %s ..." % self.table
            pass
        except Exception as e:
            self.conn.rollback()
            print e
            pass


        pass

    def __del__(self):
        self.cur.close()
        self.conn.close()
        pass
    def __getitem__(self, item):

        try:
            sql = "SELECT HTML FROM %s WHERE id = '%s'" % (self.table, item)
            self.cur.execute(sql)
            idict = self.cur.fetchall()
            # print idict
            idict = idict[0] if idict else {}
            if idict:
                return idict.get('HTML',None)
            else:
                return None
            pass
        except Exception as e:
            self.conn.rollback()
            print e
            return None
            pass
        pass
    def __setitem__(self, key, value):
        try:
            svalue = MySQLdb.escape_string(value)
            dommit  = UnicodeDammit(svalue)
            svalue = dommit.unicode_markup
            # print type(svalue)
            sql = "INSERT INTO %s VALUES('%s','%s') ON DUPLICATE KEY UPDATE html='%s'"\
                  % (self.table, key, svalue, svalue)
            self.cur.execute(sql)
            self.conn.commit()
            pass
        except Exception as e:
            self.conn.rollback()
            print e
            pass
        pass

    def __delitem__(self, key):
        try:
            sql = "DELETE FROM %s WHERE id = '%s'" % (self.table,key)
            self.cur.execute(sql)
            self.conn.commit()
            pass
        except Exception as e:
            self.conn.rollback()
            print e
            pass
        pass

    def __len__(self):
        try:
            sql = 'SELECT COUNT(*) FROM %s' % self.table
            self.cur.execute(sql)
            return self.cur.fetchall()[0]['COUNT(*)']
            pass
        except Exception as e:
            self.conn.rollback()
            print e
            return 0
            pass

    def keys(self):
        try:
            sql = "SELECT * FROM %s" % self.table
            self.cur.execute(sql)
            idict = self.cur.fetchall()
            idict = [i for i in idict]
            return [i['id'] for i in idict]
            pass
        except Exception as e:
            return []
            pass
        pass
    def values(self):
        try:
            sql = "SELECT * FROM %s" % self.table
            self.cur.execute(sql)
            idict = self.cur.fetchall()
            idict = [i for i in idict]
            return [i['html'] for i in idict]
            pass
        except Exception as e:
            return []
            pass
        pass
    def iteritems(self):
        try:
            sql = "SELECT * FROM %s" % self.table
            self.cur.execute(sql)
            idict = self.cur.fetchall()
            idict = [i for i in idict]
            return ((i['id'],i['html'])for i in idict)
            pass
        except Exception as e:
            return {}.iteritems()
            pass
        pass
        # dict.iteritems()
    pass

if __name__ == '__main__':
    cache = Cache()
    for i, k in cache.iteritems():
        print i,type(k)
    # cache = Cache()
    # # for i,v in cache.iteritems():
    # #     print i,v
    # # else:
    # #     print "OK"
    # print 'len = ',len(cache)
    # print "before set..."
    # print "get cache[test_1] = ", cache['test_1']
    # print "get cache[test_2] = ", cache['test_2']
    #
    # print "now set..."
    # cache['test_1'] = '123'
    # print "set cache[test_1] = ",cache['test_1']
    # print "set test_1:123 OK"
    # print 'len = ', len(cache)
    # cache['test_2'] = '345'
    # print "set cache[test_2] = ",cache['test_2']
    # print "set test_2:345 OK"
    # print 'len = ', len(cache)
    #
    # print "after set..."
    # print "get cache[test_1] = ", cache['test_1']
    # print "get cache[test_2] = ", cache['test_2']
    #
    # print 'len = ', len(cache)
    # print "now delete..."
    # del cache['test_1']
    # print "del test_1 OK"
    # print 'len = ', len(cache)
    # del cache['test_2']
    # print "del test_2 OK"
    # print 'len = ', len(cache)
    #
    # print "after del"
    # print "get cache[test_1] = ", cache['test_1']
    # print "get cache[test_2] = ", cache['test_2']
    #
    #
    # print 'base test OK'
    # print "iteritems(),keys(),values()"
    # for k in xrange(10):
    #     k = str(k)
    #     cache[k] = "v"+k
    # print len(cache)
    # # print cache.iteritems()
    # for k,v in cache.iteritems():
    #     print k,v
    # else:
    #     print "ON1"
    #     print "keys():", cache.keys()
    #     print "values():", cache.values()
    #
    # for i in cache.keys():
    #     print i,cache[i]
    #
    # for k in xrange(10):
    #     k = str(k)
    #     del cache[k]
    #
    # for k.v in cache.iteritems():
    #     print k,v
    # else:
    #     print "ON2"
    #
    # print 'len = ', len(cache)

    pass
