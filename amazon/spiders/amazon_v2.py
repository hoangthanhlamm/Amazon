import scrapy
from scrapy.loader import ItemLoader
from amazon.items import ProductItem, ReviewItem

from amazon.functions import get_product_urls, get_review_meta_urls, get_review_urls, get_reviewer_url, get_next_page

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
# proxy = 'http://119.15.91.137:50712'
proxy = 'http://43.246.143.74:8080'
# proxy = 'https://43.240.20.84:8080'


class Amazonv2Spider(scrapy.Spider):
    name = 'amazon_v2'
    # start_urls = ['http://api.scraperapi.com/?api_key=7c5bb1dc30778f55281c0c4feff1f0cb&url=https://www.amazon.com/s?i=specialty-aps&bbn=16225006011&rh=n%3A%2116225006011%2Cn%3A11060451&ref=nav_em__nav_desktop_sa_intl_skin_care_0_2_11_3']
    # start_urls = ['http://api.scraperapi.com/?api_key=1aab7d76695074b067afe1e91b88e845&url=https://www.amazon.com/s?i=beauty-intl-ship&bbn=16225006011&rh=n%3A16225006011%2Cn%3A11060451&page=22&qid=1603159869&ref=sr_pg_22']
    # start_urls = ['http://api.scraperapi.com/?api_key=a3c75c46b5b6f5068ef042350a6ff527&url=https://www.amazon.com/s?i=beauty-intl-ship&bbn=16225006011&rh=n%3A16225006011%2Cn%3A11060451&page=81&qid=1603212838&ref=sr_pg_80']
    start_urls = ['http://api.scraperapi.com/?api_key=1aab7d76695074b067afe1e91b88e845&url=https://www.amazon.com/s?i=beauty-intl-ship&bbn=16225006011&rh=n%3A16225006011%2Cn%3A11060451&page=101&qid=1603294332&ref=sr_pg_101']
    MAX_PAGES = 130
    page = 100

    def parse(self, response, **kwargs):
        print('\n\n\nPage: {}\n\n\n'.format(self.page + 1))
        product_xpath = "//div[@class='a-section a-spacing-none a-spacing-top-small']/h2/a[@class='a-link-normal a-text-normal']/attribute::href"
        links = response.xpath(product_xpath).extract()

        product_pages, product_ids = get_product_urls(links, return_id=True)
        # yield from response.follow_all(product_pages, self.parse_product)
        for link in product_pages:
            yield scrapy.Request(link, callback=self.parse_product)

        review_meta_urls = get_review_meta_urls(product_ids)
        # yield from response.follow_all(review_meta_urls, self.parse_review_meta, cb_kwargs={'page': self.page}, meta={"proxy": proxy}, headers=headers)
        for url in review_meta_urls:
            yield scrapy.Request(url, callback=self.parse_review_meta, cb_kwargs={'page': self.page}, meta={"proxy": proxy}, headers=headers)

        self.page += 1
        next_page = response.xpath("//ul[@class='a-pagination']/li[@class='a-last']/a/attribute::href").extract_first()
        # if next_page and self.page < self.MAX_PAGES:
        print("Next page: ", next_page)
        if next_page and self.page < self.MAX_PAGES:
            next_page = get_next_page(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            url = str(response.url)
            f = open('log_errors.txt', 'a+')
            f.writelines(url)
            f.write('\n')
            f.close()

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
            product_loader.add_value('num_rating', '0')
        else:
            product_loader.add_value('rating', get_number(stars))
            product_loader.add_value('num_rating', get_number(no_rate))

        descriptions = response.xpath("//div[@id='feature-bullets']/ul/li/span/text()").extract()
        product_loader.add_value('description', get_description(descriptions))
        product_loader.add_value('category', 'skin care')

        yield product_loader.load_item()

    def parse_review_meta(self, response, page):
        product_id = response.url.split('/')[4]

        good_review_trust = response.xpath("//div[@id='good-reviews']//div[@id='sample_reviews']/div[@class='row well show-checks-user']/div/b/text()").extract()
        good_review_link = response.xpath("//div[@id='good-reviews']//div[@id='sample_reviews']/div[@class='show-actual-review']/a/attribute::href").extract()
        good_reviewer_meta = response.xpath("//div[@id='good-reviews']//div[@id='sample_reviews']/div[@class='row well show-checks-user']/div/label/a/attribute::href").extract()

        bad_review_trust = response.xpath("//div[@id='bad-reviews']//div[@id='sample_reviews']/div[@class='row well show-checks-user']/div/b/text()").extract()
        bad_review_link = response.xpath("//div[@id='bad-reviews']//div[@id='sample_reviews']/div[@class='show-actual-review']/a/attribute::href").extract()
        bad_reviewer_meta = response.xpath("//div[@id='bad-reviews']//div[@id='sample_reviews']/div[@class='row well show-checks-user']/div/label/a/attribute::href").extract()

        n_review = 5
        review_trusts = good_review_trust[:n_review] + bad_review_trust[:n_review]
        review_links = good_review_link[:n_review] + bad_review_link[:n_review]
        reviewer_meta_links = good_reviewer_meta[:n_review] + bad_reviewer_meta[:n_review]

        # yield from response.follow_all(review_links, callback=self.parse_review, meta={'review_trust': review_trusts})
        urls, review_ids = get_review_urls(review_links, page, return_id=True)
        for i in range(len(urls)):
            # proxy_ip = get_proxy()
            yield scrapy.Request(urls[i],
                                 callback=self.parse_review,
                                 cb_kwargs={'trust': review_trusts[i], 'review_id': review_ids[i], 'product_id': product_id, 'reviewer_meta_link': reviewer_meta_links[i]})

    def parse_review(self, response, trust, review_id, product_id, reviewer_meta_link):
        title = response.xpath("//a[@data-hook='review-title']/span/text()").extract_first()
        content = response.xpath("//span[@data-hook='review-body']/span/text()").extract()

        review_content = ''
        if content:
            review_content = get_review_content(content)

        stars = response.xpath("//i[@data-hook='review-star-rating']/span/text()").extract_first()
        rating = '5.0'
        if stars:
            rating = stars.split(' ')[0]
        verify = response.xpath("//span[@data-hook='avp-badge']/text()").extract_first()
        verified_purchase = False
        if verify == 'Verified Purchase':
            verified_purchase = True

        helpful = response.xpath("//span[@data-hook='helpful-vote-statement']/text()").extract_first()
        num_helpful = '0'
        if helpful:
            num_helpful = helpful.split(' ')[0].replace(',', '')
            if num_helpful == 'One':
                num_helpful = '1'
        image = response.xpath("//img[@data-hook='review-image-tile']").extract_first()
        has_image = False
        if image:
            has_image = True

        reviewer_link = response.xpath("//div[@data-hook='genome-widget']/a/attribute::href").extract_first()
        reviewer_url, reviewer_id = get_reviewer_url(reviewer_link, return_id=True)
        review_info = {
            'review_id': review_id,
            'trust': trust,
            'product_id': product_id,
            'reviewer_id': reviewer_id,
            'review_title': title,
            'review_content': review_content,
            'review_rating': rating,
            'num_helpful': num_helpful,
            'verified_purchase': verified_purchase,
            'has_image': has_image
        }
        yield scrapy.Request(reviewer_url, callback=self.parse_reviewer, cb_kwargs={'review_info': review_info, 'reviewer_meta_link': reviewer_meta_link})

    def parse_reviewer(self, response, review_info, reviewer_meta_link):
        response_text = response.text
        reviewer_ranking = get_reviewer_ranking(response_text)
        review_info['reviewer_ranking'] = reviewer_ranking

        yield scrapy.Request(reviewer_meta_link,
                             callback=self.parse_review_meta_reviewer,
                             cb_kwargs={'review_info': review_info},
                             meta={"proxy": proxy},
                             headers=headers)

    def parse_review_meta_reviewer(self, response, review_info):
        reviewer_trust = response.xpath("//div[@class='row']/div[@class='col-md-4']/div/b/text()").extract_first()
        metrics = response.xpath("//div[@class='row']/div[@class='col-xs-2 col-sm-1 text-right']/b/text()").extract()

        review_info['reviewer_trust'] = reviewer_trust
        review_info['reviewer_num_review'] = metrics[0]
        review_info['reviewer_num_verified'] = metrics[1]
        review_info['reviewer_avg_rating'] = metrics[3]
        review_info['reviewer_avg_word_count'] = metrics[4]

        review_loader = ItemLoader(item=ReviewItem(), response=response)
        review_loader_add_value(review_loader, review_info)
        yield review_loader.load_item()


def wraptext(s):
    if not s:
        return ''
    return s.strip()


def get_review_content(content):
    if type(content) == str:
        return wraptext(content)

    review_content = ''
    for p_ in content:
        review_content += wraptext(p_)
        review_content += ' '
    return wraptext(review_content)


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


def get_reviewer_ranking(text):
    try:
        loc = text.index("decoratedRank") + 17
        subtext = text[loc:loc + 15]
        reviewer_ranking = subtext.split('"')[0]
        return reviewer_ranking.replace(',', '')
    except ValueError as err:
        print(err)
        return '0'


def review_loader_add_value(review_loader, review_info):
    keys = ['product_id', 'trust', 'review_id', 'review_title', 'review_content', 'verified_purchase', 'review_rating', 'num_helpful', 'has_image', 'reviewer_id', 'reviewer_ranking', 'reviewer_num_review', 'reviewer_trust', 'reviewer_avg_rating', 'reviewer_avg_word_count', 'reviewer_num_verified']
    for key in keys:
        review_loader.add_value(key, review_info[key])
