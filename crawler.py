''' Web Crawler Python Module '''
from bs4 import BeautifulSoup
import json
import re
import requests

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
    ''' test function to extract html links '''
    f = open('content/urls.txt', 'w')
    for url in parent_urls:
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            if str(link['href']).startswith(('http://', 'https://')):
                f.write(str(link['href']) + "\n")


def main():
    get_urls()


if __name__ == '__main__':
    main()
