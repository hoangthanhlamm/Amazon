import scrapy


class EmojiSpider(scrapy.Spider):
    name = 'emoji'
    start_urls = ['https://www.unicode.org/emoji/charts/full-emoji-list.html']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 4,
        'DOWNLOAD_DELAY': 4,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
        },
        'FEED_URI': 'Data/emoji.csv',
        'FEED_FORMAT': 'csv'
    }

    def parse(self, response, **kwargs):
        code_rows = response.xpath("//tr/td[@class='code']/a/text()").extract()
        name_rows = response.xpath("//tr/td[@class='name']/text()").extract()
        rows = zip(code_rows, name_rows)

        for code, name in rows:
            codes = code.split(' ')
            if len(codes) <= 1:
                code = None
            code_ = codes[0]
            url = 'https://www.compart.com/en/unicode/' + code_
            yield scrapy.Request(url, callback=self.parse_utf8, cb_kwargs={"code": code_, "name": name, "code_str": code})

    def parse_utf8(self, response, code, name, code_str):
        utf8 = response.xpath("//tr/td[@class='second-column']/code/text()").extract_first()
        yield {
            "code": code,
            "name": name,
            "utf8": utf8,
            "code_str": code_str
        }
