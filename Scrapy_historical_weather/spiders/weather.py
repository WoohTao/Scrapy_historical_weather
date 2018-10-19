# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader import ItemLoader
from Scrapy_historical_weather.items import ScrapyHistoricalWeatherItem
from Scrapy_historical_weather.mysql_db import MyMySQLdb


class ChineseWeather(scrapy.Spider):
    name = "ChineseWeather"

    def start_requests(self):
        urls = [
            # 所有地区
            'http://lishi.tianqi.com'  # 历史天气
            # 'http://lishi.tianqi.com/longli/201101.html'  # 测试
            # 省会城市，直辖市
            # 'http://lishi.tianqi.com/beijing/index.html',  # 北京
            # 'http://lishi.tianqi.com/tianjin/index.html',  # 天津
            # 'http://lishi.tianqi.com/shanghai/index.html',  # 上海
            # 'http://lishi.tianqi.com/chongqing/index.html',  # 重庆
            # 'http://lishi.tianqi.com/shijiazhuang/index.html',  # 石家庄
            # 'http://lishi.tianqi.com/shenyang/index.html',  # 沈阳
            # 'http://lishi.tianqi.com/haerbin/index.html',  # 哈尔滨
            # 'http://lishi.tianqi.com/hangzhou/index.html',  # 杭州
            # 'http://lishi.tianqi.com/fuzhou/index.html',  # 福州
            # 'http://lishi.tianqi.com/jinan/index.html',  # 济南
            # 'http://lishi.tianqi.com/guangzhou/index.html',  # 广州
            # 'http://lishi.tianqi.com/wuhan/index.html',  # 武汉
            # 'http://lishi.tianqi.com/chengdu/index.html',  # 成都
            # 'http://lishi.tianqi.com/kunming/index.html',  # 昆明
            # 'http://lishi.tianqi.com/lanzhou/index.html',  # 兰州
            # 'http://lishi.tianqi.com/nanning/index.html',  # 南宁
            # 'http://lishi.tianqi.com/yinchuan/index.html',  # 银川
            # 'http://lishi.tianqi.com/taiyuan/index.html',  # 太原
            # 'http://lishi.tianqi.com/changchun/index.html',  # 长春
            # 'http://lishi.tianqi.com/nanjing/index.html',  # 南京
            # 'http://lishi.tianqi.com/hefei/index.html',  # 合肥
            # 'http://lishi.tianqi.com/nanchang/index.html',  # 南昌
            # 'http://lishi.tianqi.com/zhengzhou/index.html',  # 郑州
            # 'http://lishi.tianqi.com/changsha/index.html',  # 长沙
            # 'http://lishi.tianqi.com/haikou/index.html',  # 海口
            # 'http://lishi.tianqi.com/guiyang1/index.html',  # 贵阳
            # 'http://lishi.tianqi.com/xian/index.html',  # 西安
            # 'http://lishi.tianqi.com/xining/index.html',  # 西宁
            # 'http://lishi.tianqi.com/huhehaote/index.html',  # 呼和浩特
            # 'http://lishi.tianqi.com/lasa/index.html',  # 拉萨
            # 'http://lishi.tianqi.com/wulumuqi/index.html',  # 乌鲁木齐
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_location)

    def parse_location(self, response):
        # 在地点选择页面上获取时间选择的URL
        urls = response.xpath('//ul[@class="bcity"]/li/a/@href').extract()
        for i in range(urls.count('#')):
            urls.remove('#')
        new_table = MyMySQLdb()
        for url in urls:
            new_table.ensure_table_exist(url[24:-11])
            yield scrapy.Request(url=url, callback=self.parse_date)

    def parse_date(self, response):
        new_table = MyMySQLdb()
        new_table.ensure_table_exist(response.url[24:-11])
        # 在时间选择页面上获取每月详细数据的URL
        urls = response.xpath(
            '//div[@id = "tool_site"][@class = "box-base m7"]/div[@class = "tqtongji1"]/ul/li/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_weather)

    def parse_weather(self, response):
        weather = ScrapyHistoricalWeatherItem()
        ll_weather = ItemLoader(weather, response=response)
        ll_weather.add_value('name', response.url[24:-12])  # itemloader中name 赋值
        # 2012.3 之前没有每天的详细信息，网页元素结构与之后的不同
        if response.url[-11:-5] > '201203':
            # 获取天气数据
            divs = response.xpath(
                '//div[@class = "clearfix"]/div[@class = "left"]/div[@class = "box-base m7"]'
                '/div[@class = "tqtongji2"]/ul/li/text()').extract()
            # 获取日期
            divs_date = response.xpath(
                '//div[@class = "clearfix"]/div[@class = "left"]/div[@class = "box-base m7"]'
                '/div[@class="tqtongji2"]/ul/li/a/text()').extract()
            ll_weather.add_value('date', divs_date)
            for i in range(31):
                if (i * 5 + 6) < len(divs):
                    ll_weather.add_value('max_temperature', divs[i * 5 + 6])
                    ll_weather.add_value('min_temperature', divs[i * 5 + 7])
                    ll_weather.add_value('weather', divs[i * 5 + 8])
                    ll_weather.add_value('wind_direction', divs[i * 5 + 9])
                    ll_weather.add_value('wind_speed', divs[i * 5 + 10])
                else:
                    pass
        else:
            # 获取日期和天气数据
            divs = response.xpath(
                '//div[@class = "clearfix"]/div[@class = "left"]/div[@class = "box-base m7"]'
                '/div[@class = "tqtongji2"]/ul/li/text()').extract()
            for i in range(31):
                if (i * 6 + 6) < len(divs):
                    ll_weather.add_value('date', divs[i * 6 + 6])
                    ll_weather.add_value('max_temperature', divs[i * 6 + 7])
                    ll_weather.add_value('min_temperature', divs[i * 6 + 8])
                    ll_weather.add_value('weather', divs[i * 6 + 9])
                    ll_weather.add_value('wind_direction', divs[i * 6 + 10])
                    ll_weather.add_value('wind_speed', divs[i * 6 + 11])
                else:
                    pass
        # 传入item
        ll_weather.load_item()
        yield weather
