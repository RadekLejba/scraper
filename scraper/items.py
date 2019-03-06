# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()


class ShopItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    new_price = scrapy.Field()
    old_price = scrapy.Field()
    rating = scrapy.Field()
    features = scrapy.Field()
