from urllib.parse import urljoin

import scrapy


from ..items import CarItem


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    start_urls = ['https://auto.ria.com/uk/legkovie/tesla/']
    site_url = 'https://auto.ria.com/'

    def parse(self, response):
        for i in range(24):
            next_page = f'https://auto.ria.com/uk/legkovie/tesla/?page={i}'
            yield response.follow(next_page, callback=self.parse_car)

    def parse_car(self, response):
        all_cars = response.xpath('//section')

        for car in all_cars:
            model = car.xpath('//div[@class="content"]'
                              '/div[@class="head-ticket"]/div[@class="item ticket-title"]/a[@class="address"]'
                              '/span[@class="blue bold"]/text()').extract()
            price_doll = car.xpath('//div[@class="content"]/div[@class="price-ticket"]'
                                   '//span[@class="bold green size22"]/text()').extract()
            price_ua = car.xpath('//div[@class="content"]/div[@class="price-ticket"]//span[@class="i-block"]'
                                 '/span/text()').extract()
            mileage = car.xpath('//div[@class="content"]/div[@class="definition-data"]'
                                '/ul[@class="unstyle characteristic"]/li[@class="item-char js-race"]/text()').extract()
            year = car.xpath('//div[@class="content"]'
                             '/div[@class="head-ticket"]/div[@class="item ticket-title"]'
                             '/a[@class="address"]/text()').extract()
            year = ' '.join(year).split()
            vin_code = car.xpath('//div[@class="content"]/div[@class="definition-data"]'
                                 '/div[@class="base_information"]/span[@class="label-vin"]'
                                 '/span/text()').extract()
            link = car.xpath('//div[@class="content"]/div[@class="head-ticket"]'
                             '/div[@class="item ticket-title"]/a/@href').extract()

            for items in vin_code:
                if items == "  AUTO.RIA перевірив VIN-код і порівняв інформацію від продавця з даними реєстрів МВС. ":
                    vin_code.remove(items)

            for items in vin_code:
                if items == "  Перевірено AUTO.RIA по базам УБКІ, банків, страхових компаній і " \
                            "офіційним дилерським базам.  ":
                    vin_code.remove(items)

            vin_code = ''.join(vin_code).split()

            for items in price_doll:
                if items == "$":
                    price_doll.remove(items)

        car_item = CarItem()
        car_item['model'] = model
        car_item['year'] = [x for x in year if x]
        car_item['mileage'] = mileage
        car_item['price_ua'] = price_ua
        car_item['price_dollar'] = price_doll
        car_item['link'] = link
        car_item['vin_code'] = vin_code

        yield car_item

