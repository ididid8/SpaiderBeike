# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup


class BeikeSpider(scrapy.Spider):
    name = 'beike'
    allowed_domains = ['bj.ke.com']
    start_urls = ['https://bj.ke.com/ershoufang/y4l2l3p4/']
    custom_settings = {
        "ITEM_PIPELINES": {
            "beikeSpider.pipelines.BeikespiderPipeline"
        }
    }

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html, "lxml")
        elements = soup.find_all('li', class_="clear")
        for element in elements:
            href = element.find('a', class_='img', href=True)['href']
            yield scrapy.Request(
                href,
                callback=self.parse_detail
            )

    def parse_detail(self, response):
        html = response.body
        soup = BeautifulSoup(html, "lxml")
        # 价格
        price = soup.find('div', class_="price")
        total_price = price.find('span', class_='total').get_text()
        unit_price = price.find('span', class_='unitPriceValue').get_text()
        house_info = soup.find('div', class_="houseInfo")
        # 户型
        room_main_info = house_info.find('div', class_='room').find('div', class_="mainInfo").get_text()
        room_sub_info = house_info.find('div', class_='room').find('div', class_="subInfo").get_text()
        # 朝向
        type_main_info = house_info.find('div', class_="type").find('div', class_="mainInfo").get_text()
        type_sub_info = house_info.find('div', class_="type").find('div', class_="subInfo").get_text()
        # 面积
        area_main_info = house_info.find('div', class_="area").find('div', class_="mainInfo").get_text()
        area_sub_info = house_info.find('div', class_="area").find('div', class_="subInfo").get_text()

        around_info = soup.find('div', class_="aroundInfo")
        # 小区 位置
        community_name = around_info.find('div', class_="communityName").find("span", class_="label").get_text()
        community_href = around_info.find('div', class_="communityName").find("a", class_="info", href=True)['href']
        area_name = ' '.join([area.get_text() for area in around_info.find('div', class_="areaName").find("span", class_="info").find_all("a")])

        pass