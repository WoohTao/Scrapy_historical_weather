# Scrapy_historical_weather
一个使用scrapy框架抓取历史天气项目

抓取的数据源：http://lishi.tianqi.com

2011.1至今的全国所有地区的天气数据

##说明
1.爬取的数据包括：最高气温，最低气温，天气，风向，风力

2.获取数据源的网站有少量数据缺失

3.使用MySQL数据库，请在setting.py/db_config中添加自己的数据库信息

4.采用User-Agent代理池，防止被ban

5.添加了爬取延时来防止被ban

##TODO
1.记录出错的url，并实现循环爬取

2.添加IP池
