''' Web Crawler Python Module '''
from bs4 import BeautifulSoup as bs
import json
import nltk
import os
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

bound = 20


# parent urls
parent_urls = [
    'https://csu.qc.ca/content/student-groups-associations',
    'https://www.concordia.ca/artsci/students/associations.html',
    'http://www.cupfa.org',
    'http://cufa.net'
]


def extract_content():
    ''' extract list of urls '''
    # store list of urls found
    urls = list()
    # keep track of index_id
    index_id = 0
    # create PoolManager instance
    http = urllib3.PoolManager(num_pools=200)
    # iterate over parent urls to extract and store urls
    print('started extracting list of urls...')
    for url in parent_urls:
        # use urllib3 to perform get http request of url
        request = http.request('GET', url)
        # use beautifulsoup to parse page
        soup = bs(request.data.decode('utf-8'), 'html.parser')
        # retrive urls found within link tags
        for link in soup.findAll('a', href=True):
            # extract only http:// urls
            if str(link['href']).startswith(('http://')):
                value = str(link['href'])
                urls.append(value.rstrip('/'))
    print('finished extracting list of urls.')
    print('started extracting content of children urls...')
    # create content directory if not exists
    if not os.path.exists('content'):
        os.makedirs('content')
    # iterate over urls and extract content
    with open('content/corpus.txt', 'w') as file:
        for url in urls[0:bound]:
            print('\textracting content for url %s' % url)
            # store webpage content
            text = list()
            # use urllib3 and beautifulsoup to request and parse webpage
            http = urllib3.PoolManager(num_pools=200)
            try:
                r = http.request('GET', url)
            except:
                continue
            try:
                soup = bs(r.data.decode('utf-8'), 'html.parser')
            except:
                continue
            # parse information tags
            if soup.title: text.append(soup.title.text)
            for i in range(1,6):
                header = [tag.text for tag in soup.findAll('h%s' % i)]
                if header: text.append(header)
            paragraph = [tag.text for tag in soup.findAll('p')]
            text.append(paragraph)
            span = [tag.text for tag in soup.findAll('span')]
            text.append(span)
            print('\twriting json for url %s' % url)
            data = get_json(index_id, url, text)
            file.write(json.dumps(data) + "/n")
    file.close()
    print('finished extracting all content of children urls.')


def get_json(id, url, text):
    ''' write json data to file '''
    # create json object
    data = {}
    data['id'] = id
    data['url'] = url
    data['text'] = text
    return data



def crawl():
    ''' crawl and extract data '''
    extract_content()


if __name__ == '__main__':
    crawl()
