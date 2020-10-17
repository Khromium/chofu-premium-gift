import scrapy
from scrapy.http import HtmlResponse


class GiftTicketSpider(scrapy.Spider):
    name = 'gift_ticket'
    allowed_domains = ['premium-gift.jp']
    start_urls = ['https://premium-gift.jp/chofu/use_store?events=page&id=1']

    def parse(self, response: HtmlResponse, **kwargs):
        text = response.xpath("//div[@class='store-card__item']/h3/text()").extract()
        [print(item) for item in text]
