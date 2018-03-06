#https://www.analyticsvidhya.com/blog/2017/07/web-scraping-in-python-using-scrapy/
#https://doc.scrapy.org/en/latest/intro/tutorial.html
# debugging: https://github.com/DonJayamanne/pythonVSCode/issues/249
# debugging: https://docs.scrapy.org/en/latest/topics/debug.html

# -*- coding: utf-8 -*-
import scrapy


class KarchersiteSpider(scrapy.Spider):
    name = 'karcherSite'
    allowed_domains = ['https://www.kaercher.com/us/professional.html']
    start_urls = ['https://www.kaercher.com/us/professional.html/']

    products = [];


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
        for category in response.css(".product-item"):
            yield {
                'title': category.css(".headlinebottom a::text").extract_first(),
                'link': category.css(".headlinebottom a::attr('href')").extract_first()
            }
        

        next_page = response.css(".product-item .headlinebottom a::attr('href')").extract_first()
        
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parseSubCat)

        #response.follow(categoryLinks[0], self.parse)
        #print(response)
        #view(response)
        pass

    
    def parseSubCat(self, response):
        yield {
            'test': "test"
        }
        pass
