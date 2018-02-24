# -*- coding: utf-8 -*-
import scrapy
import microdata
import json
import re

from urllib.parse import urlparse

from claimreview.items import *
from claimreview.parser import ClaimReviewParser
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ClaimReviewSpider(CrawlSpider):
    name = 'claimreview'

    allowed_domains = [
        'africacheck.org',
        'climatefeedback.org',
        'fullfact.org',
        'pagellapolitica.it',
        'politifact.com',
        'www.africacheck.org'
        'www.gossipcop.com',
        'www.snopes.com',
        'www.factcheck.org',
        'apublica.org',
        'aosfatos.org',
        'chequeado.com',
        'www.dogrulukpayi.com',
        'nieuwscheckers.nl',
        'teyit.org'
    ]

    start_urls = [
        'https://fullfact.org',
        'http://www.politifact.com',
        'https://www.snopes.com',
        'https://www.factcheck.org',
        'https://www.gossipcop.com',
        'https://pagellapolitica.it',
        'https://theferret.scot/category/fact-check/',
        'https://africacheck.org',
        'https://www.factcheck.org',
        'https://apublica.org',
        'https://aosfatos.org/',
        'http://chequeado.com/',
        'http://www.dogrulukpayi.com/',
        'http://nieuwscheckers.nl/',
        'https://teyit.org'
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
            return html_lang[0]
        else:
            return 'en'
