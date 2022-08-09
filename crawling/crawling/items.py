import scrapy


class CrawlingItem(scrapy.Item):
    date = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    labels = scrapy.Field()
    content = scrapy.Field()
