import re
import string

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess

import nltk
from nltk.corpus import stopwords


# define stopwords used for normalization
stops = set(stopwords.words("english"))


class InfoSpider(CrawlSpider):
        """ Information Retrieval Spider """
        name = "InfoSpider"
        start_urls = [
            "https://csu.qc.ca/content/student-groups-associations",
            "https://www.concordia.ca/artsci/students/associations.html",
            "http://www.cupfa.org",
            "http://cufa.net",
        ]

        rules = (
            Rule(LinkExtractor(), callback='parse_item', follow=True),
        )

        # define stopwords used for normalization
        stops = set(stopwords.words('english'))

        def parse_item(self, response):
            """ parse response (web page) """
            # create a dict object to hold data
            data = dict()
            # store response url
            data['url'] = response.url
            # store response title
            data['title'] = response.meta['link_text']
            # obtain textual tags within divs
            divs = response.xpath('//div')
            # store p tags
            paragraphs = list()
            for p in divs.xpath('.//p/text()').re('\w+'):
                paragraphs.append(p)
            # store header tags
            headers = list()
            for h in divs.xpath('.//h1/text()').re('\w+'):
                headers.append(h)
            for h in divs.xpath('.//h2/text()').re('\w+'):
                headers.append(h)
            for h in divs.xpath('.//h3/text()').re('\w+'):
                headers.append(h)
            # store text into a single list without stopwords
            text = [w.lower() for w in (paragraphs + headers) if w not in self.stops]
            data['text'] = text
            # return and write json
            yield data


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'CLOSESPIDER_ITEMCOUNT': 3,
    'FEED_FORMAT': 'json',
    'FEED_URI': 'result.json'
})

# init crawler and start
process.crawl(InfoSpider)
process.start()
