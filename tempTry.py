# -*- coding:utf -*-
import downloader
import urlparse
import shelve
import re

if __name__ == '__main__':
    sub_path = 'html_cache/page_cache/subpage_she.she'
    page_path = 'html_cache/page_cache/page_she.she'

    _she = shelve.open(sub_path, "c")
    _she = shelve.open(page_path, "r")
    for i,k in _she.iteritems():
        print i
        print k
        pass
    print len(_she)
    _she.close()
    pass