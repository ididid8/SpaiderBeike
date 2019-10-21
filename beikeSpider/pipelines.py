# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import cursors
from twisted.enterprise import adbapi


class BasicDbPipeline(object):
    def __init__(self, db_pool):
        self.db_pool = db_pool

    @classmethod
    def from_settings(cls, settings):
        db_params = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            port=settings['MYSQL_PORT'],
            database=settings['MYSQL_DBNAME'],
            charset=settings['MYSQL_CHARSET'],
            use_unicode=True,
            cursorclass=cursors.DictCursor,
            autocommit=True
        )
        db_pool = adbapi.ConnectionPool('pymysql', **db_params)
        return cls(db_pool)

    def handle_error(self, failure, item, spider):
        print(failure)

    def process_item(self, item, spider):
        raise NotImplementedError

class IpPipeline(BasicDbPipeline):

    def process_item(self, item, spider):
        query = self.db_pool.runInteraction(self.insert_into, item)
        query.addErrback(self.handle_error, item, spider)

        return item

    def insert_into(self, cursor, item):
        sql = """
        INSERT INTO tb_ip_info (
          ip,
          port,
          speed
        ) VALUES (
          %s,
          %s,
          %s
        )
        """
        args = (
            item['ip'],
            item['port'],
            item['speed']
        )
        cursor.execute(sql, args)


class BeikespiderPipeline(BasicDbPipeline):

    def process_item(self, item, spider):
        query = self.db_pool.runInteraction(self.insert_into, item)
        query.addErrback(self.handle_error, item, spider)

        return item

    def insert_into(self, cursor, item):
        sql = """
        INSERT INTO tb_room_detail (
            room_href,
            total_price,
            unit_price,
            room_type,
            room_floor,
            total_floor,
            room_toward,
            room_struct,
            room_decor_info,
            room_area,
            build_type,
            build_year,
            community_name,
            community_href,
            community_area_name,
        ) VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
        )
        """
        args = (
            item['room_href'],
            item['total_price'],
            item['unit_price'],
            item['room_type'],
            item['room_floor'],
            item['total_floor'],
            item['room_toward'],
            item['room_struct'],
            item['room_decor_info'],
            item['room_area'],
            item['build_type'],
            item['build_year'],
            item['community_name'],
            item['community_href'],
            item['community_area_name'],
        )

        cursor.execute(sql, args)
