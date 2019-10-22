#!/usr/bin/python
# -*- coding:utf-8 -*-
# @File     : get_proxy_ip.py
# @Author   : lihui
# @Time     : 2019/10/22 10:20
# @Software : PyCharm
# 说明      :
import pymysql
import requests


class GetIP(object):

    def __init__(self):
        self.connect = pymysql.Connect(
            MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            db=MYSQL_DBNAME,
            charset=MYSQL_CHARSET
        )

    def __del__(self):
        if self.connect:
            self.connect.close()

    def delete_ip(self, ip):
        """
        删除无效IP
        :param ip:
        :return:
        """
        delete_sql = """
            delete from tb_ip_info where ip = %s
        """
        cursor = self.connect.cursor()
        cursor.execute(delete_sql, (ip, ))
        self.connect.commit()
        return True

    def judge_ip(self, ip, port):
        """
        判断IP是否可用
        :param ip:
        :param port:
        :return:
        """
        http_url = "https://bj.ke.com/ershoufang/y4l2l3p4/"
        proxy_url = "http://{0}:{1}".format(ip, port)

        try:
            proxy_dict = {
                'https': proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict)
            code = response.status_code
            if 200 <= code < 300:
                print("%sIP正常" % (ip,))
                return True
            else:
                print("%sIP出现异常" % (ip,))
                self.delete_ip(ip)
                return False
        except Exception as e:
            print("%sIP出现异常" % (ip, ))
            self.delete_ip(ip)
            return False


    def get_random_ip(self):
        """
        随机获取一个可用的IP
        :return:
        """
        random_sql = """
            SELECT ip, port FROM tb_ip_info
            ORDER BY RAND()
            LIMIT 1
        """
        cursor = self.connect.cursor()
        cursor.execute(random_sql)
        res = cursor.fetchall()
        if not res:
            raise LookupError

        for ip_info in res:
            ip = ip_info[0]
            port = ip_info[1]
            if self.judge_ip(ip, port):
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()