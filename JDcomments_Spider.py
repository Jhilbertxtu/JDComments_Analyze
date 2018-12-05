#coding=utf-8
import urllib.request
from lxml.html import etree
import json
from twisted.enterprise import adbapi
from twisted.internet import reactor
import MySQLdb.cursors
class JDcomments(object):
    headers={
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Hosts': 'item.jd.com',
        'Referer': 'item.jd.com',
        'Connection': 'close'
    }
    tbname='phone'
    #手机按评论数排名入口
    productListURL='https://list.jd.com/list.html?cat=9987,653,655&page=1&sort=sort_commentcount_desc&trans=1&JL=4_5_0#J_main'
    productIds=[]
    # 评价星级,1为最低,5为最高
    score=5
    # 最多50页
    page=50
    counts=0
    def __init__(self):
        params=dict (
            host='localhost',
            db='jd_comments',
            user='root',
            port=3306,
            password='****',
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            init_command='set foreign_key_checks=0'  # 异步容易冲突
        )
        self.dbpool=adbapi.ConnectionPool ('MySQLdb',**params)
    #爬取
    def crawl(self):
        for i in range (0, len(self.productIds)):
            print(i,len(self.productIds))
            for j in range (0, self.page):
                # https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv27141&productId=8735304&score=1&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1
                url='https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv129858&productId=%s&score=%s&sortType=5&page=%s&pageSize=10&isShadowSku=0&fold=1' % (
                    self.productIds[i], self.score, j)
                req=urllib.request.Request (url=url, headers=self.headers)
                try:
                    response=urllib.request.urlopen (req)
                    res=str (response.read ().decode ('GBK'))
                    res=res[28:-2]
                    jd_comments=json.loads (res)
                    for item in jd_comments['comments']:
                        #异步存入数据库
                        query=self.dbpool.runInteraction (self.insert_comments, item['content'])
                        query.addErrback (self.handle_error, item['content'])
                except Exception as e:
                    print(e)
        if i==len(self.productIds)-1:
            reactor.stop()
    #插入错误
    def handle_error(self,fail):
        print ('Insert to database error: %s \
        when dealing with item: %s' % (fail))
    #获取产品ID,并调用爬虫
    def pre_data(self):
        req=urllib.request.Request (url=self.productListURL, headers=self.headers)
        response=urllib.request.urlopen (req)
        res=response.read ().decode ('utf8')
        html=etree.HTML (res)
        productlist=html.xpath ('//*[@class="gl-i-wrap j-sku-item"]')
        for item in productlist:
            sku=item.xpath ('@data-sku')
            self.productIds.append (sku[0])
        reactor.callWhenRunning (self.crawl)
        reactor.run ()
    #插入数据库
    def insert_comments(self,cursor, content):
        sql="insert into " + self.tbname + " values(%s, %s, %s)"
        if self.score > 3:
            good=1
        else:
            good=0
        params=[None, good, content]
        self.counts=self.counts+1
        print('inserts :',self.counts)
        cursor.execute (sql, params)
def main():
    jdc=JDcomments ()
    jdc.pre_data()

if __name__=='__main__':
    main()