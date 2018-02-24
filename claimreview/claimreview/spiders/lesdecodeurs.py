import scrapy
from claimreview.spiders.claimreview import ClaimReviewSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class LesDecodeursSpider(ClaimReviewSpider):
    name = 'lesdecodeurs'
    allowed_domains = ['www.lemonde.fr']
    start_urls = ['http://www.lemonde.fr/les-decodeurs']
    language = 'fr'

    rules = (
        Rule(LinkExtractor(allow='/les-decodeurs'),
             follow=True, callback='parse_item'),
    )

