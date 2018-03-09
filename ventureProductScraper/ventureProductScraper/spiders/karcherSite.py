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

    def parsedTitleFromResp(self, response):
        fullTitle = response.css('.product h1').extract_first()
        parsedTitle = ''
        try:
            parsedTitle = re.search('\ {2,}[a-z,A-Z,\-, \ ]+\ {2,}', fullTitle)
            if parsedTitle:
                parsedTitle = parsedTitle.group(0).strip()
            parsedTitle = parsedTitle + " " + re.search('fix-spelling.>[a-z,A-Z,\-,\ ,\/,0-9,+,\.,(,),!]+<', fullTitle).group(0).split(">")[1].split("<")[0]
        except:
            parsedTitle = fullTitle
        return parsedTitle

    def parsedDescFromResp(self, response):
        description = response.css('#description p').extract_first()
        description = description.split('<p property=\"description\">')[1].split('</p>')[0]
        return description

    def parsedCatFromResp(self, response):
        category = response.css('#breadcrumbs li').extract();
        category = category[2].split('property=\"name\">')[1].split('</span')[0]
        return category        

    def parsedSubCatsFromResp(self, response):
        subCategories = response.css('#breadcrumbs li').extract();
        finalCats = []
        for i in range(3,len(subCategories)):
            finalCats.append(subCategories[i].split('property=\"name\">')[1].split('</span')[0])
        return str(finalCats)

    def parse(self, response):
        if response.url.find('professional') > -1:
            if response.css('.product-box.product-salesdata'):
                yield{
                #    'image',
                    'title': self.parsedTitleFromResp(response),
                    'description': self.parsedDescFromResp(response),
                    'category': self.parsedCatFromResp(response),
                    'subcategories': self.parsedSubCatsFromResp(response)
                #    'technical-data'
                }
            else:
                for href in response.css("a::attr('href')"):
                    if href.extract().find('professional') > -1:
                        yield response.follow(href, callback=self.parse)