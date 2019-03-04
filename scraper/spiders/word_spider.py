import os

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

fileDir = os.path.dirname(os.path.realpath('__file__'))


RULES = {
    "start_urls": ["https://www.x-kom.pl/g-13/c/1291-monitory-led-27-28-9.html"],
    "allow": r"\.",
    "xpath": "//div[@class='pagination-wrapper']//a",
    "deny": [],
}


class WordSpider(CrawlSpider):
    name = 'words'
    next_page = ''
    rules = [
        Rule(
            LinkExtractor(
                allow=RULES["allow"],
                restrict_xpaths=RULES["xpath"],
                deny=RULES["deny"],
            ),
            callback='parse_page',
            follow=True,
        ),
    ]
    APPAREANCE = 0

    def __init__(self, *args, **kwargs):
        super(WordSpider, self).__init__(*args, **kwargs)
        self.word = kwargs.get('word', '')

        self.parse_rules()

    def parse_rules(self):
        self.start_urls = [url for url in RULES['start_urls']]

    def parse_page(self, response):
        self.APPAREANCE += str(response.body).count(self.word)
        self.log('Apperance of word %s' % self.APPAREANCE)
