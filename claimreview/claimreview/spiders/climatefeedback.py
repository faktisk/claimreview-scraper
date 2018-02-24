import scrapy
from claimreview.spiders.claimreview import ClaimReviewSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class ClimateFeedbackSpider(ClaimReviewSpider):
    name = 'climatefeedback'
    allowed_domains = ['climatefeedback.org']
    start_urls = ['https://climatefeedback.org/claim-reviews/']

    rules = (
        Rule(LinkExtractor(allow='/claim-?reviews?/'),
             follow=True, callback='parse_item'),
    )
