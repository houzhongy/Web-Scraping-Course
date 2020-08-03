import scrapy


class GlassesSpider(scrapy.Spider):
    name = 'Glasses'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers']

    def parse(self, response):
        for product in response.xpath("//div[@class= 'col-12 pb-5 mb-lg-3 col-lg-4 product-list-row']"):
            yield {
                "Product_Imglink": product.xpath(".//div[@class='product-img-outer']/a[@href]/img[@class='lazy d-block w-100 product-img-default']/@src").get(),
                "Product_URL": product.xpath(".//div[@class='product-img-outer']/a[@href]/@href").get(),
                "Product_Price": product.xpath(".//div[@class='p-title-block']/div[@class='mt-3']/div[@class='row no-gutters']/div[@class='col-6 col-lg-6']/div[@class='p-price']//span/text()").get()
            }

        next_page = response.xpath("//ul[@class='pagination' ]/li[6]/a/@href").get()
        if next_page:
            yield scrapy.Request(url = next_page, callback= self.parse)