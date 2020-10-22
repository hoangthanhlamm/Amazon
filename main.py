from scrapy.crawler import CrawlerProcess
from amazon.spiders.amazon_v2 import Amazonv2Spider


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(Amazonv2Spider)
    process.start()
