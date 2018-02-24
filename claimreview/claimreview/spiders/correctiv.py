import scrapy
from claimreview.spiders.claimreview import ClaimReviewSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class CorrectivSpider(ClaimReviewSpider):
    name = 'correctiv'
    allowed_domains = ['correctiv.org']
    start_urls = ['https://correctiv.org/echtjetzt/artikel/']
    language = 'de'


    rules = (
        Rule(LinkExtractor(allow='/echtjetzt'),
             follow=True, callback='parse_item'),
    )

