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

    def parse(self, response):
        if response.url.find('professional') > -1:
            if response.css('.product-box.product-salesdata'):
                fullTitle = response.css('.product h1').extract_first()
                try:
                    parsedTitle = re.search('\ {2,}[a-z,A-Z,\-, \ ]+\ {2,}', fullTitle)
                    if parsedTitle:
                        parsedTitle = parsedTitle.group(0).strip()
                    else:
                        parsedTitle = '' 
                    parsedTitle = parsedTitle + " " + re.search('fix-spelling.>[a-z,A-Z,\-,\ ,\/,0-9,+,\.,(,),!]+<', fullTitle).group(0).split(">")[1].split("<")[0]
                except:
                    parsedTitle = fullTitle


                description = response.css('#description p').extract_first();
                category = response.css('#breadcrumbs li').extract_first();
                subCategories = response.css('#breadcrumbs li').extract_first();

                yield{
                #    'image',
                    'title': parsedTitle,
                    'description': description,
                    'category': category
                #    'subcategories',
                #    'technical-data'
                }
            else:
                for href in response.css("a::attr('href')"):
                    if href.extract().find('professional') > -1:
                        yield response.follow(href, callback=self.parse)