# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from beikeSpider.items import RoomInfoItem


class BeikeSpider(scrapy.Spider):
    name = 'beike'
    allowed_domains = ['bj.ke.com']
    start_urls = ['https://bj.ke.com/ershoufang/y4l2l3p4/']
    custom_settings = {
        "ITEM_PIPELINES": {
            "beikeSpider.pipelines.BeikespiderPipeline": 10
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
        room_floor, total_floor = room_sub_info.split('/')
        # 朝向
        type_main_info = house_info.find('div', class_="type").find('div', class_="mainInfo").get_text()
        type_sub_info = house_info.find('div', class_="type").find('div', class_="subInfo").get_text()
        room_struct, room_decor_info = type_sub_info.split('/')
        # 面积
        area_main_info = house_info.find('div', class_="area").find('div', class_="mainInfo").get_text()
        area_sub_info = house_info.find('div', class_="area").find('div', class_="subInfo").get_text()
        build_year, build_type = area_sub_info.split('/')
        around_info = soup.find('div', class_="aroundInfo")
        # 小区 位置
        community_name = around_info.find('div', class_="communityName").find("span", class_="label").get_text()
        community_href = around_info.find('div', class_="communityName").find("a", class_="info", href=True)['href']
        area_name = ' '.join([area.get_text() for area in around_info.find('div', class_="areaName").find("span", class_="info").find_all("a")])
        room_item = RoomInfoItem({
            'room_href': response.url,
            'total_price': int(float(total_price)),
            'unit_price': int(float(unit_price)),
            'room_type': room_main_info,
            'room_floor': room_floor,
            'total_floor': total_floor,
            'room_toward': type_main_info,
            'room_struct': room_struct,
            'room_decor_info': room_decor_info,
            'room_area': area_main_info.replace('平米', ''),
            'build_year': build_year,
            'build_type': build_type,
            'community_name': community_name,
            'community_href': community_href,
            'community_area_name': area_name
        })
        yield room_item