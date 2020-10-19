keys = [
    '46e9d93fd16dd8983c8af80c8bac5956',
    '4d93f4df40e9ae86c109e6a7c1689341',
    '25761200c37cd6a5b0bf6360dcf9b38b',
    # '7c5bb1dc30778f55281c0c4feff1f0cb',
    # 'ae9cda1957127796b05ca80e0b623a07',
    # '40d242b50d4f9fd637ead3bed48b0d19',
    # '7963f270e2141d3babd4a4ccd5140d9b',
    # '99c005ab73f2bdc1e270b19a3c937ba9',
    # '6b84da20c5269e66732ef743da562936',
    '5b618604415f1bdfb01fe97d0860cc4f',
    'c9a77b3465a08a1179f0d55c65ef3f63',
    '7b6675c9ad56c588dcf2add40b4a9661',
    '3efd8cfc63b953777de6020d068034bd',
    # '18ca07c6a6cfb433727d25534d201ae4',
    '037fb228799dfcad27a6fe179edb5b15',
    # 'af0826ab527d5142c5330f96cc4cf0da',
    # '91c27d8ede24d5762864223ffe4b4456',
    '40b32fce6d5336b1c96b1b52fdb22281',
    # 'd065120943b923fdab6cbc1f4b897e79',
    # '94011a6c8be86faec00380d51b15810f',
    'a3c75c46b5b6f5068ef042350a6ff527',
    '1aab7d76695074b067afe1e91b88e845'  # to get product info
]


def get_product_urls(links, return_id=False):
    if type(links) == str:
        links = [links]

    urls = []
    for link in links:
        # key_idx = ord(product_id[-1]) % 20
        urls.append('http://api.scraperapi.com/?api_key={key}&url=https://www.amazon.com{url}'.format(key=keys[10], url=link))

    if return_id:
        product_ids = []
        for link in links:
            product_id = link.split('/')[3]
            product_ids.append(product_id)
        return urls, product_ids
    return urls


def get_review_meta_urls(product_ids):
    if type(product_ids) == str:
        product_ids = [product_ids]

    urls = []
    for product_id in product_ids:
        urls.append('https://reviewmeta.com/amazon/{product_id}'.format(product_id=product_id))
    return urls


def get_review_urls(review_links, return_id=False):
    if type(review_links) == str:
        review_links = [review_links]

    urls = []
    review_ids = []
    for link in review_links:
        review_id = link.split('/')[5]
        review_ids.append(review_id)
        key_idx = (ord(review_id[-1]) + ord(review_id[-2])) % 10
        urls.append('http://api.scraperapi.com/?api_key={key}&url={url}'.format(key=keys[key_idx], url=link))

    if return_id:
        return urls, review_ids
    return urls


def get_reviewer_url(reviewer_link, return_id=False):
    reviewer_id = reviewer_link.split('/')[3].split('.')[2]
    key_idx = (ord(reviewer_id[-1]) + ord(reviewer_id[-2])) % 10
    url = 'http://api.scraperapi.com/?api_key={key}&url=https://www.amazon.com{url}'.format(key=keys[key_idx], url=reviewer_link)

    if return_id:
        return url, reviewer_id
    return url
