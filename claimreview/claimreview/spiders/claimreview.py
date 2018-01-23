# -*- coding: utf-8 -*-
import scrapy
import microdata
import json



class ClaimreviewSpider(scrapy.Spider):
    name = 'claimreview'

    schema_type = 'http://schema.org/ClaimReview'

    allowed_domains = [
        'fullfact.org',
        'politifact.com',
        'faktisk.no',
        'factcheck.org',
        'snopes.com'
    ]

    start_urls = [
        'https://fullfact.org',
        'http://www.politifact.com',
        'https://www.snopes.com',
        'https://www.factcheck.org'
    ]

    def parse(self, response):
        items = self.get_claim_reviews(response)

        if len(items) == 0:
            self.log('no items found')

        for item in items:
            yield item

        for a in response.css('a'):
            if a.css('::attr(href)').extract():
                yield response.follow(a, callback=self.parse)


    def get_claim_reviews(self, response):
        items = [item.json_dict() for item in microdata.get_items(response.text)]
        items = [item for item in items if 'type' in item and self.schema_type in item['type']]

        scripts = response.css('script[type="application/ld+json"]::text').extract()

        for script in scripts:
            item = json.loads(script)

            if '@type' in item and (item['@type'] == 'ClaimReview' or 'ClaimReview' in item['@type']):
                items.append(item)

        return items
