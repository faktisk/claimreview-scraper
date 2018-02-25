import json
import gzip
import io

from scrapy import Spider, Request
from scrapy.http import TextResponse
from claimreview.parser import ClaimReviewParser


class CommonCrawlSpider(Spider):
    name = "commoncrawl"
    domains = [
        'politifact.com',
        'faktisk.no',
        'africacheck.org',
        'aosfatos.org',
        'apublica.org',
        'chequeado.com',
        'climatefeedback.org',
        'fullfact.org',
        'nieuwscheckers.nl',
        'pagellapolitica.it',
        'politifact.com',
        'teyit.org'
        'www.africacheck.org'
        'www.dogrulukpayi.com',
        'www.factcheck.org',
        'www.gossipcop.com',
        'www.snopes.com'
    ]

    custom_settings = {
        'ROBOTSTXT_OBEY': False,  # index doesn't allow crawling
        'HTTPCACHE_ENABLED': False,  # caching won't work with our Range requests
    }

    claim_review_parser = ClaimReviewParser()

    indices = [
        "2018-05",
        "2017-51",
        "2017-47",
        "2017-43",
        "2017-39",
        "2017-34",
        "2017-30",
        "2017-26",
        "2017-22",
        "2017-17",
        "2017-13",
        "2017-09",
        "2017-04"
    ]

    def start_requests(self):
        for domain in self.domains:
            for index in self.indices:
                yield Request('http://index.commoncrawl.org/CC-MAIN-{}-index?url={}&matchType=domain&output=json'.format(index, domain), self.parse_index)

    def parse_index(self, response):
        items = []
        lines = response.body.splitlines()

        for line in lines:
            item = json.loads(line)

            if item['status'] == '200' and item['mime'] == 'text/html':
                offset, length = int(item['offset']), int(item['length'])
                offset_end = offset + length - 1

                req = Request('https://commoncrawl.s3.amazonaws.com/{}'.format(item['filename']), headers={
                              'Range': 'bytes={}-{}'.format(offset, offset_end)}, callback=self.parse_record, dont_filter=True)
                req.meta['index_item'] = item

                yield req

    def parse_record(self, response):
        # self.log('headers={}, body={}'.format(response.headers, response.body[0:100]))
        original_url = response.meta['index_item']['url']
        data = gzip.GzipFile(fileobj=io.BytesIO(response.body)).read()

        if len(data):
            warc, header, body = data.decode().strip().split('\r\n\r\n', 2)

            items = self.claim_review_parser.parse(
                TextResponse(original_url, body=body, encoding='utf8'))

            self.log('{}: {} items found'.format(original_url, len(items)))

            for item in items:
                yield item
