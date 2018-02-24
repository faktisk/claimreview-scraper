import scrapy
from claimreview.spiders.claimreview import ClaimReviewSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class AgenciaLupaSpider(ClaimReviewSpider):
    name = 'agencialupa'
    allowed_domains = ['piaui.folha.uol.com.br']
    start_urls = ['http://piaui.folha.uol.com.br/lupa']
    language = 'pt'

    rules = (
        Rule(LinkExtractor(allow='/lupa'),
             follow=True, callback='parse_item'),
    )

