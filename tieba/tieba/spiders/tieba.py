# -*- coding: utf-8 -*-
__author__ = 'Yu Sun'

import scrapy
from tieba.items import Posting


class TiebaSpider(scrapy.Spider):
    name = "tieba"
    allowed_domains = ["tieba.baidu.com"]
    start_urls = [
        "http://tieba.baidu.com/f?kw=%E7%81%AB%E8%BD%A6&ie=utf-8"
    ]

    def parse(self, response):
        for sel in response.xpath('//div[@class="t_con cleafix"]'):
            item = Posting()
            item['title'] = sel.xpath('.//a[@class="j_th_tit "]/text()').extract()
            item['author'] = sel.xpath('.//span[@class="frs-author-name-wrap"]/a/text()').extract()
            item['counts'] = sel.xpath('.//span[@class="threadlist_rep_num center_text"]/text()').extract()
            print("Title: {}\n Author: {}\nReply counts: {}".format(item['title'], item['author'], item['counts']))
            print("-"*79)
