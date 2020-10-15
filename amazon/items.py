# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ProductItem(scrapy.Item):
    product_id = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    rating = scrapy.Field()
    no_rating = scrapy.Field()


class ReviewItem(scrapy.Item):
    product_id = scrapy.Field()
    reviewer_id = scrapy.Field()
    review_content = scrapy.Field()
    review_rating = scrapy.Field()
    helpful = scrapy.Field()
    # reviewer_ranking = scrapy.Field()
