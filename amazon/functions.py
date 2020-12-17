# import requests
# import json

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

# keys = [
#     '070bda52b28e81bc9fd169a31962f766',
#     '3378a6a29ed48618213bdfb6d780b308',
#     'f629642d65aa1ed5be893d0be5eda5f9',
#     '15a83623b372b712e762af311cc0cfa9',
#     'd39b28ae36dd641dc9fae76d9683d57b'
# ]

# keys = [
#     '71fef348d1fab41bc1b243ecdb51b0f3',
#     '71fef348d1fab41bc1b243ecdb51b0f3',
#     '71fef348d1fab41bc1b243ecdb51b0f3',
#     '71fef348d1fab41bc1b243ecdb51b0f3',
#     '71fef348d1fab41bc1b243ecdb51b0f3'
# ]


def get_product_urls(links, return_id=False):
    if type(links) == str:
        links = [links]

    urls = []
    product_ids = []

    # page: 201 to ...
    for link in links:
        product_id = link.split('/')[3]
        product_ids.append(product_id)
        key_idx = (ord(product_id[-1]) + ord(product_id[-2])) % 11
        urls.append('http://api.scraperapi.com/?api_key={key}&url=https://www.amazon.com{url}'.format(key=keys[key_idx], url=link))

    if return_id:
        return urls, product_ids
    return urls


def get_review_meta_urls(product_ids):
    if type(product_ids) == str:
        product_ids = [product_ids]

    urls = []
    for product_id in product_ids:
        urls.append('https://reviewmeta.com/amazon/{product_id}'.format(product_id=product_id))
    return urls


def get_review_urls(review_links, page, return_id=False):
    if type(review_links) == str:
        review_links = [review_links]

    urls = []
    review_ids = []
    for link in review_links:
        review_id = link.split('/')[5]
        review_ids.append(review_id)
        key_idx = (ord(review_id[-1]) + ord(review_id[-2])) % 11  # page: 201 to ...
        if page < 3:
            urls.append('http://api.scraperapi.com/?api_key={key}&url={link}'.format(key=keys[key_idx], link=link))
        else:
            urls.append('http://api.scraperapi.com/?api_key={key}&url=https://www.amazon.com/gp/customer-reviews/{review_id}/ref=cm_cr_dp_d_rvw_ttl?ie=UTF8'.format(key=keys[key_idx], review_id=review_id))

    if return_id:
        return urls, review_ids
    return urls


def get_reviewer_url(reviewer_link, return_id=False):
    reviewer_id = reviewer_link.split('/')[3].split('.')[2]
    key_idx = (ord(reviewer_id[-1]) + ord(reviewer_id[-2])) % 11  # page: 201 to ...
    url = 'http://api.scraperapi.com/?api_key={key}&url=https://www.amazon.com{url}'.format(key=keys[key_idx], url=reviewer_link)

    if return_id:
        return url, reviewer_id
    return url


# def get_proxy():
#     url = 'https://api.getproxylist.com/proxy'
#     try:
#         response = requests.get(url)
#         response = json.loads(response.content.decode('utf-8'))
#         return response['ip']
#     except Exception as err:
#         print(err)
#         return None


def get_next_page(link):
    page_errors = [
        '/s?i=beauty-intl-ship&bbn=16225006011&rh=n%3A16225006011%2Cn%3A11060451&page=81&qid=1603212838&ref=sr_pg_80',
    ]
    prefix = 'http://api.scraperapi.com/?api_key={key}&url=https://www.amazon.com'.format(key=keys[10])  # page: 201 to ...
    if link in page_errors:
        key = keys[9]
        return 'http://api.scraperapi.com/?api_key={key}&url=https://www.amazon.com{url}'.format(key=key, url=link)
    return prefix + link
