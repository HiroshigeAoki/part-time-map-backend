# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Job(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    deadline = scrapy.Field()
    is_definite = scrapy.Field()
    address = scrapy.Field()
    wages = scrapy.Field()
    type_of_job = scrapy.Field()
    preferences = scrapy.Field()
    es = scrapy.Field() # employment status
    target = scrapy.Field()
    working_hours = scrapy.Field()
    work_period = scrapy.Field()
    loc = scrapy.Field()
    is_loc_accurate = scrapy.Field() # the loc value may be inaccurate
    fetched_date = scrapy.Field()
    jc = scrapy.Field()
    jmc = scrapy.Field()

class Area(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    prefecture = scrapy.Field()
    marea = scrapy.Field()
    sarea = scrapy.Field()
    ssarea = scrapy.Field()
    station = scrapy.Field()
    railway = scrapy.Field()