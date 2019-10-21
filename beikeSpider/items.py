# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IpItem(scrapy.Item):
    ip = scrapy.Field()                 # IP地址
    port = scrapy.Field()               # 端口号
    speed = scrapy.Field()              # 速度


class RoomInfoItem(scrapy.Item):
    room_href = scrapy.Field()          # 房源链接
    total_price = scrapy.Field()        # 总价
    unit_price = scrapy.Field()         # 单价
    room_type = scrapy.Field()          # 户型
    room_floor = scrapy.Field()         # 楼层
    total_floor = scrapy.Field()        # 总楼层
    room_toward = scrapy.Field()        # 朝向
    room_struct = scrapy.Field()        # 房屋类型
    room_decor_info = scrapy.Field()    # 装修情况
    room_area = scrapy.Field()          # 房屋面积
    build_type = scrapy.Field()         # 建筑类型
    build_year = scrapy.Field()         # 建筑年限
    community_name = scrapy.Field()     # 小区
    community_href = scrapy.Field()     # 小区链接
    community_area_name = scrapy.Field()# 小区位置
