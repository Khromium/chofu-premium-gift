import scrapy
from scrapy.http import HtmlResponse


class GiftTicketSpider(scrapy.Spider):
    name = 'gift_ticket'
    allowed_domains = ['premium-gift.jp']
    start_urls = ['https://premium-gift.jp/chofu/use_store?events=page&id=1']

    def parse(self, response: HtmlResponse, **kwargs):
        table = response.xpath("//div[@class='store-card__item']")
        for item in table:
            store_title = item.xpath(".//h3[@class='store-card__title']/text()")
            store_tag = item.xpath(".//p[@class='store-card__tag']/text()")
            store_table = item.xpath(".//table[@class='store-card__table']/tbody/tr/td")
            store_address = store_table[0].xpath("string(.)")
            store_tel = store_table[1].xpath("string(.)")
            store_url = store_table[2].xpath(".//a/@href")


            print(f"店名：{store_title.get()}\n"
                  f"タグ：{store_tag.get()}\n"
                  f"住所：{store_address.get()}\n"
                  f"電話：{store_tel.get()}\n"
                  f"URL：{store_url.get()}\n")
