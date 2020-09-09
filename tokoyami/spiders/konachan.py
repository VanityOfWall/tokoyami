import scrapy

from tokoyami.items import TokoyamiItem


class KonachanSpider(scrapy.Spider):
    name = 'konachan'
    # allowed_domains = ['konachan.net']
    start_urls = ['https://konachan.com/post']

    base_url = 'https://konachan.com'

    pages = 0

    def parse(self, response):
        picData = response.xpath('//a[@class="thumb"]/@href').extract()
        for pic_url in picData:
            yield scrapy.Request(self.base_url + pic_url, callback=self.detail_parse)

        nextUrl = response.xpath('//a[@class="next_page"]/@href').extract()[0]
        if self.pages < 5:
            self.pages += 1
            yield scrapy.Request(
                url=self.base_url + nextUrl,
                callback=self.parse
            )

    def detail_parse(self, response):
        url = response.xpath("//a[@id='highres-show']/@href").extract()[0]
        item = TokoyamiItem()
        item["image_urls"] = url
        yield item
