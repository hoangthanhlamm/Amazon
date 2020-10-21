# BigData Project Crawler

### Replace this directory in file settings.py (line 53)

```
DELTAFETCH_DIR = '/home/vegeta/Documents/amazon/amazon/delta_fetch'
```

with your directory, ```{your_project_dir}``` is your directory where this project placed (eg. ```/home/vegeta/Documents/amazon```):

```
DELTAFETCH_DIR = '{yours_project_dir}/amazon/delta_fetch
```

### Install packages

```
pip install scrapy scrapy-deltafetch
```

### Run crawler

```
cd {yours_project_dir}
scrapy crawl amazon_v2
```

### If proxy doesn't work success (503 or 403 status code response)

Replaced ```proxy``` in file amazon_v2.py line 9 with another proxy 

