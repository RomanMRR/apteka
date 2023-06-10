import time
from scrapy import Spider, Request
from scrapy.http import JsonRequest
from json import JSONDecodeError

from apteka.items import AptekaItem

URL_FOR_API = 'https://apteka-ot-sklada.ru/api/catalog/{id}'
MAIN_URL = 'https://apteka-ot-sklada.ru{product_url}'
CITY = 92  # Идентификатор города Томск


class AptekaOtSkladaSpider(Spider):
    name = 'apteka_ot_sklada'
    start_urls = [
        'https://apteka-ot-sklada.ru/catalog/sredstva-gigieny/uhod-za-polostyu-rta/zubnye-niti_-ershiki/',
        'https://apteka-ot-sklada.ru/catalog/sredstva-gigieny/uhod-za-polostyu-rta/opolaskivatel-dlya-rta',
        'https://apteka-ot-sklada.ru/catalog/medikamenty-i-bady/obezbolivayushchie-sredstva/obezbolivayushchee-naruzhnoe'
    ]

    def start_requests(self):
        """
        Делаем первый запрос на получения информации о городе Томск, чтобы последующие запросы были для этого города
        """
        data = {"id": CITY}
        yield JsonRequest(
            url='https://apteka-ot-sklada.ru/api/user/city/requestById',
            callback=self.parse_region,
            data=data,
            method="POST"

        )

    def parse_region(self, response, **kwargs):
        """
        Собираем информацию о товарах в заданных категориях
        """
        for url in self.start_urls:
            yield Request(
                url=url,
                callback=self.parse
            )

    def parse(self, response, **kwargs):
        """
        Собираем информацию о товарах в категории
        """
        products = response.xpath('//div[@itemprop="itemListElement"]')
        for product in products:
            url = product.xpath('.//a[@class="goods-card__link"]/@href').get()
            product_id = url.split('_')[-1]
            yield Request(
                url=URL_FOR_API.format(id=product_id),
                callback=self.parse_product,
                cb_kwargs={"url": url,
                           "good_id": product_id}
            )
        next_page = response.xpath('//a[contains(@class, "ui-pagination__link_direction")]/@href')[-1].get()

        if next_page is not None:
            url = MAIN_URL.format(product_url=next_page)
            yield Request(url, callback=self.parse, cookies={"city": f'{CITY}'})

    def parse_product(self, response, **kwargs):
        """
        Собираем информацию о товаре
        """
        item = AptekaItem()
        item["timestamp"] = time.time()
        item["url"] = MAIN_URL.format(product_url=kwargs.get("url"))

        item["RPC"] = kwargs.get("product_id")
        try:
            json_data = response.json()
        except JSONDecodeError:
            self.logger.warning("Failed to get product information")
            yield item
            return

        item["title"] = json_data.get("name")
        item["marketing_tags"] = [marketing_tag.get("name") for marketing_tag in
                                  json_data.get("stickers", [])]

        item["section"] = []
        if json_data.get("category", {}).get("parents"):
            item["section"] = [category_name.get("name") for category_name in
                               json_data.get("category", {}).get("parents")]
        item["section"].append(json_data.get("category", {}).get("name"))

        item["price_data"] = {
            "current": 0.,
            "original": 0.,
            "sale_tag": ""
        }
        item["price_data"]["current"] = json_data.get("cost")
        item["price_data"]["original"] = json_data.get("oldCost")
        if item["price_data"]["original"] and item["price_data"]["original"]:
            discount_percent = ((item["price_data"]["original"] - item["price_data"]["current"]) / item["price_data"][
                "original"]) * 100
            item["price_data"]["sale_tag"] = f'Скидка {discount_percent}%'

        item["stock"] = {
            "in_stock": False,
            "count": 0
        }
        item["stock"]["in_stock"] = json_data.get("inStock")
        item["stock"]["count"] = json_data.get("availability")  # Количество магазинов, где доступен товар

        item["assets"] = {
            "main_image": "",  # {str} Ссылка на основное изображение товара
            "set_images": [],  # {list of str} Список больших изображений товара
        }
        if json_data.get("images"):
            item["assets"]["main_image"] = json_data.get("images").pop(
                0)  # Первое изображение в списке является главным
        item["assets"]["set_images"] = json_data.get("images")

        item["metadata"] = {
            "__description": "",  # {str} Описание товар
            "СТРАНА ПРОИЗВОДИТЕЛЬ": ""
        }
        item["metadata"]["__description"] = json_data.get("description")
        item["metadata"]["СТРАНА ПРОИЗВОДИТЕЛЬ"] = json_data.get("country")
        item["metadata"]["производитель"] = json_data.get("producer")
        item["metadata"]["Дата доставки"] = json_data.get("delivery")

        yield item
