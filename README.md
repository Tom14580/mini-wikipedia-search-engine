# Mini Search Engine

## Description

This is a mini search engine that I have built to crawl Wikipedia. It indexes pages using **TF‑IDF** (Term Frequency‑Inverse Document Frequency), and provides a web interface to search the crawled pages. I built this to learn about and demonstrate inverted index data structures, TF-IDF ranking, and pipeline architecture.

## How to run it

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Crawl pages (start from a few Wikipedia seeds configured in `main.py`). This saves raw HTML into `data/documents.json`
```bash
python main.py crawl
```

3. Build the inverted index. This produces `data/index.json`
```bash
python main.py index
```

4. Start the web server (flask)
```bash
python main.py serve
```

**or**

Search in the terminal
```bash
python main.py search
```

## How it works

1. Crawling - A bredth-first search is run starting with the seed URLs in the queue. It crawls to a configures depth with a max number of pages. URLs are filtered to only crawl .en domain URLs and only main articles. URL fragments are also removed. It fetches each page using requests and BeautifulSoup and cleans the HTML to remove punctuation and common words and it separates each term in a list.

2. Indexing - An IDF score is first calculated from the documents crawled (log(total num of token lists / num of token lists containing the term)). Then for each document, a TF score is calculated (total occurances / total terms in page) and the term along with TF-IDF score (TF score * IDF score) is added to the inverted index

3. Searching - Each word in the query is searched individually and the TF-IDF score of the same page for different terms are added together so pages with multiple terms are given a higher weighting. It then returns the top_n results (passed into the function). This search can be queried from the terminal or from within the web app.

## Design Decisions

**BFS over DFS for crawling:** a BFS will visit all pages at a given depth before moving to the next. As the max pages crawled is limited, this is better because it will visit a wider ranger of pages whereas a DFS will travel down one branch so will discover lots of related articles. So a BFS results in a more varied index.

**TF-IDF over raw frequency:** raw frequency only counts how many times a word appears. So long documents with lots of common words will rank high. With TF-IDF, TF will account for document length and IDF will account for how common a term is so it ensures results are relevant.

**JSON over SQLite:** This search engine is only designed to crawl a few hundred documents so JSON is easier to read and debug. SQLite would be overcomplicated for this project, the focus should be on the crawler and indexer. SQLite would be better if I wanted to scale this as it stores the index on disk and supports incremental updates without rewriting the entire file every time.

## What I would change if I wanted to scale this

If the index grew in size I would have to change the current architecture:

- Store the inverted index on disk (e.g., using SQLite or LMDB)
- Move to distributed crawling – multiple workers fetching pages in parallel, respecting robots.txt and rate limits
- Replace the simple BFS with a priority queue that prioritises high quality pages (e.g. based on PageRank)
