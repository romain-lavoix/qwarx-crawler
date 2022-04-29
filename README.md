QWARX Spiders
=============


Reset Algolia spider data
=========================
Each spider does insert into algolia a field called 'spider_name'. When we want to reset all data related to a spider
we can use spider argument like this:

```bash
scrapy crawl spider_name -a algolia_reset_spider_data=1
```

Or you can as well use scrapy settings for it

```bash
scrapy crawl spider_name -s ALGOLIA_RESET_SPIDER_DATA=1
```
