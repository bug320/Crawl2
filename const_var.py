# -*- coding:utf-8 -*-
import re

#  下载函数相关
DEFAULT_HEADER = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	    'Accept-Language':'zh-CN,zh;q=0.8',
		'Cache-Control':'max-age=0',
		'Connection':'keep-alive',
		'Host':'www.hngp.gov.cn',
		'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }

# 下载延时，就是等多久下载会网页，单位是秒
DEFAULT_DELAY = 0
# 当下载出错时候，遇到　5XX 错误，重新请求下载几次才停止下载　　
DEFAULT_RETRIES = 5
# socket 的服务请求时间
DEFAULT_TIMEOUT = 60
# 网页缓存
DEFAULT_CACHE = None
DEFAULT_LOGQUEUE = None
DEFAULT_DOWNLOAD_ECHO = not True
DEFAULT_MYSQL_ECHO = True
DEFAULT_CRAWLER_ECHO = not True
# 上面是一些默认设置，可以修改做全局默认，不必每次都加上这些参数。

#  和 crawler 相关的设置
# Beautifullysoup 需要的的 htmlparser 的选择
HTMLPARSER= "html.parser"
# 提取脚本中要 innerHTML 部分的 url
endUrlCmp=re.compile(r'\$\.get\(\"(.*\.htm)')
# 获取 pageUrl 中的 pageNo
pageNo = re.compile(r"pageNo=(\d+)")
# 把 innerHTML 的 url 转换成绝对 url
mainHTTP = "http://www.hngp.gov.cn"
LOG_PATH = './dbs/shelve_cache/log_cache/log.she'      # {pageNo : current}
PAGER_PATH='./dbs/shelve_cache/pager_cache/pager.she'  # {pageNo : (current_url,[sub_urls])}
SUBPAGER_PATH='./dbs/shelve_cache/subpager_cache/subpager.she'

# 数据库相关
## MySQL
MYSQL_TABLE = 'website'
MYSQL_DBASE = 'bug320'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'
MYSQL_HOST = 'localhost'

## MyHbase
HBASE_TABLE = 'website3'

