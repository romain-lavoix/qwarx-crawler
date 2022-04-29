import logging
logging.getLogger('boto').setLevel(logging.CRITICAL)
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('oauth2client').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

AWS_ACCESS_KEY_ID = 'AKIAIAR3LOUEJBSUNZRQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_REGION = 'ap-southeast-2'

# AWS SQS settings
AWS_SQS_QUEUE_NAME = 'algolia-items'
# Number of item to send at once to the SQS queue
ALGOLIA_CHUNK_SIZE = 200

ALGOLIA_SEARCH_APP_ID = '5NXUF7YDRN'
ALGOLIA_SEARCH_APP_KEY = 'ce00544c03c7016cbf0e45e976d8a6d2'
ALGOLIA_SEARCH_INDEX = 'qwarx.nc'
ALGOLIA_DOMAINS_INDEX = 'qwarx_domains.nc'
# Option to pass if you want to reset algolia data related to this spider
ALGOLIA_RESET_SPIDER_DATA = False

# Define here the domain score file from S3
DOMAIN_SCORE_BUCKET = 'qwarx-parameters'
DOMAIN_SCORE_FILENAME = 'domains_scores.jl'
# Define here the domain score file from S3
DOMAIN_CATEGORY_BUCKET = 'qwarx-parameters'
DOMAIN_CATEGORY_FILENAME = 'domains_categories.jl'

# Google Sheet key where we store information about domains and categories
QWARX_DB_GSHEET_KEY = '1zWpJCr51JF2YgwQQ6eEKvjPNaoceZvG_ehzzhUdLtBE'

SPIDER_MODULES = ['qwarx_spiders.spiders.broad', 'qwarx_spiders.spiders.custom', 'qwarx_spiders.spiders.check']
NEWSPIDER_MODULE = 'qwarx_spiders.spiders'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'qwarx_spiders.downloadermiddlewares.canonical.RelCanonicalMiddleware': 50,
    # 'qwarx_spiders.downloadermiddlewares.deltafetch.DeltaFetchKeyUrlMiddleware': 200,
    'qwarx_spiders.downloadermiddlewares.rotate_user_agent.RotateUserAgentMiddleware': 100,
}

SPIDER_MIDDLEWARES = {
    'scrapy_deltafetch.DeltaFetch': 300,
}

ITEM_PIPELINES = {
    'qwarx_spiders.pipelines.duplicates.DuplicatesPipeline': 400,
    'qwarx_spiders.pipelines.item_categorization.ItemCategorizationPipeline': 401,
    'qwarx_spiders.pipelines.reset_db.ResetSpiderDataPipeline': 402,
}

BOT_NAME = 'Qwarxbot'

USER_AGENT = 'Qwarxbot/1.0 (+https://qwarx.nc)'

ROBOTSTXT_OBEY = True
LOG_LEVEL = 'INFO'

CONCURRENT_REQUESTS = 512
CONCURRENT_REQUESTS_PER_DOMAIN = 8

COOKIES_ENABLED = False
REDIRECT_ENABLED = False
AJAXCRAWL_ENABLED = False
DOWNLOAD_TIMEOUT = 60
REACTOR_THREADPOOL_MAXSIZE = 20
RETRY_ENABLED = False
# DELTAFETCH PARAMS
DELTAFETCH_ENABLED = True
DOTSCRAPY_ENABLED = True

URLLENGTH_LIMIT = 180

USER_AGENT_CHOICES = [
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:23.0) Gecko/20100101 Firefox/23.0 (compatible; Qwarxbot/1.0; +https://qwarx.nc)',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36 (compatible; Qwarxbot/1.0; +https://qwarx.nc)',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36 (compatible; Qwarxbot/1.0; +https://qwarx.nc)',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36 (compatible; Qwarxbot/1.0; +https://qwarx.nc)',
    'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20140205 Firefox/24.0 Iceweasel/24.3.0 (compatible; Qwarxbot/1.0; +https://qwarx.nc)',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0 (compatible; Qwarxbot/1.0; +https://qwarx.nc)',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 (compatible; Qwarxbot/1.0; +https://qwarx.nc)',
]

ADDONS_AWS_ACCESS_KEY_ID = 'AKIAIAR3LOUEJBSUNZRQ'
ADDONS_AWS_SECRET_ACCESS_KEY = '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'
ADDONS_S3_BUCKET = 'qwarx-dotscrapy'