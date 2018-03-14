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
            parsedTitle = parsedTitle + " " + re.search('fix-spelling.>[^<]+<', fullTitle).group(0).split(">")[1].split("<")[0]
            parsedTitle = parsedTitle.strip()
        except:
            parsedTitle = fullTitle
        return parsedTitle

    def parsedHandleFromResp(self, response):
        handle = self.parsedTitleFromResp(response)
        #remove stray html
        #handle = re.sub('\([^\)]+\)', "", handle) # delete anything between brackets
        handle = handle.replace(" ", "-") # replace spaces with - 
        handle = handle.replace("/", "-") # replace spaces with - # replace / with - 
        handle = re.sub('[^a-zA-Z0-9-]+', "", handle)# replace anything non alpha-numberic or dashed or space with nothing
        # test with uniq -d
        # only known offender right now is Commercial Carpet Extractor Puzzi
        return handle

    def parsedDescFromResp(self, response):
        description = response.css('#description p').extract_first()
        if description:
            description = description.split('<p property=\"description\">')[1].split('</p>')[0]
        return description

    def parsedCatFromResp(self, response):
        category = response.css('#breadcrumbs li').extract();
        category = category[2].split('property=\"name\">')[1].split('</span')[0]
        return category        

    def parsedSubCatsFromResp(self, response):
        subCategories = response.css('#breadcrumbs li').extract();
        finalCats = []
        for i in range(3,len(subCategories)-1):
            finalCats.append(subCategories[i].split('property=\"name\">')[1].split('</span')[0])
        return str(finalCats)

    def parse(self, response):
        if response.url.find('professional') > -1:
            if response.css('.product-box.product-salesdata'):
                img_url = "https:" + response.css('.product-image a::attr("href")').extract_first()
                yield{
                    #    'technical-data'
                    # 'image_urls': [img_url],
                    # 'productUrl': response.url, 
                    # 'title': self.parsedTitleFromResp(response),
                    # 'description': self.parsedDescFromResp(response),
                    # 'category': self.parsedCatFromResp(response),
                    # 'subcategories': self.parsedSubCatsFromResp(response),
                    
                    # shopify specific tags https://help.shopify.com/manual/products/import-export
                    "Handle": self.parsedHandleFromResp(response),
                    "Title": self.parsedTitleFromResp(response),
                    "Body (HTML)": "<p>"+self.parsedDescFromResp(response)+"</p>",
                    "Vendor": "Karcher",
                    "Type": "cleaning equipment",
                    "Tags": "karcher, equipment,"+self.parsedCatFromResp(response),
                    "Published": "FALSE",
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