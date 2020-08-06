import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']

    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"

    def start_requests(self):
        yield scrapy.Request(url="http://books.toscrape.com", headers={
            "User-Agent": self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//div[@class = 'image_container']")), callback='parse_item', follow=True, process_request="set_user_agent"),
        Rule(LinkExtractor(restrict_xpaths=("//li[@class = 'next']/a")), process_request="set_user_agent")
    )

    def set_user_agent(self,request,spider):
        request.headers["User-Agent"]= self.user_agent
        return request

    def parse_item(self, response):
       yield {
           "Name":response.xpath("//h1/text()").get(),
           "Price": response.xpath("//p[@class='price_color']/text()").get()
       }
