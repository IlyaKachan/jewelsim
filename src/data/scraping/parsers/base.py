from itemloaders.processors import Identity, MapCompose, TakeFirst
from scrapy.loader import ItemLoader
from src.data.scraping.items import Jewel


class JewelLoader(ItemLoader):
    """
    Default loader class for a jewel item, which may potentially be
    overridden for a particular website. The loader class is used inside
    a parser to fill the Jewel instance fields with the extracted data.
    """
    default_item_class = Jewel
    # By default for each field take its first value from the list
    default_output_processor = TakeFirst()

    # Fields for images pipeline must take values of list type, so the
    # behavior of the default output preprocessor is overridden for them
    image_urls_out = Identity()
    images_out = Identity()

    # Convert numeric attributes to float
    price_in = MapCompose(float)
    weight_in = MapCompose(float)
    width_in = MapCompose(float)
    height_in = MapCompose(float)


class BaseJewelParser:
    """
    Abstract base parser class that should be implemented for every
    particular website. This class takes the response from the web
    scraper as input, extracts the required data, and returns the
    jewel instance with the fields filled by the jewel loader.

    The following contact is implicitly assumed:
    - for each jewel field there should be a method, called
      `parse_<field_name>`, for parsing the data for this field
    - the main method, called `parse` by default runs all implemented
      `parse_*` methods and returns the jewel instance.

    For mandatory jewel fields the abstract `parse_*` methods are
    declared in this class.
    """
    loader_cls = JewelLoader

    def __init__(self, response):
        self.response = response
        self.loader = self.loader_cls(response=response)

    def parse_image_urls(self):
        raise NotImplementedError

    def parse_title(self):
        raise NotImplementedError

    def parse_category(self):
        raise NotImplementedError

    def parse_brand(self):
        raise NotImplementedError

    def parse_price(self):
        raise NotImplementedError

    def parse_currency(self):
        raise NotImplementedError

    def parse_sku(self):
        raise NotImplementedError

    def parse_metal(self):
        raise NotImplementedError

    def parse_probe(self):
        raise NotImplementedError

    def parse(self):
        """
        Runs all implemented `parse_*` methods related to the jewel
        fields data parsing and returns the jewel instance filled
        with the parsed data.
        :return: Jewel instance
        """
        for field in self.loader.item.fields.keys():
            getattr(self, f'parse_{field}', lambda: None)()

        return self.loader.load_item()
