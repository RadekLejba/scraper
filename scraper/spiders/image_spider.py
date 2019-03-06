import os
from urllib.parse import urljoin

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scraper.items import ImageItem

fileDir = os.path.dirname(os.path.realpath('__file__'))


RULES = {
    "start_urls": ["https://www.x-kom.pl/g-13/c/1291-monitory-led-27-28-9.html"],
    "allow": r"\.",
    "xpath": "//div[@class='pagination-wrapper']//a",
    "deny": [],
}

IMAGES = '//img/@src'


class ImageSpider(CrawlSpider):
    name = 'images'
    rules = [
        Rule(
            LinkExtractor(
                allow=RULES["allow"],
                restrict_xpaths=RULES["xpath"],
                deny=RULES["deny"],
            ),
            callback='parse_item',
            follow=True,
        ),
    ]

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)
        self.word = kwargs.get('word', '')

        self.parse_rules()

    def parse_rules(self):
        self.start_urls = [url for url in RULES['start_urls']]

    def parse_item(self, response):
        img_urls = [
            urljoin(response.url, src) for
            src in response.xpath(IMAGES).extract()
        ]
        image_item = ImageItem()
        image_item['image_urls'] = img_urls
        return image_item
