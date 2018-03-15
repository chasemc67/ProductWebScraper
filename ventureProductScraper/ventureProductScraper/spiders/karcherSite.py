#https://www.analyticsvidhya.com/blog/2017/07/web-scraping-in-python-using-scrapy/
#https://doc.scrapy.org/en/latest/intro/tutorial.html
# debugging: https://github.com/DonJayamanne/pythonVSCode/issues/249
# debugging: https://docs.scrapy.org/en/latest/topics/debug.html

# -*- coding: utf-8 -*-
import scrapy
import re

from bs4 import BeautifulSoup

from scrapy.utils.response import open_in_browser

class KarchersiteSpider(scrapy.Spider):
    name = 'karcherSite'
    # allowed_domains = ['kaercher.com/']
    start_urls = ['https://www.kaercher.com/us/professional.html/']

    def parsedTitleFromResp(self, response):
        title = BeautifulSoup(response.css('.product h1').extract_first(), 'lxml').get_text().strip()
        title = re.sub(" +", " ", title) # remove doublespaces
        return title

    def parsedHandleFromResp(self, response):
        handle = self.parsedTitleFromResp(response)
        handle = handle.replace(" ", "-") # replace spaces with - 
        handle = handle.replace("/", "-") # replace spaces with - # replace / with - 
        handle = re.sub('[^a-zA-Z0-9-]+', "", handle)# replace anything non alpha-numberic or dashed or space with nothing
        # only known offender right now is Commercial Carpet Extractor Puzzi
        return handle

    def parsedDescFromResp(self, response):
        description = BeautifulSoup(response.css('#description p').extract_first(), 'lxml').get_text().strip()
        return description

    def parsedCatFromResp(self, response):
        category = response.css('#breadcrumbs li').extract();
        category = BeautifulSoup(category[1], 'lxml').get_text().strip()
        return category        

    def parsedSubCatsFromResp(self, response):
        subCategories = response.css('#breadcrumbs li').extract();
        finalCats = []
        for i in range(2,len(subCategories)-1):
            finalCats.append(BeautifulSoup(subCategories[2], 'lxml').get_text().strip())
        if len(finalCats) == 0:
            return ""
        return ", " + ','.join(finalCats)  #put a leading comma because of defaults, then new ones

    def parse(self, response):
        if response.url.find('professional') > -1:
            if response.css('.product-box.product-salesdata'):
                img_url = "https:" + response.css('.product-image a::attr("href")').extract_first()
                yield{
                    #debug
                    #'productUrl': response.url, 
                    
                    # shopify specific tags https://help.shopify.com/manual/products/import-export
                    "Handle": self.parsedHandleFromResp(response), # handles and titles with slashes dont work
                    "Title": self.parsedTitleFromResp(response),  # Make sure vital oxide looks good on shopify
                    "Body (HTML)": "<p>"+self.parsedDescFromResp(response)+"</p>",
                    "Vendor": "Karcher",
                    "Type": self.parsedCatFromResp(response),
                    "Tags": "karcher, equipment"+self.parsedSubCatsFromResp(response),
                    "Published": "TRUE",
                    "Option1 Name": "Title",
                    "Option1 Value": "Default Title",
                    "Option2 Name": "",
                    "Option2 Value": "",
                    "Option3 Name": "",
                    "Option3 Value": "",
                    "Variant SKU": "",
                    "Variant Grams": "",
                    "Variant Inventory Tracker": "",
                    "Variant Inventory Qty": "1",
                    "Variant Inventory Policy": "deny",
                    "Variant Fulfillment Service": "manual",
                    "Variant Price": "",
                    "Variant Compare At Price": "",
                    "Variant Requires Shipping": "",
                    "Variant Taxable": "",
                    "Variant Barcode": "",
                    "Image Src": img_url,
                    "Image Position": "1",
                    "Image Alt Text": "",
                    "Gift Card": "",
                    "SEO Title": "",
                    "SEO Description": "",
                    "Google Shopping / Google Product Category": "",
                    "Google Shopping / Gender": "",
                    "Google Shopping / Age Group": "",
                    "Google Shopping / MPN": "",
                    "Google Shopping / AdWords Grouping": "",
                    "Google Shopping / AdWords Labels": "",
                    "Google Shopping / Condition": "",
                    "Google Shopping / Custom Product": "",
                    "Google Shopping / Custom Label 0": "",
                    "Google Shopping / Custom Label 1": "",
                    "Google Shopping / Custom Label 2": "",
                    "Google Shopping / Custom Label 3": "",
                    "Google Shopping / Custom Label 4": "",
                    "Variant Image": "",
                    "Variant Weight Unit": "",
                    "Variant Tax Code": ""
                }
            else:
                for href in response.css("a::attr('href')"):
                    if href.extract().find('professional') > -1:
                        yield response.follow(href, callback=self.parse)