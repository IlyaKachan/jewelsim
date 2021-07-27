from pathlib import Path

# Overwrite CSV files by default, do not append new data
CSV_FEED_PARAMS = {'format': 'csv', 'overwrite': True}
# Use custom pipeline class that controls image-related attributes
ITEM_PIPELINES = {'src.data.scraping.pipelines.SimpleImagesPipeline': 1}

# The name of the package containing this file (in dot notation)
SCRAPING_PACKAGE_NAME = '.'.join(__name__.split('.')[:-1])
# The path to the folder containing this file
SCRAPING_PACKAGE_PATH = Path(__file__).parent

# The list of modules where Scrapy will look for spiders.
# This list consists of the modules in a `spiders` package
SPIDER_MODULES = [
    f'{SCRAPING_PACKAGE_NAME}.spiders.{file_path.stem}'
    for file_path in Path(SCRAPING_PACKAGE_PATH, 'spiders').glob('*.py')
    if file_path.name != '__init__.py'
]
# Make Scrapy failing with ImportError in case the spider
# is not found in `SPIDER_MODULES`
SPIDER_LOADER_WARN_ONLY = False


def get_scraping_output_paths(site):
    """
    Return paths to the scraping output files (relative to the
    project root):
    data/raw/<site_py>/items.csv - csv feed path,
    data/raw/<site_py>/images/ - the path of the folder with images.

    Here, <site_py> is the shortest website domain, in which dots are
    replaced with underscores.

    :param site: str
        The shortest domain name of the website to scrape data from.
    :return: tuple (str, str)
        CSV feed path and image folder path, respectively.
    """
    site_py = site.replace('.', '_')
    raw_data_path = Path('data', 'raw_new')
    feed_path = Path(raw_data_path, site_py, 'items.csv')
    images_path = Path(raw_data_path, site_py, 'images')
    return str(feed_path), str(images_path)
