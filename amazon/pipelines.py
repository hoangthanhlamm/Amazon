# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter


class AmazonPipeline:
    def process_item(self, item, spider):
        return item


class MultiCSVItemPipeline:
    SaveTypes = ['product', 'review']

    def __init__(self):
        self.files = dict([(name, open('Data/' + name + '.csv', 'w+b')) for name in self.SaveTypes])
        # self.exporters = dict([(name, CsvItemExporter(self.files[name], include_headers_line=False)) for name in self.SaveTypes])
        self.exporters = dict([(name, CsvItemExporter(self.files[name])) for name in self.SaveTypes])

    def spider_opened(self, spider):
        [e.start_exporting() for e in self.exporters.values()]

    def spider_closed(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):
        what = item_type(item)
        if what in set(self.SaveTypes):
            self.exporters[what].export_item(item)
        return item


def item_type(item):
    return type(item).__name__.replace('Item', '').lower()
