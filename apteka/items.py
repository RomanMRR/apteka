# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class AptekaItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    timestamp = Field()
    RPC = Field()
    url = Field()
    title = Field()
    marketing_tags = Field()
    section = Field()
    price_data = Field()
    stock = Field()
    assets = Field()
    metadata = Field()