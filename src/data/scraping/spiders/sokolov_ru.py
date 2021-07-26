from scrapy.spiders import SitemapSpider
from src.data.scraping.parsers.sokolov_ru import SokolovRuJewelParser


class SokolovRuSpider(SitemapSpider):
    """
    Scraping spider class for sokolov.ru that iterates over the
    product webpages listed in the sitemap and parses jewel product
    data from these webpages.
    """
    name = 'sokolov_ru_spider'
    allowed_domains = ['sokolov.ru']
    sitemap_urls = ['https://sokolov.ru/sitemap.xml']
    # All product pages share a common prefix /jewelry-catalog/product
    sitemap_rules = [('/jewelry-catalog/product/', 'parse_product')]

    def parse_product(self, response):
        yield SokolovRuJewelParser(response).parse()

    def parse(self, response, **kwargs):
        # Do nothing, all products will be parsed by `parse_product`
        pass

    @staticmethod
    def is_sitemap_url(url):
        return url.endswith('.xml')

    @staticmethod
    def is_product_url(url):
        # Remove scheme from URL
        route = url.split('//')[-1]
        # Cut domain from the route
        domain = route.split('/')[0]
        route = route.replace(domain, '', 1)

        product_prefix, _ = SokolovRuSpider.sitemap_rules[0]
        return route.startswith(product_prefix)

    def sitemap_filter(self, entries):
        for entry in entries:
            url = entry['loc']
            if self.is_sitemap_url(url) or self.is_product_url(url):
                yield entry
