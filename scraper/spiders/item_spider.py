import os

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scraper.items import ShopItem


fileDir = os.path.dirname(os.path.realpath('__file__'))
RULES = {
    "start_urls": ["https://www.x-kom.pl/g-12/c/442-klawiatury-przewodowe.html"],
    "allow": r"\.",
    "xpath": "//div[@class='pagination ']//a[@class='next']",
    "deny": [],
}

ITEM = {
    # Container with item
    'container': '//div[@class="product-item product-impression"]',
    # Element with url to item page
    'url': {
        'main': 'https:/www.x-kom.pl',
        'xpath': 'a//@href',
    },
    # Element with item rating
    'rating': 'div//a[@class="rating-bar text-nowrap js-scroll-top"]/@title',
    # Element with item features
    'features': 'div//div[@class="features"]//ul//@title',
    # Element with item name
    'name': 'div//a//@title',
    # Element with item price
    'price': 'div//div[@class="prices"]//span[@class="price text-nowrap"]/text'
             '()',
    # Element with optional old item price
    'old_price': 'div//div[@class="prices"]//span[@class="previous-price text-'
                 'nowrap"]/text()',
    # Element with optional new item price
    'new_price': 'div//div[@class="prices"]//span[@class="price text-nowrapnew'
                 '-price"]/text()',
    'image': 'a//img//@src'
}


class ItemSpider(CrawlSpider):
    name = 'items'
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
        super(ItemSpider, self).__init__(*args, **kwargs)
        self.parse_rules()

    def safe_list_get(self, list):
        try:
            return list[0]
        except IndexError:
            return ''

    def parse_rules(self):
        self.start_urls = [url for url in RULES['start_urls']]

    def parse_item(self, response):
        items = response.xpath(ITEM['container'])

        for item in items:
            shop_item = ShopItem()
            shop_item['url'] = (
                ITEM['url']['main'] +
                self.safe_list_get(
                    item.xpath(ITEM['url']['xpath']).extract()
                )
            )
            shop_item['rating'] = self.safe_list_get(
                item.xpath(ITEM['rating']).extract()
            )
            shop_item['features'] = (
                self.safe_list_get(
                    item.xpath(ITEM['features']).extract()
                )
            )
            shop_item['name'] = self.safe_list_get(
                item.xpath(ITEM['name']).extract()
            )

            if bool(item.xpath(ITEM['new_price'])):
                shop_item['old_price'] = self.safe_list_get(
                    item.xpath(ITEM['old_price']).extract()
                )
                shop_item['new_price'] = self.safe_list_get(
                    item.xpath(ITEM['new_price']).extract()
                )
            else:
                shop_item['old_price'] = self.safe_list_get(
                    item.xpath(ITEM['price']).extract()
                )

            if ITEM['image']:
                shop_item['image_urls'] = [self.safe_list_get(
                    item.xpath(ITEM['image']).extract()
                )]

            yield shop_item
