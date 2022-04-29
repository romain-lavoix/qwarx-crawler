from diskcache import FanoutCache

cache = FanoutCache('/tmp/scrapy_cache', shards=1)
