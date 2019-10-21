# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from beikeSpider.items import IpItem


class XiciSpider(scrapy.Spider):
    cur_page = 1
    max_page = 3869
    base_url = "http://www.xicidaili.com/nn/%s"
    name = 'xici'
    allowed_domains = ['www.xicidaili.com']
    start_urls = [base_url % cur_page]

    custom_settings = {
        "ITEM_PIPELINES": {
            "beikeSpider.pipelines.IpPipeline"
        }
    }


    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('table', id="ip_list")
        for tr in table.find_all('tr', class_="odd"):
            tds = tr.find_all('td')
            ip = tds[1].get_text()
            port = tds[2].get_text()
            speed = tds[9].find('div', title=True)['title']

            item = IpItem({
                'ip': ip,
                'port': port,
                'speed': speed
            })

            yield item

        self.cur_page += 1
        if self.cur_page <= self.max_page:
            yield scrapy.Request(
                self.base_url % (self.cur_page, )
            )
        else:
            yield
