from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider):
    name = "guillaumefenollar"
    allowed_domains = ['guillaume.fenollar.fr']
    sitemap_urls = ["https://guillaume.fenollar.fr/sitemap.xml"]
