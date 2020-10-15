import scrapy
from scrapy.loader import ItemLoader
from amazon.items import ProductItem, ReviewItem


class StayhomesSpider(scrapy.Spider):
    name = 'amazons'
    # start_urls = ['http://api.scraperapi.com/?api_key=b15018d515cd673cebec34bf4449b5ea&url=https://www.amazon.com/s?i=specialty-aps&bbn=16225006011&rh=n%3A%2116225006011%2Cn%3A11060451&ref=nav_em__nav_desktop_sa_intl_skin_care_0_2_11_3']
    start_urls = ['http://api.scraperapi.com/?api_key=b15018d515cd673cebec34bf4449b5ea&url=https://www.amazon.com/s?i=beauty-intl-ship&bbn=16225006011&rh=n%3A16225006011%2Cn%3A11060451&page=52&qid=1602530829&ref=sr_pg_51']
    # MAX_PAGES = 400
    page = 0

    def parse(self, response, **kwargs):
        print('\n\n\nPage: {}\n\n\n'.format(self.page + 1))
        product_xpath = "//div[@class='a-section a-spacing-none a-spacing-top-small']/h2/a[@class='a-link-normal a-text-normal']/attribute::href"
        links = response.xpath(product_xpath).extract()

        product_pages = get_url(links)
        yield from response.follow_all(product_pages, self.parse_product)

        self.page += 1
        next_page = response.xpath("//ul[@class='a-pagination']/li[@class='a-last']/a/attribute::href").extract_first()
        # if next_page and self.page < self.MAX_PAGES:
        print("Next page: ", next_page)
        if next_page:
            print(next_page)
            yield scrapy.Request(get_url(next_page), callback=self.parse)

    def parse_product(self, response):
        product_loader = ItemLoader(item=ProductItem(), response=response)

        product_id = response.xpath("//*[@data-asin]/attribute::data-asin").extract_first()
        product_loader.add_value('product_id', product_id)

        product_name = response.xpath("//div[@id='titleSection']/h1/span[@id='productTitle']/text()").extract_first()
        product_loader.add_value('name', wraptext(product_name))

        stars = response.xpath("//a[@class='a-popover-trigger a-declarative']/i/span[ @class ='a-icon-alt']/text()").extract_first()

        no_rate = response.xpath("//a[@id='acrCustomerReviewLink']/span[@id='acrCustomerReviewText']/text()").extract_first()
        if no_rate is None:
            product_loader.add_value('rating', None)
            product_loader.add_value('no_rating', '0')
        else:
            product_loader.add_value('rating', get_number(stars))
            product_loader.add_value('no_rating', get_number(no_rate))

        descriptions = response.xpath("//div[@id='feature-bullets']/ul/li/span/text()").extract()
        product_loader.add_value('description', get_description(descriptions))

        yield product_loader.load_item()

        # crawl reviews
        reviewers_ = response.xpath("//div[@data-hook='genome-widget']/a[@class='a-profile']/attribute::href").extract()
        reviewer_ids = []
        for reviewer in reviewers_:
            reviewer = reviewer.split('/')[3]
            reviewer_id = reviewer.split('.')[2]
            reviewer_ids.append(reviewer_id)
        no_of_reviews = len(reviewer_ids)

        review_contents = []
        for tag in response.xpath("//div[@data-hook='review-collapsed']/span"):
            content = tag.xpath("string(.)").extract()
            review_contents.append(wraptext(content[0]))
        review_contents = remove_empty_string(review_contents)[:no_of_reviews]

        ratings = response.xpath("//i[@data-hook='review-star-rating']/span/text()").extract()
        review_ratings = []
        for rate in ratings:
            review_ratings.append(rate.split(' ')[0])
        review_ratings = review_ratings[:no_of_reviews]

        helpful = response.xpath("//span[@data-hook='helpful-vote-statement']/text()").extract()
        review_helpful = []
        for h in helpful:
            hf = h.split(' ')[0].replace(',', '')
            if hf == 'One':
                hf = '1'
            review_helpful.append(hf)
        review_helpful = review_helpful[:no_of_reviews]

        reviews = zip(reviewer_ids, review_contents, review_ratings, review_helpful)
        for review in reviews:
            review_loader = ItemLoader(item=ReviewItem(), response=response)
            review_loader.add_value('product_id', product_id)
            review_loader.add_value('reviewer_id', review[0])
            review_loader.add_value('review_content', review[1])
            review_loader.add_value('review_rating', review[2])
            review_loader.add_value('helpful', review[3])
            yield review_loader.load_item()

    def parse_user(self, response):
        pass


def get_url(urls):
    prefix = 'http://api.scraperapi.com/?api_key=b15018d515cd673cebec34bf4449b5ea&url=https://www.amazon.com'
    if type(urls) == str:
        return prefix + urls

    scraper_url = []
    for url in urls:
        scraper_url.append(prefix + url)
    return scraper_url


def wraptext(s):
    return s.strip()


# get rating or number of rating from string
def get_number(s):
    s = s.split(' ')[0]
    s = s.replace(',', '')
    return s


# get description
def get_description(descriptions):
    s = ''
    for description in descriptions:
        s_ = description.strip() + ' '
        s += s_
    return s


def remove_empty_string(list_str):
    for s in list_str:
        if s == '':
            list_str.remove(s)
    return list_str
