import scrapy

class Gdp_debtSpider(scrapy.Spider):
    name = "gdp_debt"
    allowed_domains = ["worldpopulationreview.com"]
    start_urls = ["https://worldpopulationreview.com/countries/countries-by-national-debt"]


    def parse(self, response):
        rows = response.xpath("//table/tbody/tr")
        for row in rows:
            name = row.xpath(".//td/a/text()").get()
            gdp_ratio = row.xpath(".//td[2]/text()").get()
            yield {
                "country_name": name,
                "Gdp_ratio": gdp_ratio
                }


