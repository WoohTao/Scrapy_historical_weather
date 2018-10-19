# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyHistoricalWeatherItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()  # 地名
    date = scrapy.Field()  # 日期
    max_temperature = scrapy.Field()  # 最高温度
    min_temperature = scrapy.Field()  # 最低温度
    weather = scrapy.Field(serializer=str)  # 天气
    wind_direction = scrapy.Field(serializer=str)  # 风向
    wind_speed = scrapy.Field(serializer=str)  # 风力

    pass
