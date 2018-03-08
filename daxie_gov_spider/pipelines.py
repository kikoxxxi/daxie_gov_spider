# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class DaxieGovSpiderPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host="localhost", user="root", password="xxxxxxxx", db="daxie_db", charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = "INSERT INTO project(pro_name,pro_date,com_name,original_url) VALUES (%s,%s,%s,%s)"
        self.cursor.execute(insert_sql, (item["pro_name"], item["pro_date"],
                                         item["com_name"], item["original_url"]))
        self.conn.commit()
