# Apteka-ot-sklada parser

⚕️ Парсер для получения информации о товарах в
магазиние [Apteka-ot-sklada](https://apteka-ot-sklada.ru/)
⚕️

Парсер реализован с использованием фреймворка `Scrapy`

## Инструкция для запуска

Для запуска скрипта у себя на компьютере проделайте следующее:

Скопируйте данный репозиторий

```
git clone https://github.com/RomanMRR/apteka.git
```

Перейдите в папку проекта

```
cd apteka
```

Установите необходимые пакеты

```
pip install -r requirements.txt
```

Запустите скрипт

```
scrapy crawl apteka_ot_sklada
```

Полученные данные будут сохранены в файле json `apteka/data/apteka_ot_sklada.json`












