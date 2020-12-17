from scrapy.crawler import CrawlerProcess
from amazon.spiders.amazon_v2 import Amazonv2Spider
from amazon.spiders.emoji import EmojiSpider

import time


if __name__ == "__main__":
    # while True:
    process = CrawlerProcess()
    process.crawl(Amazonv2Spider)
    process.start()
    # time.sleep(3600 * 24)
