from scrapy import cmdline
cmdline.execute("scrapy crawl immonc -a deltafetch_reset=1".split())
