# -*- coding: utf-8 -*-
import scrapy
import microdata
import json
import re

from urllib.parse import urlparse

from claimreview.parser import ClaimReviewParser
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ClaimReviewSpider(CrawlSpider):
    name = 'claimreview'

    allowed_domains = [
        'africacheck.org',
        'aosfatos.org',
        'apublica.org',
        'chequeado.com',
        'climatefeedback.org',
        'fullfact.org',
        'nieuwscheckers.nl',
        'pagellapolitica.it',
        'www.politifact.com',
        'teyit.org'
        'www.africacheck.org'
        'www.dogrulukpayi.com',
        'www.factcheck.org',
        # 'www.gossipcop.com',
        'www.snopes.com',
    ]

    start_urls = [
        'http://chequeado.com/',
        'http://nieuwscheckers.nl/',
        'http://www.dogrulukpayi.com/',
        'http://www.politifact.com',
        'https://africacheck.org',
        'https://aosfatos.org/',
        'https://apublica.org',
        'https://fullfact.org',
        'https://pagellapolitica.it',
        'https://teyit.org'
        'https://theferret.scot/category/fact-check/',
        'https://www.factcheck.org',
        'https://www.factcheck.org',
        # 'https://www.gossipcop.com',
        'https://www.snopes.com',
    ]

    rules = (
        Rule(LinkExtractor(allow=''), follow=True, callback='parse_item'),
    )

    claim_review_parser = ClaimReviewParser()

    domain_languages = {
        'pagellapolitica.it': 'it',
        'apublica.org': 'pt',
        'aosfatos.org': 'pt',
        'chequeado.com': 'es',
        'dogrulukpayi.com': 'tr',
        'nieuwscheckers.nl': 'nl',
        'teyit.org': 'tr'
    }

    language = None

    def parse_item(self, response):
        items = self.claim_review_parser.parse(response, language=self.get_language(response))
        self.log('{}: {} items found'.format(response.url, len(items)))

        for item in items:
            yield item

    def get_language(self, response):
        host = urlparse(response.url).netloc
        host_without_www = re.sub('^www.', '', host)
        html_lang = response.css('html::attr("lang")').extract();

        if self.language is not None:
            return self.language
        elif host in self.domain_languages:
            return self.domain_languages[host]
        elif host_without_www in self.domain_languages:
            return self.domain_languages[host_without_www]
        elif html_lang:
            return re.split('[\-_]', html_lang[0])[0]
        else:
            return 'en'
