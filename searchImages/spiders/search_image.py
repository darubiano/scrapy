# -*- coding: utf-8 -*-
import re
import scrapy
import requests
from scrapy.spiders import Spider
from ..items import SearchimagesItem

class SearchImageSpider(scrapy.Spider):
    name = 'image'
    search = input("Escribe lo que deseas buscar : ")
    start_urls = ['https://www.shutterstock.com/es/search/'+search+'?page=1']
    page_number= 2
    pages=0
    count = 0 

    def parse(self, response):
        items = SearchimagesItem()
        
        image_url = response.css('img::attr(src)').extract()
        
        if SearchImageSpider.count == 0:
            number_page = response.css('.b_M_g::text').extract()
            SearchImageSpider.pages = int(re.sub("\D", "", number_page[0]))
            SearchImageSpider.count +=1

        items['image_url'] = image_url


        for url in image_url:
            name_image='./img/'+str(SearchImageSpider.count)+'.jpg'
            image = requests.get(url).content
            with open(name_image, 'wb') as handler:
                handler.write(image)
            SearchImageSpider.count+=1

        yield items

        next_page = 'https://www.shutterstock.com/es/search/'+SearchImageSpider.search+'?page='+str(SearchImageSpider.page_number)

        if SearchImageSpider.page_number<=SearchImageSpider.pages:
            SearchImageSpider.page_number +=1
            yield response.follow(next_page, callback=self.parse)

