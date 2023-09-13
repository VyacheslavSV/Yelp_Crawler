from urllib.parse import unquote

import scrapy

CATEGORY = "contractors"
LOCATION = "San Francisco, CA"
RANGE = 10


class YelpSpider(scrapy.Spider):
    name = 'yelp_spider'

    def start_requests(self):
        url = f"https://www.yelp.com/search?find_desc={CATEGORY}&find_loc={LOCATION}"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for link in response.css('span.css-1egxyvc a::attr(href)'):
            yield response.follow(link, callback=self.parse_results)

        for i in range(1, RANGE):
            next_page = f"https://www.yelp.com/search?find_desc={CATEGORY}&find_loc={LOCATION}&start={i}"
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_results(self, response):
        business_data = {'business_name': response.css('h1.css-1se8maq::text').get(),
            'business_rating': response.css('span.css-1p9ibgf::text').get(),
            'num_reviews': response.css('span.css-1evauet a::text').re(r'(\d+) reviews')[0],
            'business_yelp_url': response.css('link[rel=canonical]::attr(href)').get(),
            'business_website': unquote(response.css('p.css-1p9ibgf a::attr(href)').re_first(r'(?<=url=)(.*?)(?=&c)')),
            'reviews': []}

        yield business_data
