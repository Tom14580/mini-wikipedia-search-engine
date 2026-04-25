import sys

if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "help"

    if command == "crawl":
        from crawler.crawler import crawl
        seed_urls = [
            "https://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Level/4",
            "https://en.wikipedia.org/wiki/Wikipedia:Contents/Overviews",
            "https://en.wikipedia.org/wiki/List_of_lists_of_lists",
            "https://en.wikipedia.org/wiki/Portal:Contents",
            "https://en.wikipedia.org/wiki/Wikipedia:Contents/Outlines",
        ]
        docs = crawl(seed_urls, max_depth=2, max_pages=500)
        print(f"Crawled {len(docs)} pages.")

    elif command == "index":
        from indexer.indexer import build_index
        from utils.helpers import load_json, save_json
        docs = load_json("data/documents.json")
        index = build_index(docs)
        save_json(index, "data/index.json")
        print(f"Indexed {len(docs)} documents, {len(index)} unique terms.")

    elif command == "search":
        from search.search import query
        from utils.helpers import load_json, save_json
        q = input("Enter search query: ")
        docs = load_json("data/documents.json")
        index = load_json("data/index.json")
        result = query(q, index, docs, 10)
        for item in result:
            print(result[item]["url"])
    
    elif command == "serve":
        from web.app import app
        app.run(debug=True)

    else:
        print("Usage: python main.py [crawl | index | serve]")