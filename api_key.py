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
    '1aab7d76695074b067afe1e91b88e845'
]

new_keys = [
    '070bda52b28e81bc9fd169a31962f766',
    '3378a6a29ed48618213bdfb6d780b308',
    'f629642d65aa1ed5be893d0be5eda5f9',
    '15a83623b372b712e762af311cc0cfa9',
    'd39b28ae36dd641dc9fae76d9683d57b'
]
for i in range(len(keys)):
    print('URL {it}: http://api.scraperapi.com/?api_key={key}&url=https://www.amazon.com'.format(it=i, key=keys[i]))

key_error = [3, 4, 5, 6, 7, 8, 13, 15, 16, 18, 19]  # index from 0
# You're sending requests a bit too fast! Please slow down your requests, or contact support@scraperapi.com with any questions.
