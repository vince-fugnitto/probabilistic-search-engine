import nltk
from bs4 import BeautifulSoup
import os
import shutil
import sys
from math import log

# Sets encoding to utf8
reload(sys)
sys.setdefaultencoding('utf8')


# Writes a frequency inverted index to a text file using the spimi algorithm
def create_inverted_index():
    inverted_index = dict()

    # Goes through each of the documents
    for i in range(22):
        file_name = "reuters21578/reut2-{:03d}.sgm".format(i)
        soup = BeautifulSoup(open(file_name), "html.parser")

        articles = soup.find_all("reuters")  # Retrieves a list of articles within a file

        # Iterates through each article to get tokens
        for article in articles:
            newid = article.attrs["newid"]  # Gets NEWID value from article
            text = article.find('text').get_text()  # Retrieves text from article
            tokens = nltk.word_tokenize(text)  # Forms a list of tokens from text

            # Adds tokens and their belonging document IDs to inverted index
            for token in tokens:
                modified_token = token.lower()
                if modified_token not in inverted_index:
                    inverted_index[modified_token] = dict()
                if newid not in inverted_index[modified_token]:
                    inverted_index[modified_token][newid] = 1
                else:
                    inverted_index[modified_token][newid] += 1

    # Write to text file
    f = open("inverted_index", "w")
    sorted_terms = sorted(inverted_index)

    for term in sorted_terms:
        f.write(term)
        for posting, frequency in inverted_index[term].iteritems():
            f.write(" %s %s" % (posting, frequency))
            f.write("\n")
            f.close()

            inverted_index = dict()


    f.close()   # Closes file


# Retrieves SPIMI inverted index
def load_inverted_index():
    f = open("inverted_index.txt", "r")
    f.readline()  # Discards empty line
    index = dict()

    # Adds each line from file to dictionary
    for line in f.readlines():
        elements = line.split()
        index[elements[0]] = dict()

        for i in range(1, len(elements), 2):
            index[elements[0]][elements[i]] = elements[i + 1]

    return index




query_tests()
