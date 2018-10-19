# -*- coding:utf-8 -*-

from scrapy import cmdline

# scrapy crawl itcast （itcast为爬虫名）
cmdline.execute("scrapy crawl ChineseWeather".split())
