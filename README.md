# BigData Project Crawler

### Configuration

Replace this directory in file amazon_v2.py (line 40)

```
'DELTAFETCH_DIR': '/home/vegeta/Documents/amazon/amazon/delta_fetch'
```

with your directory, ```{your_project_dir}``` is your directory where this project placed (eg. ```/home/vegeta/Documents/Amazon```):

```
'DELTAFETCH_DIR': '{yours_project_dir}/amazon/delta_fetch
```

### Install packages

```
pip install scrapy scrapy-deltafetch
```

#### If install ```scrapy-deltafetch``` error, run 

```
sudo apt install libdb-dev
pip3 install bsddb3
```

### Run crawler

```
cd {yours_project_dir}
python3 main.py
```

### If proxy doesn't work success (503 or 403 status code response)

Replaced ```proxy``` in file amazon_v2.py line 9 with another proxy 

