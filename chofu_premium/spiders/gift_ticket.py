import scrapy
from scrapy.http import HtmlResponse


class GiftTicketSpider(scrapy.Spider):
    name = 'gift_ticket'
    allowed_domains = ['premium-gift.jp']
    start_urls = ['https://premium-gift.jp/chofu/use_store?events=page&id=1']

    def parse(self, response: HtmlResponse, **kwargs):
        current_page = int(response.xpath("//span[@class='pagenation__item is-current']/text()").get())
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
        pagenation = response.xpath("//a[@class='pagenation__item']")
        has_next_page = pagenation[len(pagenation) - 1].xpath("string(.)").get() == "次へ"
        if has_next_page:
            yield scrapy.Request(url="https://premium-gift.jp/chofu/use_store?events=page&id=" + str(current_page + 1))
