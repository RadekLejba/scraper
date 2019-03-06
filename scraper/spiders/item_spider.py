import os

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scraper.items import ShopItem


fileDir = os.path.dirname(os.path.realpath('__file__'))
RULES = {
    "start_urls": ["https://www.morele.net/komputery/komputery-pc/komputery-dla-graczy-672/"],
    "allow": r"\.",
    "xpath": "//li[@class='pagination-lg next']//a",
    "deny": [],
}

ITEM = {
    # Container with item
    'container': '//div[@class="cat-product card "]',
    # Element with url to item page
    'url': {
        'main': 'https:/www.morele.net',
        'xpath': '//h2[@class="cat-product-name"]//a//@href',
    },
    # Element with item rating
    'rating': '//div[@class="cat-product-sold"]//@data-tooltip',
    # Element with item features
    'features': '//div[@class="cat-product-features"]',
    # Element with item name
    'name': '//h2[@class="cat-product-name"]//a//text()',
    # Element with item price
    'price': 'div//div[@class="price-new"]//text()',
    # Element with optional old item price
    'old_price': 'div//div[@class="price-old"]//text()',
    # Element with optional new item price
    'new_price': 'div//div[@class="price-new"]//text()',
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
            try:
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
            except IndexError:
                pass

            yield shop_item
