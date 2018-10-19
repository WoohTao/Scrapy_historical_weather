# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from Scrapy_historical_weather.mysql_db import MyMySQLdb


class ScrapyHistoricalWeatherPipeline(object):
    def process_item(self, item, spider):
        # TODO check data
        try:
            insert_weather = MyMySQLdb()
            insert_weather.insert_item(item)
        except Exception as e:
            raise DropItem('Cannot Insert %s %s into mysql. Exception：%s' % (item['name'], item['date'], e))
        return item
