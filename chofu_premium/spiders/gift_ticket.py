import unicodedata

import scrapy
from scrapy.http import HtmlResponse
from typing import List


class GiftTicketSpider(scrapy.Spider):
    name = 'gift_ticket'
    allowed_domains = ['premium-gift.jp']
    base_url = 'https://premium-gift.jp/chofu2021/use_store?events=page&id='
    start_urls = [base_url + '1']

    def parse(self, response: HtmlResponse, **kwargs):
        current_page = int(response.xpath("//span[@class='pagenation__item is-current']/text()").get())
        # 店舗情報の取得
        stores = CrawlStore(response).crawl_stores()
        for item in stores:
            yield Store(
                    **item,
                    is_large_store=str("大型店" in item["title"])
            )

        # 次のページがあるか確認
        pagenation = response.xpath("//a[@class='pagenation__item']")
        has_next_page = pagenation[len(pagenation) - 1].xpath("string(.)").get() == "次へ"
        if has_next_page:
            yield scrapy.Request(url=self.base_url + str(current_page + 1))


class CrawlStore:
    def __init__(self, response: HtmlResponse):
        self.response = response

    def crawl_stores(self) -> List[dict]:
        table = self.response.xpath("//div[@class='store-card__item']")
        stores = []
        for item in table:
            store_table = item.xpath(".//table[@class='store-card__table']/tbody/tr/td")

            store_data = {
                "title": item.xpath(".//h3[@class='store-card__title']/text()").get(),
                "tag": item.xpath(".//p[@class='store-card__tag']/text()").get(),
                "address": store_table[0].xpath("string(.)").get(),
                "tel": store_table[1].xpath("string(.)").get(),
                "url": store_table[2].xpath(".//a/@href").get()
            }
            # 整形
            for k, v in store_data.items():
                if not v:
                    store_data[k] = ""
                    continue
                store_data[k] = unicodedata.normalize("NFKC", v.strip())

            stores.append(store_data)
        return stores


class Store(scrapy.Item):
    """
    データ保存用
    """

    # cf. settings.py 内の FEED_EXPORT_FIELDS
    title = scrapy.Field()
    tag = scrapy.Field()
    address = scrapy.Field()
    tel = scrapy.Field()
    url = scrapy.Field()
    is_large_store = scrapy.Field()
