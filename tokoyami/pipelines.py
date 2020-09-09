import re
from urllib.parse import unquote

import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class TokoyamiPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item["image_urls"], meta={"name": item["image_urls"].split("/")[-1], "book_name": item["image_names"]})
        pass

    def file_path(self, request, response=None, info=None):
        name = request.meta.get("name")
        name = re.sub(r'[？\\*|“<>:/]', '', unquote(name))
        book_name = request.meta.get("book_name")
        book_name = re.sub(r'[？\\*|“<>:/]', '', unquote(book_name))
        filename = u'{0}/{1}'.format(book_name, name)
        return filename

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item
