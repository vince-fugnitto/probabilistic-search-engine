# Information Retrieval Sentiment Ranking
Experiment with web crawling, scrape and index a set of web documents, use the sentiment dictionary aFinn to associate sentiment values to the index, make document ranking reflect sentiment.


### Prerequisites


```
pip install scrapy --user
```

### Usage

A step by step series of examples that tell you have to get a development env running

Spider

```
python spider.py
python spider.py -max {value}
```

Inverted Index

```
python inverted_index.py
python inverted_index.py -build
```
