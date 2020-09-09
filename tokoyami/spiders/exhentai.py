import scrapy

from tokoyami.items import TokoyamiItem


class ExhentaiSpider(scrapy.Spider):
    name = 'exhentai'
    allowed_domains = ['exhentai.org']
    # start_urls = ['https://exhentai.org/']
    cookies = [{
        "domain": ".exhentai.org",
        "expirationDate": 1630826273.094063,
        "hostOnly": "false",
        "httpOnly": "false",
        "name": "igneous",
        "path": "/",
        "sameSite": "unspecified",
        "secure": "false",
        "session": "false",
        "storeId": "null",
        "value": "52ed9dcfb"
    }, {
        "domain": ".exhentai.org",
        "expirationDate": 1599332477.639999,
        "hostOnly": "false",
        "httpOnly": "false",
        "name": "yay",
        "path": "/",
        "sameSite": "unspecified",
        "secure": "false",
        "session": "false",
        "storeId": "null",
        "value": "louder"
    }, {
        "domain": ".exhentai.org",
        "expirationDate": 1630826161.063736,
        "hostOnly": "false",
        "httpOnly": "false",
        "name": "ipb_member_id",
        "path": "/",
        "sameSite": "unspecified",
        "secure": "false",
        "session": "false",
        "storeId": "null",
        "value": "2935985"
    }, {
        "domain": ".exhentai.org",
        "hostOnly": "false",
        "httpOnly": "false",
        "name": "ipb_session_id",
        "path": "/",
        "sameSite": "unspecified",
        "secure": "false",
        "session": "true",
        "storeId": "null",
        "value": "244ffc25fc15c86996ffdb711dda85fb"
    }, {
        "domain": ".exhentai.org",
        "expirationDate": 1630826163.369476,
        "hostOnly": "false",
        "httpOnly": "false",
        "name": "sk",
        "path": "/",
        "sameSite": "unspecified",
        "secure": "false",
        "session": "false",
        "storeId": "null",
        "value": "9tcn7qfs30eb2g3ix1a1b07y9zq5"
    }, {
        "domain": ".exhentai.org",
        "expirationDate": 1601881924.020506,
        "hostOnly": "false",
        "httpOnly": "true",
        "name": "__cfduid",
        "path": "/",
        "sameSite": "lax",
        "secure": "false",
        "session": "false",
        "storeId": "null",
        "value": "dec184e4c84bb2105c77e8189ae3c03111599289923"
    }, {
        "domain": ".exhentai.org",
        "expirationDate": 1630826161.063759,
        "hostOnly": "false",
        "httpOnly": "false",
        "name": "ipb_pass_hash",
        "path": "/",
        "sameSite": "unspecified",
        "secure": "false",
        "session": "false",
        "storeId": "null",
        "value": "2134096d749554dc25e127bd04ff7b46"
    }]

    def start_requests(self):
        yield scrapy.FormRequest("https://exhentai.org/?f_cats=765&f_search=chiness", cookies=self.cookies,
                                 callback=self.parse)

    def parse(self, response):
        gallery_list = response.xpath("//td[@class='gl3c glname']//a").extract()
        for gallery in gallery_list:
            link = scrapy.selector.Selector(text=gallery).xpath("//a/@href").get()
            name = scrapy.selector.Selector(text=gallery).xpath("//div[@class='glink']//text()").get()
            yield scrapy.Request(url=link, callback=self.detail_pares, meta={"name": name})

    def detail_pares(self, response):
        label = response.xpath("//div[@class='gtl']//a//text()").extract()
        if "netorare" not in label and "yaoi" not in label and "furry" not in label:
            images = response.xpath("//div[@class='gdtl']//a/@href").extract()
            pages = response.xpath("//div[@id='gdd']//table//tr[6]//td[@class='gdt2']/text()").extract()[0]
            for img_url in images:
                yield scrapy.Request(url=img_url, callback=self.image_parse,
                                     meta={"name": u"{0}({1})".format(response.meta.get("name"), pages)})
        next_page = response.xpath("//table[@class='ptt']//tr//td[last()]/@onclick").extract()
        if next_page:
            next_page_url = response.xpath("//table[@class='ptt']//tr//td[last()]//a/@href").extract()[0]
            yield scrapy.Request(url=next_page_url, callback=self.detail_pares,
                                 meta={"name": response.meta.get("name")})

    @staticmethod
    def image_parse(response):
        images_url = response.xpath("//img[@id='img']/@src").extract()[0]
        images_name = response.meta.get("name")
        item = TokoyamiItem()
        item["image_urls"] = images_url
        item["image_names"] = images_name
        yield item
