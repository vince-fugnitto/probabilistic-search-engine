import argparse
import collections
import json

from afinn import Afinn


# Creates a "inverted_index.txt" file containing the inverted index
def create_inverted_index():
    with open('result.json') as json_data:
        inverted_index = dict()  # Dictionary representing inverted index
        data = json.load(json_data)  # Data retrieved from json file created by crawler

        for entry in data:
            url = entry["url"]  # Gets URL value from article
            tokens = entry["text"]  # Gets a list of tokens from text

            # Adds tokens to dictionary while keeping track of frequency
            for token in tokens:
                modified_token = token.lower()
                if modified_token not in inverted_index:
                    inverted_index[modified_token] = dict()
                if url not in inverted_index[modified_token]:
                    inverted_index[modified_token][url] = 1
                else:
                    inverted_index[modified_token][url] += 1

        # Write to text file
        with open("inverted_index.txt", "w") as f:
            sorted_terms = sorted(inverted_index)
            for term in sorted_terms:
                sentiment = sentiment_score(term, 's')
                f.write("%s %s" % (term, sentiment))
                for posting, frequency in inverted_index[term].items():
                    f.write(" %s %s" % (posting, frequency))
                f.write("\n")


# Retrieves inverted index as a dictionary
def load_inverted_index():
    with open("inverted_index.txt", "r") as f:
        f.readline()  # Discards empty line
        index = {}  # Dictionary representing inverted index

        # Adds each line from file to dictionary
        for line in f.readlines():
            elements = line.split()
            index[elements[0]] = TermDict()

            for i in range(2, len(elements), 2):
                index[elements[0]].sentiment = elements[1]
                index[elements[0]][elements[i]] = elements[i + 1]

    return index


# Scores content based on the afinn dictionary
# Set type to s for strings, l for lists
def sentiment_score(content, s_type='s'):
    afinn = Afinn()  # Afinn dictionary library object
    score = 0.0  # Sentiment score value
    if s_type == 's':
        score = afinn.score(content)
    elif s_type == 'l':
        score = afinn.score(' '.join(content))
    return score


# Creates a "doc_stats.txt" file containing all crawled URL with their length and sentiment value
def create_doc_stats():
    with open("doc_stats.txt", "w") as f:
        with open("result.json", "r") as json_data:
            data = json.load(json_data)  # Retrieves data from json file created by crawler
            doc_stats = collections.OrderedDict()  # Dictionary holding length and sentiment values for all URLs

            for entry in data:
                url = entry["url"]  # Gets URL
                tokens = entry["text"]  # Gets a list of tokens from text
                score = sentiment_score(tokens, 'l')  # Scores all tokens
                doc_stats[url] = (len(tokens), score)  # Sets length and sentiment as stats
                f.write("%s %s %s\n" % (url, len(tokens), score))  # Write URL, length and sentiment values


# Returns a dictionary containing all crawled URL with their length and sentiment value
def load_doc_stats():
    doc_stats = {}

    with open("doc_stats.txt", "r") as f:
        for line in f.readlines():
            parts = line.split(' ')  # Split line into list
            doc_stats[parts[0]] = (int(parts[1]), float(parts[2]))  # Set length and sentiment values to each URL

    return doc_stats


# Returns a list of matching URLs that contain the keyword(s) in the search string.
# It is assumed that the keywords have an implicit AND between them.
def search(search_string, inverted_index):
    search_terms = search_string.split()  # Gets list of query terms
    search_score = sentiment_score(search_string, 's')  # Gets sentiment score for all query terms
    is_positive = search_score >= 0  # Gets whether query is positive or negative
    doc_stats = load_doc_stats()  # Loads length and sentiment values for all docs

    postings_list = list()

    # Creates a list of URLs that each contain all terms in query
    for term in search_terms:
        modified_term = term.lower()
        if modified_term in inverted_index:
            postings_list.append(set(inverted_index[modified_term].keys()))

    # Returns empty list if nothing is found
    if len(postings_list) == 0:
        return list()

    results = postings_list[0]  # Contains all URLs

    # Intersects the sets of each URL
    for postings in postings_list:
        results = results.intersection(postings)

    # Sorts based on the sentiment score of the URLs
    sorted_results = sorted(results, key=lambda x: doc_stats[x][1], reverse=is_positive)
    return sorted_results


# Dictionary class made to hold sentiment values
class TermDict(dict):
    def __init__(self):
        self.sentiment = 0


def run():
    """ run inverted index """
    parser = argparse.ArgumentParser(description='define build settings')
    parser.add_argument('-build', action='store_true')
    args = parser.parse_args()
    if args.build:
        print("building inverted index...")
        create_inverted_index()
        create_doc_stats()
        print("inverted index complete.")
    index = load_inverted_index()
    doc_stats = load_doc_stats()
    while True:
        query = input("\nplease provide a query:\n")
        if query is not None:
            results = search(str(query), index)
            for result in results:
                print(result, doc_stats[result][1])
        else:
            continue


if __name__ == '__main__':
    run()
