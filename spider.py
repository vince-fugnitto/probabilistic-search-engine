import scrapy
from scrapy.crawler import CrawlerProcess

class IRSpider(scrapy.Spider):
    ''' Information Retrieval Spider '''
    name = "IRSpider"
    # spider start urls
    start_urls = [
        "https://csu.qc.ca/content/student-groups-associations",
        "https://www.concordia.ca/artsci/students/associations.html",
        "http://www.cupfa.org",
        "http://cufa.net",
    ]

    def parse(self, response):
        ''' parse webpages for content '''
        # retrieve html tags
        titles = response.selector.xpath('//title/text()').extract()
        # iterate over nodes found
        for node in titles:
            data = {
                'title': node
            }
            yield data

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'FEED_FORMAT': 'json',
    'FEED_URI': 'result.json'
})

# init crawler and start
process.crawl(IRSpider)
process.start()
