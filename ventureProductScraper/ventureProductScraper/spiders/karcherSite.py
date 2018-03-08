#https://www.analyticsvidhya.com/blog/2017/07/web-scraping-in-python-using-scrapy/
#https://doc.scrapy.org/en/latest/intro/tutorial.html
# debugging: https://github.com/DonJayamanne/pythonVSCode/issues/249
# debugging: https://docs.scrapy.org/en/latest/topics/debug.html

# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy.utils.response import open_in_browser

class KarchersiteSpider(scrapy.Spider):
    name = 'karcherSite'
    # allowed_domains = ['kaercher.com/']
    start_urls = ['https://www.kaercher.com/us/professional.html/']


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

    def parse(self, response):
        if response.url.find('professional') > -1:
            if response.css('.product-box.product-salesdata'):
                fullTitle = response.css('.product h1').extract()
                parsedTitle = re.search('\ {2,}[a-z,A-Z,\-, \ ]+\ {2,}',fullTitle)
                parsedTitle = parsedTitle.group(0) if parsedTitle else '' 
                parsedTitle = parsedTitle + re.search('fix-spelling">[a-z,A-Z,\-, \ ]+<', fullTitle).split(">")[1].split("<")[0]
                
                yield{
                #    'image',
                    'title': parsedTitle
                    #'description',
                    #'category',
                #    'subcategories',
                #    'technical-data'
                }
            else:
                for href in response.css("a::attr('href')"):
                    yield response.follow(href, callback=self.parse)

    def cleanTitle(self, title):
        return title

    def parse_old(self, response):
        for category in response.css(".product-item"):
            categoryName = category.css(".headlinebottom a::text").extract_first()
            for href in category.css(".headlinebottom a::attr('href')"):
                yield response.follow(href, callback=self.parseSubCat, meta={'category': categoryName})
    
    def parseSubCat(self, response):
        #open_in_browser(response)
        #for href in response.css('#products a img').css("a::attr('href')"):
        for href in response.css('#products a::attr("href")'):
            yield response.follow(href, callback=self.parseProductsGrid, meta={'category': response.request.meta['category']})
    
    def parseProductsGrid(self, response):
        open_in_browser(response)
        yield {
            'category': response.request.meta['category']
        }

    def checkIfOnProductPages(self, response):
        #instead of knowing HOW to get to the product pages
        #just have it visit EVERY page, looking for product pages
        #and find some way to scope it to only professional products, 
        #to avoif home and garden
        if response.url.find('professional') > -1 and response.css('.product-box.product-salesdata'):
            yield{
            #    'image',
                'title': response.css('.product h1').extract()
                #'description',
                #'category',
            #    'subcategories',
            #    'technical-data'
            }