#https://www.analyticsvidhya.com/blog/2017/07/web-scraping-in-python-using-scrapy/

# -*- coding: utf-8 -*-
import scrapy


class KarchersiteSpider(scrapy.Spider):
    name = 'karcherSite'
    allowed_domains = ['https://www.kaercher.com/us/professional.html']
    start_urls = ['http://https://www.kaercher.com/us/professional.html/']

    def parse(self, response):
        # get categories
        # get images for categories
        # get urls to category items
            #get subcategory titles
            #click on subCategory
                #navigate to product
                #create new product object in code
                #save description
                #save image
                #tag subCategory
                #tag category

        pass
