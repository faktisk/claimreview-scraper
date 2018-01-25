import scrapy
from scrapy.spiders import XMLFeedSpider
from claimreview.spiders.claimreview import ClaimReviewSpider
from claimreview.parser import ClaimReviewParser

class FaktiskSpider(XMLFeedSpider):
    name = 'faktisk'

    allowed_domains = [
      'www.faktisk.no'
    ]

    start_urls = [
      'https://www.faktisk.no/atom.xml'
    ]

    iterator = 'xml'
    namespaces = [('atom', 'http://www.w3.org/2005/Atom')]
    itertag = 'atom:entry'

    parser = ClaimReviewParser()

    def parse_node(self, response, node):
      html_page = node.xpath('./atom:link[@rel="alternate" and @type="text/html"]/@href').extract_first()
      self.logger.info(html_page)

      return response.follow(html_page, callback=self.parse_html)

    def parse_html(self, response):
      items = self.parser.parse(response)
      for item in items:
        yield item



