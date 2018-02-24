import scrapy
from claimreview.spiders.claimreview import ClaimReviewSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class AnimalPoliticoSpider(ClaimReviewSpider):
    name = 'animalpolitico'
    allowed_domains = ['www.animalpolitico.com']
    start_urls = ['https://www.animalpolitico.com/elsabueso/']
    language = 'es'

    rules = (
        Rule(LinkExtractor(allow='/elsabueso/'),
             follow=True, callback='parse_item'),
    )

