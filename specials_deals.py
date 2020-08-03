import scrapy


class SpecialsDealsSpider(scrapy.Spider):
    name = 'special_deals'
    allowed_domains = ['www.tinydeal.com']
    start_urls = ['https://www.tinydeal.com/specials.html']

    def parse(self, response):
        for product in response.xpath("//ul[@class='productlisting-ul']/div/li"):
            yield{
                "Name": product.xpath(".//a[@class='p_box_title']/text()").get(),
                "Price": product.xpath(".//div[@class='p_box_price']/span[1]/text()").get(),
                "URL": response.urljoin(product.xpath(".//a[@class='p_box_title']/@href").get())
            }

        next_page = response.xpath("//a[@class='nextPage']/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)