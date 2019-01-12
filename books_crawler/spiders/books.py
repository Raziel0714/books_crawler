# -*- coding: utf-8 -*-
#from scrapy.spiders import CrawlSpider, Rule
#from scrapy.linkextractors import LinkExtractor
#from time import sleep

import os
import csv
import glob
from scrapy import Spider
#from selenium import webdriver
#from scrapy.selector import Selector
from scrapy.http import Request
#from selenium.common.exceptions import NoSuchElementException

from books_crawler.items import BooksCrawlerItem
from scrapy.loader import ItemLoader

"""
def product_description(response, value):
    return response.xpath('//th[text()="' + value + '"]/following-sibling::td/text()').extract_first()
"""
class BooksSpider(Spider):
    name = 'books'
    allow_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']

    """
    def __init__(self, category):
        self.start_urls = [category]
    """

    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            absolute_url = response.urljoin(book)
            yield Request(absolute_url, callback=self.parse_book)

        # process next page
        #next_page_url = response.xpath('//a[text()="next"]/@href').extract_first()
        #absolute_next_page_url = response.urljoin(next_page_url)
        #yield Request(absolute_next_page_url)

    def parse_book(self, response):
        l = ItemLoader(item=BooksCrawlerItem(), response=response)
        title = response.css('h1::text').extract_first()
        price = response.xpath('//*[@class="price_color"]/text()').extract_first()

        image_urls = response.xpath('//img/@src').extract_first()
        image_urls = image_urls.replace('../..', 'http://books.toscrape.com/')

        l.add_value('title', title)
        l.add_value('price', price)
        l.add_value('image_urls', image_urls)

        return l.load_item()

        """
        rating = response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
        rating = rating.replace('star-rating ', '')

        description = response.xpath('//*[@id="product_description"]/following-sibling::p/text()').extract_first()

        # product information data points

        upc = product_description(response, 'UPC')
        product_type = product_description(response, 'Product Type')
        price_without_tax = product_description(response, 'Price (excl. tax)')
        price_with_tax = product_description(response, 'Price (incl. tax)')
        tax = product_description(response, 'Tax')
        availability = product_description(response, 'Availability')
        number_of_reviews = product_description(response, 'Number of reviews')

        yield{
            'title': title,
            'price': price,
            'image_url': image_url,
            'rating': rating,
            'description': description,
            'upc': upc,
            'product_type': product_type,
            'price_without_tax': price_without_tax,
            'price_with_tax': price_with_tax,
            'tax': tax,
            'availability': availability,
            'number_of_reviews': number_of_reviews
        }

    def close(self, reason):
        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)
        os.rename(csv_file, 'foobar.csv')

    """
    """
    name = "books"
    allowed_domains = ['books.toscrape.com']

    def start_requests(self):
        self.driver = webdriver.Chrome('C:/Users/7huan/Desktop/chromedriver')
        self.driver.get('http://books.toscrape.com')

        sel = Selector(text=self.driver.page_source)
        books = sel.xpath('//h3/a/@href').extract()

        for book in books:
            url = 'http://books.toscrape.com/' + book
            yield Request(url, callback=self.parse_book)
        a = 1

        while a < 3:
            a += 1
            try:
                next_page = self.driver.find_element_by_xpath('//a[text()="next"]')
                sleep(3)
                self.logger.info('Sleeping for 3 seconds')
                next_page.click()

                sel = Selector(text=self.driver.page_source)
                books = sel.xpath('//h3/a/@href').extract()
                for book in books:
                    url = 'http://books.toscrape.com/catalogue/' + book
                    yield Request(url, callback=self.parse_book)

            except NoSuchElementException:
                self.logger.info('No more pages to load.')
                self.driver.quit()
                break
    
    def parse_book(self, response):
        items = BooksCrawlerItem()
        title = response.css('h1::text').extract_first()
        url = response.request.url

        items['title'] = title
        items['url'] = url
        yield items
    """
    #start_urls = ['http://books.toscrape.com/']

    #rules = (Rule(LinkExtractor(deny_domains=('google.com')), callback='parse', follow=False),)
    #rules = (Rule(LinkExtractor(allow=('music')), callback='parse', follow=False),)

    #def parse_page(self, response):
    #    pass
