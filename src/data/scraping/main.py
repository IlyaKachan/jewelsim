import click
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.spiderloader import SpiderLoader

from src.data.scraping import config


def scrape(site, log_level='INFO', logstats_interval=10):
    """
    Runs the scraping spider corresponding to the website that walks
    through the website, parses the product data and saves it to the
    data/raw/ folder. The output data is a folder (named as the website
    domain, in which dots are replaced with underscores) that contains:
    - a csv feed file (items.csv) describing all products
      with their attributes;
    - an images/ sub-folder containing images of products.

    The matching between the website domain and its scraping spider is
    based on the scraper's name attribute. Dots in the domain are
    replaced with underscores and the suffix `_spider` is added to the
    result to obtain the scraper's name.

    :param site: str
        The shortest domain name of the website to scrape data from.
    :param log_level: str [DEBUG|INFO|WARNING|ERROR|CRITICAL]
        Minimum level of messages to be written to the log.
    :param logstats_interval: float
        The interval (in seconds) between each logging printout of
        the scraping spider statistics.
    :return: nothing
    """
    scrapy_settings = Settings(dict(
        SPIDER_MODULES=config.SPIDER_MODULES,
        SPIDER_LOADER_WARN_ONLY=config.SPIDER_LOADER_WARN_ONLY,
    ))
    spider_name = site.replace('.', '_') + '_spider'
    spider = SpiderLoader(scrapy_settings).load(spider_name)

    feed_path, images_path = config.get_scraping_output_paths(site)

    process = CrawlerProcess(settings=dict(
        FEEDS={feed_path: config.CSV_FEED_PARAMS},
        ITEM_PIPELINES=config.ITEM_PIPELINES,
        IMAGES_STORE=images_path,
        LOG_LEVEL=log_level,
        LOGSTATS_INTERVAL=logstats_interval,
    ))
    process.crawl(spider)
    process.start()


@click.command('scrape')
@click.option(
    '--site', '-s', type=str, required=True,
    help='The domain name of the website to scrape data from'
)
@click.option(
    '--log-level',
    type=click.Choice([l for num, l in logging._levelToName.items() if num]),
    default='INFO',
    show_default=True,
    help='Minimum level of messages to be written to the log'
)
@click.option(
    '--logstats-interval', type=float, default=10, show_default=True,
    help='The interval (in seconds) between each logging printout '
         'of the scraping spider statistics.'
)
def scrape_cli(site, log_level, logstats_interval):
    """
    Run scraping spider corresponding to the website that walks
    through the website, parses the product data, and saves it to
    the data/raw/ folder.
    """
    scrape(site, log_level, logstats_interval)
