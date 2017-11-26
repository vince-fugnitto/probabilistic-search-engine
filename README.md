# Information Retrieval Sentiment Ranking
Experiment with web crawling, scrape and index a set of web documents, use the sentiment dictionary aFinn to associate sentiment values to the index, make document ranking reflect sentiment.


### Prerequisites


```
pip install scrapy --user
```

### Usage

Spider
 * -max {value}: specifies max bound for url crawling. default=10

```
python spider.py
python spider.py -max {value}
```

Inverted Index
* -build: 'optional': if specified, inverted index is built

```
python inverted_index.py
python inverted_index.py -build
```
