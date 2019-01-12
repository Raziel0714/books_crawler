# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from pymongo import MongoClient
from scrapy.conf import settings

class MongoDBPipeline(object):
    def __init__(self):
        connection = MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item


"""
class BooksCrawlerPipeline(object):
    def process_item(self, item, spider):
        pass
        
        os.chdir('C:/Users/7huan/Desktop/books_crawler/books_crawler/foobar')
        
        if item['images'][0]['path']:
            file_n = item['title'][0]
            for c in file_n:
                if c == ' ' or c.isalpha():
                    pass
                else:
                    file_n.replace(c, '')
            new_image_name = file_n[0:10] + '.jpg'
            new_image_path = 'full/'+new_image_name
            
            os.rename(item['images'][0]['path'], new_image_path)
        """
