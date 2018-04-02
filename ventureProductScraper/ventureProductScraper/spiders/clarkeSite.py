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
    name = 'ClarkeSite'
    start_urls = ['http://www.clarkeus.com/products/autoscrubbers.aspx']

    def inDomain(self, url): # Known Finished
        # tests a domain to see if it should be dropped
        return url.find('products') > -1

    def isProductPage(self, response): #known getting all products
        # Checks if a page has a prodct on it which should be scraped
        return response.css(".reqbutton")

    def getHandle(self, response): #known uniq handles
        urlPieces = response.url.split("/")
        handle = urlPieces[len(urlPieces)-1].split(".aspx")[0]
        handle = handle.replace(" ", "-") # replace spaces with - 
        handle = handle.replace("/", "-") # replace spaces with - # replace / with - 
        handle = re.sub('[^a-zA-Z0-9-]+', "", handle)# replace anything non alpha-numberic or dashed or space with nothing
        return handle

    def getTitle(self, response):
        html = response.css('.titleHolder h1').extract_first()
        title = BeautifulSoup(html, 'lxml').get_text().strip()
        title = re.sub(" +", " ", title) # remove doublespaces
        return title

    def getDesc(self, response):
        # everything up until the first <p> in this the features
        featureDesc = response.css('#middlearea_0_body_0_TabContainer p').extract_first()
        finalArray = []

        htmlArray = response.css('p').extract()
        for p in htmlArray:
            if not p == featureDesc:
                finalArray.append(p)
        return "\n".join(p)

    def getType(self, response):
        return response.url.split("clarkeus.com/products/")[1].split("/")[0]

    def getTags(self, response):
        return ""

    def parse(self, response):
        # yield {
        #     'productUrl': response.url
        # }
        if self.inDomain(response.url):
            if self.isProductPage(response):
                img_url = 'http://www.clarkeus.com' + response.css('img::attr("src")').extract_first()
                yield{
                    #debug
                    'productUrl': response.url, 
                    
                    # shopify specific tags https://help.shopify.com/manual/products/import-export
                    "Handle": self.getHandle(response), # handles and titles with slashes dont work
                    "Title": "Clarke " + self.getTitle(response),  # Make sure vital oxide looks good on shopify
                    "Body (HTML)": "<p>"+self.getDesc(response)+"</p>",
                    "Vendor": "Clarke",
                    "Type": self.getType(response),
                    "Tags": "Clarke, equipment"+self.getTags(response),
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
        for href in response.css("a::attr('href')"):
            if href.extract().find('products') > -1:
                yield response.follow(href, callback=self.parse)