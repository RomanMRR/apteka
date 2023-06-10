# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class AptekaItem(Item):
    """
    :param timestamp: Текущее время в формате timestamp
    :param RPC: {str} Уникальный код товара
    :param url: {str} Ссылка на страницу товара
    :param title: {str} Заголовок/название товара
    :param marketing_tags: Список тэгов
    :param section: {list of str} Иерархия разделов
    :param price_data: Словарь в формате {
        "current": {float} Цена со скидкой, если скидки нет то = original,
        "original": {float} Оригинальная цена,
        "sale_tag": {str} Если есть скидка на товар то записываем в формате: "Скидка {}%"
    }
    :param stock: Словарь в формате {
        "in_stock": {bool} Должно отражать наличие товара в магазине,
        "count": {int} Количество магазинов, в которых есть товар
    }
    :param assets: Словарь в формате {
        "main_image": {str} Ссылка на основное изображение товара,
        "set_images": {list of str} Список больших изображений товара
    }
    :param metadata: Словарь в формате {
        "__description": {str} Описание товара,
        "СТРАНА ПРОИЗВОДИТЕЛЬ": {str},
        "Производитель": {str},
        "Дата доставки": {str}
    }
    """
    timestamp = Field()
    RPC = Field()
    url = Field()
    title = Field()
    marketing_tags = Field()
    section = Field()
    price_data = Field()
    stock = Field()
    assets = Field()
    metadata = Field()
