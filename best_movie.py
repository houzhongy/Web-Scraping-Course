import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMovieSpider(CrawlSpider):
    name = 'best_movie'
    allowed_domains = ['www.imdb.com']


    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc', headers = {
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//h3[@class='lister-item-header']/a")), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths=("(//a[@class='lister-page-next next-page'])[2]")), process_request= "set_user_agent")
    )

    def set_user_agent(self, request, spider):
        request.headers["User-Agent"] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            "Title" : response.xpath("//div[@class = 'title_wrapper']/h1/text()").get(),
            "Year": response.xpath("//span[@id='titleYear']/a/text()").get(),
            "Duration": response.xpath("normalize-space(//div[@class = 'subtext']//time/text())").get(),
            "Genre": response.xpath("(//div[@class = 'subtext']/a)[1]/text()").get(),
            "Rating": response.xpath("//div[@class='ratingValue']//span[@itemprop='ratingValue']/text()").get(),
            "Url": response.url,
            "user-agent": response.request.headers["User-Agent"]
        }