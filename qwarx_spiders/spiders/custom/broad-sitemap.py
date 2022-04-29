from ..base import BaseSpider
from ...utils.qwarx_sitemap_spider import QwarxSitemapSpider


class Spider(QwarxSitemapSpider, BaseSpider):
    name = "broad-sitemap"
    allowed_domains = ['ac-noumea.nc', 'annuaire-web.nc', 'cci.nc', 'cen.nc', 'finc.nc', 'idcnc.nc', 'jeux-concours.nc', 'lacasserolette.nc', 'ldhnc.nc', 'legiscal.com', 'maisondulivre.nc', 'manga.nc', 'mapara.nc', 'materiaux.nc', 'medicalequipement.nc', 'meubles-import.nc', 'monepiceriesante.nc', 'paita.nc', 'opt.nc', 'service-public.nc', 'sipa.nc', 'ville-dumbea.nc']
    sitemap_urls = ["http://cio.ac-noumea.nc/sitemap.xml",
                    "http://lettres.ac-noumea.nc/sitemap.xml",
                    "http://webportesdefer.ac-noumea.nc/sitemap.xml",
                    'http://assistance.ac-noumea.nc//sitemap.xml',
                    'http://webboulari.ac-noumea.nc/sitemap.xml',
                    'http://webattiti.ac-noumea.nc/sitemap.xml',
                    'http://eps.ac-noumea.nc/sitemap.xml',
                    'http://webnormandie.ac-noumea.nc/sitemap.xml',
                    'http://documentation.ac-noumea.nc/sitemap.xml',
                    'http://webmariotti.ac-noumea.nc/sitemap.xml',
                    'http://eps.ac-noumea.nc/sitemap.xml',
                    'http://webnormandie.ac-noumea.nc/sitemap.xml',
                    'http://webrs.ac-noumea.nc/sitemap.xml',
                    'https://www.annuaire-web.nc/robots.txt',
                    "https://www.cci.nc/sitemap.xml",
                    "http://www.cen.nc/sitemap.xml",
                    "https://finc.nc/robots.txt",
                    "http://idcnc.nc/sitemap.xml",
                    "https://www.jeux-concours.nc/sitemap.xml",
                    "http://www.lacasserolette.nc/sitemap.xml",
                    "http://www.ldhnc.nc/sitemap.xml",
                    "https://legiscal.com/sitemap_index.xml",
                    "http://maisondulivre.nc/sitemap.xml",
                    "https://manga.nc/robots.txt",
                    "https://www.mapara.nc/sitemap_index.xml",
                    "https://www.materiaux.nc/sitemap_index.xml",
                    'http://medicalequipement.nc/sitemap.xml',
                    'http://meubles-import.nc/sitemap_index.xml',
                    'https://www.monepiceriesante.nc/sitemap.xml',
                    'http://paita.nc/sitemap_index.xml',
                    'https://www.opt.nc/sitemap.xml',
                    'https://service-public.nc/sitemap.xml',
                    'http://www.sipa.nc/sitemap.xml',
                    'http://www.ville-dumbea.nc/sitemap.xml']
