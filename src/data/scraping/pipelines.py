from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class SimpleImagesPipeline(ImagesPipeline):
    """
    A slight modification of the default images pipeline in such way
    that `images` item field is filled only with the local paths of
    images and not with dicts of paths, urls, download statuses etc.
    """
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        adapter = ItemAdapter(item)
        adapter['images'] = image_paths
        return item
