def query(q: str, index: dict, doc_store: dict, top_n: int = 10) -> dict[str, dict]:
    # Holds all the url that match the query
    results = {}

    # Holds the top_n results
    return_dict = {}

    # Splits the query into its terms and adds the matching urls into results
    for term in q.split(" "):
        if term in index:
            for url in index[term]:
                if not url in results:
                    results[url] = index[term][url]
                else:
                    results[url] += index[term][url]
    
    # If there are less results than top_n then return all the results
    if len(results) < top_n:
        top_n = len(results)

    # maps urls to the dict so they can be accessed more easily
    doc_store_dict = {doc["url"]: doc for doc in doc_store}

    # Adds the top_n results to the return_dict
    for i in range(top_n):
        max_value = -1
        max_key = ""
        for key, value in results.items():
            if value > max_value:
                max_value = value
                max_key = key
        return_dict[max_key] = doc_store_dict[max_key]
        results.pop(max_key)
    return return_dict