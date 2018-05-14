### Automate Product Scraping from VentureSupply's Vendor Sites

A simple web scraper, written using scrapy.  
Visits vendors sites, scrapes down all of their product information, and prepares a CSV file for upload into shopify.  
  
Supports:
* [Karcher](https://www.kaercher.com/int/)
* [Clarke](http://www.clarkeus.com/)
* [Tork](https://www.torkusa.com/)

#### Installation
`conda install -c conda-forge scrapy`  
`pip install scrapy`  

#### Running
`scrapy runspider clarkeSpider.py -o clarkeSite.json`
  
  
  
For handy debug information, see [this guide](https://www.analyticsvidhya.com/blog/2017/07/web-scraping-in-python-using-scrapy/)
