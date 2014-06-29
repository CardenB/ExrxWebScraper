# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ExrxItem(Item):
    # define the fields for your item here like:
    title = Field()
    link = Field()

class ExrxCategory(Item):
    # define the fields for your item here like:
    title = Field()
    link = Field()

class ExrxExercise(Item):
    # define the fields for your item here like:
    preparation = Field()
    execution = Field()
    link = Field()
    title = Field()

