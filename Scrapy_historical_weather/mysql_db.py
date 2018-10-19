# -*- coding: utf-8 -*-


import pymysql
import logging
import scrapy
from Scrapy_historical_weather.settings import db_config


class MyMySQLdb(object):

    def __init__(self, host=db_config.get("host"), user=db_config.get("user"),
                 password=db_config.get("password"), database=db_config.get("database"),
                 port=db_config.get("port"), charset=db_config.get("charset")):
        self.database = pymysql.connect(host, user, password, database, port, charset=charset)
        # self.check_table_data_flag = 0  # 1:存在 0：不存在

    def __del__(self):
        self.database.close()

    def ensure_table_exist(self, table_name):
        cursor = self.database.cursor()
        try:
            # 检查是否存在表
            table_exist = cursor.execute("SHOW TABLES LIKE %s", table_name)
            if table_exist == 0:
                self.create_table(table_name)
            else:
                # 检查表内是否有数据
                cursor.execute("SELECT COUNT(*) FROM " + table_name)
                if cursor.fetchone()[0] != 0:  # 有数据
                    # self.check_table_data_flag = 1
                    logging.log(logging.INFO, "--------check table --------:exist table %s, exist data", table_name)
                else:  # 没有数据
                    # self.check_table_data_flag = 0
                    cursor.execute("DROP TABLE " + table_name)
                    self.create_table(table_name)
        except Exception as e:
            self.database.rollback()
            logging.error("--------check table error--------table:%s exception：%s", table_name, e)
        finally:
            cursor.close()

    def create_table(self, table_name):
        cursor = self.database.cursor()
        sql = "CREATE TABLE " + table_name + "(WEATHER_DATE DATE," \
                                             " MAX_TEMP CHAR(10)," \
                                             " MIN_TEMP CHAR(10)," \
                                             " WEATHER CHAR(30)," \
                                             " WIND_DIRECT CHAR(30)," \
                                             " WIND_SPEED CHAR(30), " \
                                             "PRIMARY KEY (`WEATHER_DATE`))" \
                                             "DEFAULT CHARSET=utf8"
        try:
            cursor.execute(sql)
        except Exception as e:
            self.database.rollback()
            logging.error("--------create table error--------table:%s exception：%s", table_name, e)
        finally:
            cursor.close()

    def delete_table(self, table_name):
        cursor = self.database.cursor()
        sql = "DROP TABLE " + table_name
        try:
            cursor.execute(sql)
        except Exception as e:
            self.database.rollback()
            logging.error("--------delete table error--------table:%s exception：%s", table_name, e)
        finally:
            cursor.close()

    def insert_data(self, table_name, data, max_temp, min_temp, weather, wind_direct, wind_speed):
        cursor = self.database.cursor()
        sql = "INSERT INTO " + table_name + "(WEATHER_DATE, MAX_TEMP, MIN_TEMP, WEATHER, WIND_DIRECT, WIND_SPEED)" \
                                            "VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"\
              % (data, max_temp, min_temp, weather, wind_direct, wind_speed)
        try:
            cursor.execute(sql)
            self.database.commit()
        except Exception as e:
            self.database.rollback()
            logging.error("--------insert data error--------table:%s exception：%s", table_name, e)
        finally:
            cursor.close()

    def insert_item(self, item=scrapy.Item):
        table_name = item['name'][0]
        try:
            for i in range(len(item['date'])):
                self.insert_data(table_name, item['date'][i], item['max_temperature'][i], item['min_temperature'][i],
                                 item['weather'][i], item['wind_direction'][i], item['wind_speed'][i])
        except Exception as e:
            logging.error("--------insert item error--------table:%s exception：%s", table_name, e)
