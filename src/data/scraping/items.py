from scrapy.item import Item, Field


class Jewel(Item):
    """Container class for storing jewel properties."""
    # Free-form, but sufficiently short jewel title (string)
    title = Field()
    # Optional free-form jewel textual description (string)
    description = Field()
    # Jewel category, e.x. ring, pendant, bracelet etc.
    # (string from the finite set of values)
    category = Field()
    # Jewel brand or manufacturer name (string)
    brand = Field()
    # Jewel price (float)
    price = Field()
    # The currency of the jewel price, e.x. RUB, BYN
    # (string from the finite set of values)
    currency = Field()
    # Manufacturer's internal identifier of a jewel (string)
    sku = Field()
    # Jewel weight in grams (float number)
    weight = Field()
    # Jewel width in millimeters (float number)
    width = Field()
    # Jewel height in millimeters (float number)
    height = Field()
    # Metal from which the jewel is made, e.x. gold, silver
    # (string from the finite set of values)
    metal = Field()
    # The probe of the jewel method, e.x. 375, 585, 925
    # (string from the finite set of values)
    probe = Field()
    # Target type of jewelry owner: women, men, children, etc.
    # (string from the finite set of values)
    for_whom = Field()
    # Textual description of gem inserts, if any (structured string)
    gems = Field()
    # Name of the collection the jewel belongs to, if any (string)
    collection = Field()
    # The list of jewel image urls (list of strings)
    image_urls = Field()
    # Auto-filled filed containing a local paths to jewel images
    # (list of strings)
    images = Field()
