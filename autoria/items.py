# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item


class AutoriaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CarItem(Item):
    model = scrapy.Field()
    year = scrapy.Field()
    mileage = scrapy.Field()
    price_ua = scrapy.Field()
    price_dollar = scrapy.Field()
    link = scrapy.Field()
    vin_code = scrapy.Field()
