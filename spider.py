import argparse
import os

from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class InfoSpider(CrawlSpider):
    """
    Information Retrieval Spider
    - spider starts by using start_urls and iteratively scanning web-pages for content and url links
    - content is scrapped using the parse_item class method which retrieves textual content from each web-page
    - content is written to a single json file (dict of url, and text)
    """
    name = "InfoSpider"

    # spider start-urls (initial urls which are used once the spider is initiated)
    start_urls = [
        "https://csu.qc.ca/content/student-groups-associations",
        "https://www.concordia.ca/artsci/students/associations.html",
        "http://www.cupfa.org",
        "http://cufa.net",
    ]

    # specify spider rules to follow urls found on the web-page and call parse_item
    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        """
        parse individual web-pages for textual content
        :param response: web-page in context
        """
        # create a dict object to hold data
        data = dict()
        # store response url
        data['url'] = response.url
        # store response title
        title = response.meta['link_text'].split()
        # obtain textual tags within divs, use regex '\w+' to only obtain word occurences within tags
        divs = response.xpath('//div')
        # store p tags (paragraphs)
        paragraphs = list()
        for p in divs.xpath('.//p/text()').re('\w+'):
            paragraphs.append(p)
        # store header tags (h1 to h3)
        headers = list()
        for h in divs.xpath('.//h1/text()').re('\w+'):
            headers.append(h)
        for h in divs.xpath('.//h2/text()').re('\w+'):
            headers.append(h)
        for h in divs.xpath('.//h3/text()').re('\w+'):
            headers.append(h)
        for h in divs.xpath('.//h4/text()').re('\w+'):
            headers.append(h)
        for h in divs.xpath('.//h5/text()').re('\w+'):
            headers.append(h)
        for h in divs.xpath('.//h6/text()').re('\w+'):
            headers.append(h)
        # store span tags textual content
        spans = list()
        for s in response.xpath('.//span/text()').re('\w+'):
            spans.append(s)
        # store footer textual content
        footers = list()
        for f in response.xpath('.//footer/text()').re('\w+'):
            footers.append(f)
        # store text into a single list excluding any stopwords
        text = [w.lower() for w in (title + paragraphs + headers + spans + footers)]
        data['text'] = text
        # return and write dictionary to json result file
        yield data


def clear_results():
    """ delete existing result.json file if it exists """
    try:
        os.remove('result.json')
        print('result.json file was successfully deleted')
    except OSError as e:
        print('error occured: {}'.format(str(e)))


def execute_spider():
    parser = argparse.ArgumentParser(description='define spider params')
    parser.add_argument('-max', type=int, help='spider url max bound', default=10)
    args = parser.parse_args()
    '''
    Define a CrawlerProcess to be able to run Scrapy spider through a python script
    CLOSESPIDER_ITEMCOUNT = # of urls items to be parsed (bound)
    FEED_FORMAT = specify the file type
    FEED_URI = specify the file name to write data to at yield keyword
    '''
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'CLOSESPIDER_ITEMCOUNT': args.max,
        'FEED_FORMAT': 'json',
        'FEED_URI': 'result.json'
    })
    # init crawler and start
    process.crawl(InfoSpider)
    process.start()


if __name__ == '__main__':
    clear_results()
    execute_spider()
