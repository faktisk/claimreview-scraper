# -*- coding: utf-8 -*-
import scrapy
import microdata
import json

from claimreview.items import *
from claimreview.parser import ClaimReviewParser
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ClaimReviewSpider(CrawlSpider):
    name = 'claimreview'

    allowed_domains = [
        'fullfact.org',
        'politifact.com',
        'www.faktisk.no',
        'factcheck.org',
        'www.snopes.com'
    ]

    start_urls = [
        'https://fullfact.org',
        'http://www.politifact.com',
        'https://www.snopes.com',
        'https://www.factcheck.org',
    ]

    rules = (
        Rule(LinkExtractor(allow=''), follow=True, callback='parse_item'),
    )

    claim_review_parser = ClaimReviewParser()

    def parse_item(self, response):
        items = self.claim_review_parser.parse(response)
        self.log('{}: {} items found'.format(response.url, len(items)))

        for item in items:
            yield item
