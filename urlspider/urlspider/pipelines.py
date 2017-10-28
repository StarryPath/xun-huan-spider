# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5

import MySQLdb
import MySQLdb.cursors

class UrlspiderPipeline(object):
    def __init__(self):
        try:
            self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                                host='localhost',
                                                db='test',
                                                user='root',
                                                passwd='19980724',
                                                cursorclass=MySQLdb.cursors.DictCursor,
                                                charset='utf8',
                                                use_unicode=True
                                                )
            print "Connect to db successfully!"

        except:
            print "Fail to connect to db!"

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.insert_into_table, item)
        return item

    def insert_into_table(self, conn, item):

        sql = 'insert into biao4(url,flag) values(%s,%s)'
        param = (item['url'],item['flag'])
        conn.execute(sql, param)