from src.data.scraping.parsers.base import BaseJewelParser, JewelLoader
from src.data.scraping.processors import TakeMax


class SokolovRuJewelLoader(JewelLoader):
    """
    Sokolov.ru jewels sometimes possess length property, which is
    considered as height and appended to the list of height property
    values. In this case height denotes the thickness and is usually
    smaller than the length. We don't need the thickness value to be
    present in height property, so we choose the length by taking the
    maximum over the list of height values.
    """
    height_out = TakeMax()


class SokolovRuJewelParser(BaseJewelParser):
    """
    Parser class for sokolov.ru product pages for mining jewel data.
    All these product pages have two common main blocks:
    - A div of .product class with data-list-id=product attribute.
      Contains main product info: title, price, category, images etc.
    - A div with id=props.
      Contains the detailed description of specific jewel properties:
      physical characteristics (metal, probe, gem inserts, weight,
      width, height, etc.), collection, free-form description etc.
    """
    loader_cls = SokolovRuJewelLoader

    def __init__(self, response):
        super(SokolovRuJewelParser, self).__init__(response)
        # Main product info
        self.product = response.css('.product[data-list-id=product]')
        # Specific product properties
        self.props = response.css('#props')

    def parse_image_urls(self):
        """
        Get main image url from data-src attribute of the image
        marked with contentUrl itemprop attribute.
        """
        urls = self.product.css(
            'img[itemprop=contentUrl]::attr(data-src)'
        ).get()
        self.loader.add_value('image_urls', urls)

    def parse_title(self):
        """Get title from h1 data-detail-name attribute"""
        title = self.product.css('h1::attr(data-detail-name)').get()
        self.loader.add_value('title', title)

    def parse_category(self):
        """
        Get category from the data-detail-category attribute of the
        main div.product block. This attribute value is organized in
        granular way "category / sub-category / sub-sub-category / ...".
        Thus the value is split by slash and the second item is taken,
        if present (since the first item represents too generic name),
        otherwise the default value is returned.
        """
        category = self.product.css(
            '.product[data-list-id=product]::attr(data-detail-category)'
        ).get() or 'Ювелирные украшения'

        categories = category.split('/')
        category = categories[1] if len(categories) > 1 else categories[0]
        self.loader.add_value('category', category)

    def parse_sku(self):
        """Get product id from the meta-tag with sku itemprop"""
        sku = self.product.css('meta[itemprop=sku]::attr(content)').get()
        self.loader.add_value('sku', sku)

    def parse_price(self):
        """Get price from the meta-tag with price itemprop"""
        price = self.product.css('meta[itemprop=price]::attr(content)').get()
        self.loader.add_value('price', price)

    def parse_currency(self):
        """Get currency from the meta-tag with priceCurrency itemprop"""
        currency = self.product.css(
            'meta[itemprop=priceCurrency]::attr(content)'
        ).get()
        self.loader.add_value('currency', currency)

    def parse_description(self):
        """
        There are two types of description provided with sokolov.ru
        products: about the product itself (target one) and about the
        brand (non-relevant). In div#props they are placed in two "tab"
        blocks (or in a single one in case only the brand description
        is provided). Here, the tab names are extracted and the text
        corresponding to the pure product description tab is returned.
        """
        tab_names = self.props.css('.tab-header-item > p::text').getall()
        tab_texts = self.props.css('.props.wrap-text-show > p::text').getall()

        description_tab_name = 'Об украшении'
        if description_tab_name in tab_names:
            description = tab_texts[tab_names.index(description_tab_name)]
            self.loader.add_value('description', description)

    @staticmethod
    def _list_props(element, name_in_span=True, value_in_span=True):
        """
        Iterates over item blocks with names and values in props list
        inside the div#props container and generates (name, value) pairs.
        Each item consists of two divs: one of .name class and another
        one of .val class. These blocks contain names and values of jewel
        properties optionally wrapped with span blocks.
        :param element: scrapy's SelectorList
            The container element of the list of properties.
        :param name_in_span: bool
            Indicator of whether the name is wrapped with a span block.
        :param value_in_span:
            Indicator of whether the value is wrapped with a span block.
        :return:
            Nothing, but (name, value) pairs are generated.
        """
        name_selector = '.name > span::text' if name_in_span else '.name::text'
        value_selector = '.val > span::text' if value_in_span else '.val::text'

        for prop in element.css('.props-list'):
            name = prop.css(name_selector).get() or ''
            value = prop.css(value_selector).get() or ''
            yield name.strip(), value.strip()

    def parse_props_list(self):
        """
        Parse the detailed list of all known jewel properties by
        iterating over the list. Since almost all properties are
        concentrated in a single list, it's more convenient to parse
        them in one method by iterating the entire list rather than
        querying the list for each property separately.
        """
        for name, value in self._list_props(self.props):
            if name == 'Коллекция':
                self.loader.add_value('collection', value)
            elif name == 'Бренд':
                self.loader.add_value('brand', value)
            elif name == 'Для кого':
                self.loader.add_value('for_whom', value)
            elif name == 'Тип металла':
                self.loader.add_value('metal', value)
            elif name == 'Проба':
                self.loader.add_value('probe', value)
            elif name == 'Примерный вес':
                self.loader.add_value('weight', value.split()[0])
            elif name == 'Ширина':
                self.loader.add_value('width', value.split()[0])
            elif name == 'Высота':
                self.loader.add_value('height', value.split()[0])
            elif name == 'Длина':
                # sokolov.ru jewels sometimes also possess length property,
                # in such case height denotes the thickness and is usually
                # smaller than the length. For our purposes, we need only
                # two dimensions: width and height, and so we consider the
                # length as height in such cases.
                self.loader.add_value('height', value.split()[0])

    @staticmethod
    def _compose_gem_description(props):
        """
        Composes a sentence-description of a single certain type of gem
        inserts. The description is a string of the following format
        (square brackets denote optional parts):
        <Gem name>, <amount of gems>[, color: ...][, faceting: ...]
        [, form: ...][, quality: <chromaticity>/<purity>][, weight]
        :param props: dict
            Dictionary of the form gem property name -> property value.
        :return: str, the desired description
        """
        gem_desc_parts = [props['Тип'], props['Количество']]

        if 'Цвет' in props:
            gem_desc_parts.append(f'цвет {props["Цвет"].lower()}')
        if 'Огранка' in props:
            gem_desc_parts.append(f'огранка {props["Огранка"]}')
        if 'Форма' in props:
            gem_desc_parts.append(f'форма {props["Форма"].lower()}')

        if 'Цветность' in props and 'Чистота' in props:
            chromaticity, purity = props['Цветность'], props['Чистота']
            gem_desc_parts.append(f'качество {chromaticity}/{purity}')

        if 'Вес' in props:
            gem_desc_parts.append(f'вес {props["Вес"]}')

        return ', '.join(gem_desc_parts)

    def parse_props_insert(self):
        """
        Iterates over the special type of list of properties - the list
        of gem inserts - and composes the comprehensive description of
        all jewel gems by concatenating the sentences-descriptions of
        individual gems.
        """
        gem_descs = []
        for insert in self.props.css('.props-insert__item'):
            insert_props = dict(self._list_props(insert, name_in_span=False))
            gem_descs.append(self._compose_gem_description(insert_props))

        if gem_descs:
            self.loader.add_value('gems', '. '.join(gem_descs))

    def parse_metal(self):
        # `metal` value is parsed in `parse_props_list`
        pass

    def parse_probe(self):
        # `probe` value is parsed in `parse_props_list`
        pass

    def parse_brand(self):
        # `brand` value is parsed in `parse_props_list`
        pass

    def parse(self):
        """
        Parses the detailed list of jewel properties (including gem
        inserts) first, and all the rest attributes then.
        """
        self.parse_props_list()
        self.parse_props_insert()
        return super(SokolovRuJewelParser, self).parse()
