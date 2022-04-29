from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "finc"
    allowed_domains = ['finc.nc']
    sitemap_urls = ["https://finc.nc/component/osmap/?view=xml&id=1"]
