import scrapy
from claimreview.spiders.claimreview import ClaimReviewSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

class WashingtonPostSpider(ClaimReviewSpider):
    name = 'wp'
    allowed_domains = ['www.washingtonpost.com']
    start_urls = [ 'https://www.washingtonpost.com/news/fact-checker/' ]

    rules = (
        Rule(LinkExtractor(allow='/news/fact-checker/'), follow=True, callback='parse_item'),
    )


