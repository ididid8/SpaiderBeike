# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup


class BeikeSpider(scrapy.Spider):
    name = 'beike'
    allowed_domains = ['bj.ke.com']
    start_urls = ['https://bj.ke.com/ershoufang/y4l2l3p4/']

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
        price = soup.find('div', class_="price")
        total_price = price.find('span', class_='total').get_text()
        unit_price = price.find('span', class_='unitPriceValue').get_text()
        house_info = soup.find('div', class_="houseInfo")
        room_main_info = house_info.find('div', class_='room').find('div', class_="mainInfo").get_text()
        room_sub_info = house_info.find('div', class_='room').find('div', class_="subInfo").get_text()
        type_main_info = house_info.find('div', class_="type").find('div', class_="mainInfo").get_text()
        type_sub_info = house_info.find('div', class_="type").find('div', class_="subInfo").get_text()
        area_main_info = house_info.find('div', class_="area").find('div', class_="mainInfo").get_text()
        area_sub_info = house_info.find('div', class_="area").find('div', class_="subInfo").get_text()

        around_info = soup.find('div', class_="aroundInfo")
        community_name = around_info.find('div', class_="communityName").find("span", class_="label").get_text()
        community_href = around_info.find('div', class_="communityName").find("a", class_="info", href=True)['href']
        area_name = [ for area in around_info.find('div', class_="areaName").find("span", class_="info").find_all("a")]



        base = soup.find('div', class_="base")
        transaction = soup.find('div', class_="transaction")
        pass