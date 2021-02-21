# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy import Spider
from datetime import date

class AlonhadatTradingsSpider(scrapy.Spider):
    name = 'alonhadat_tradings'
    allowed_domains = ['alonhadat.com.vn']
    recorddate = str(date.today())
    start_urls = ['https://alonhadat.com.vn/nha-dat/can-ban.html']
    custom_settings = {'FEED_URI': "alonhadat-tradings_"+recorddate+".json",
                       'FEED_EXPORT_ENCODING': 'utf-8',
                       'FEED_FORMAT': 'json'}
    
    def parse(self, response):
        print("procesing:"+response.url)
        # Extract data using xpath
        # Tiều đề đăng bán
        title = response.xpath('//div[@class="ct_title"]/a/text()').extract()
        # Lấy link theo bài viết
        hreflink = response.css(".ct_title a::attr(href)").extract()
        # Ngày đăng bài viết
        postdate = response.xpath('//div[@class="ct_date"]/text()').extract() 
        # Giá bán
        price = response.xpath('////div[@class="ct_price"]/text()').extract()
        # Địa điểm
        proparea = response.xpath('//div[@class="ct_dis"]/a/text()').extract()
        # Tổng diện tích
        propsquares = response.xpath('//div[@class="ct_dt"]/text()').extract()
        # Kích thước dài x rộng
        measurement = response.xpath('//div[@class="ct_kt"]/text()').extract()
        # Test một số giá trị bổ sung cho Crawler
        floors = response.xpath('//div[@class="characteristics"]/span[@class="floors"]/text()').extract()
        parkings = response.xpath('//div[@class="characteristics"]/span[@class="parking"]/text()').extract()

        row_data = zip(
            title,
            hreflink,
            postdate,
            price,
            proparea,
            propsquares,
            measurement,
            floors,
            parkings
        )

        # Making extracted data row wise
        for item in row_data:
            #create a dictionary to store the scraped info
            scraped_info = {
            #key:value
                'webpage':response.url,
                # item[0] means product in the list and so on, index tells what value to assign
                'title' : item[0],
                'link' : item[1],
                'postdate' : item[2],
                'price' : item[3],
                'proparea' : item[4],
                'propsquares': item[5],
                'measurement': item[6],
                'floors': item[7],
                'parkings': item[8]
            }
        #yield or give the scraped info to scrapy
            yield scraped_info

            pages = response.css('.page a::attr(href)').extract()
            for page in pages:
                if page:
                    yield scrapy.Request(response.urljoin(page), callback=self.parse)
                                        
