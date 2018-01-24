# import scrapy
# from claimreview.spiders.claimreview import ClaimReviewSpider
# from scrapy.spiders import Rule
# from scrapy.linkextractors import LinkExtractor

# class FaktiskSpider(XMLFeedSpider):
#     name = 'faktisk'
#     allowed_domains = ['www.faktisk.no']
#     start_urls = [ 'https://www.faktisk.no/atom.xml' ]

#     rules = (
#         Rule(LinkExtractor(allow='/news/fact-checker/'), callback='parse_item'),
#     )


