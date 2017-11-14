''' Web Crawler Python Module '''
from bs4 import BeautifulSoup
import json
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# page bound
bound = 10

# store pages
pages = list()

# parent urls
parent_urls = [
    'https://csu.qc.ca/content/student-groups-associations',
    'https://www.concordia.ca/artsci/students/associations.html',
    'http://www.cupfa.org',
    'http://cufa.net'
]


def get_urls():
    ''' extract all possible url '''
    print('=== Started: Extracting list of possible URLs... ===')
    # open and write to file
    f = open('content/urls.txt', 'w')
    # iterate through each url within parent_urls list
    http = urllib3.PoolManager()
    for url in parent_urls:
        request = http.request('GET', url)
        soup = BeautifulSoup(request.data.decode('utf-8'), 'html.parser')
        # retrieve all url beginning with http:// or https://
        for link in soup.find_all('a', href=True):
            if str(link['href']).startswith(('http://', 'https://')):
                # write url to file
                f.write(str(link['href']) + "\n")
    f.close()
    print('=== Finished: URLs written to content/urls.txt ===')


def get_content(url):
    ''' obtain webpage content (title, h1-h6 tags, p, span tags) '''
    # store data within json
    data = {}
    content = list()
    # use urrlib3 and beautifulsoup to requet and parse html pages
    http = urllib3.PoolManager()
    request = http.request('GET', url)
    soup = BeautifulSoup(request.data.decode('utf-8'), 'html.parser')
    # parse webpage for content ===
    # obtain page title
    title = soup.title.text
    # obtain page headers (h1 to h6)
    for i in range(1,6):
        header = [tag.text for tag in soup.findAll('h%s' % i)]
        if header: content.append(header)
    # add p tags
    paragraph = [tag.text for tag in soup.findAll('p')]
    content.append(paragraph)
    # add span tags
    span = [tag.text for tag in soup.findAll('span')]
    content.append(paragraph)
    # store content into dict
    data['title'] = title
    data['content'] = content
    return data


def write_content(filename, url):
    ''' write json data to file '''
    with open('content/%s' % filename, 'w') as file:
        data = get_content(url)
        file.write(json.dumps(data))
        file.close()


def main():
    # get_urls()
    # get_content(parent_urls[0])
    write_content('test.txt', parent_urls[0])


if __name__ == '__main__':
    main()
