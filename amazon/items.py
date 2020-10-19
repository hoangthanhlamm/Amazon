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
    num_rating = scrapy.Field()
    category = scrapy.Field()


class ReviewItem(scrapy.Item):
    trust = scrapy.Field()
    product_id = scrapy.Field()

    review_id = scrapy.Field()
    review_title = scrapy.Field()
    verified_purchase = scrapy.Field()
    review_content = scrapy.Field()
    review_rating = scrapy.Field()
    num_helpful = scrapy.Field()
    has_image = scrapy.Field()

    reviewer_id = scrapy.Field()
    reviewer_ranking = scrapy.Field()
    # reviewer_helpful = scrapy.Field()
    reviewer_num_review = scrapy.Field()
    reviewer_trust = scrapy.Field()
    reviewer_avg_rating = scrapy.Field()
    reviewer_avg_word_count = scrapy.Field()
    reviewer_num_verified = scrapy.Field()
