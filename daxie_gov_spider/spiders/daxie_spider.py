# -*- coding:utf-8 -*-

__author__ = 'kikoxxxi'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup
from w3lib.html import remove_tags
from daxie_gov_spider.items import DaxieGovSpiderItem


class DaxieGovSpider(scrapy.Spider):
    name = 'daxie_spider'

    def start_requests(self):
        return [Request(url="http://www.daxie.gov.cn/module/web/jpage/dataproxy.jsp?page=1&appid=1&webid=142&columnid=85336&unitid=134492", callback=self.parse_project)]

    def parse_project(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        record_list = soup.find("recordset").find_all("record")
        # 提取每个链接
        for record in record_list:
            detail_url = "http://www.daxie.gov.cn/" + record.find("a")["href"]
            # 根据标签获取日期和工程名字
            pro_date = record.find("span", class_="time").text
            pro_name = record.find("a")["title"].split("中标公示")[0]
            yield Request(detail_url, callback=self.parse_info, meta={'pro_name': pro_name, 'pro_date': pro_date})

    def parse_info(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        # 对数据以表格形式展示的网页解析，其余为图片形式展示的不做处理
        if soup.find("div", id="detailedWrap").find("table"):
            tr_list = soup.find("div", id="detailedWrap").find(
                "table").find_all("tr")
            com_list = []
            com_kw = '预中标单位名称'
            com_list = self.parse_detail_first(
                tr_list, com_kw, com_list)  # 初步获得中标公司名称
            # 同一项目可能有多个中标公司，分别保存
            for com in com_list:
                com_name = re.sub(r"[\n\t\r ]", "", com).strip()  # 刮掉数据多余的部分
                # 保存数据到items容器
                item = DaxieGovSpiderItem()
                item['com_name'] = com_name
                item['pro_name'] = response.meta["pro_name"]
                item['pro_date'] = response.meta['pro_date']
                item['original_url'] = response.url
                yield item

    # 初步获得所需字段
    def parse_detail_first(self, tr_list, com_kw, com_list):
        # 遍历表格的每一行找到关键字所在的那一行
        for tr in tr_list:
            if com_kw in tr.text:
                td_list = tr.find_all("td")
                com_list = [td.text for td in td_list[1:]
                            if td.text != u'\n\xa0\n']  # 遍历关键字所在行的所有列，保存中标公司名称所在单元格的文字
        return com_list
