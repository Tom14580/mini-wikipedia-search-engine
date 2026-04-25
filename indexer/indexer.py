import math
from utils.text_processing import clean
from tqdm import tqdm

def compute_tf(tokens: list[str]) -> dict[str, float]:
    # number of words in page
    total = len(tokens)

    # number of times each term appears in the page
    term_total: dict[str, int] = {}

    # the tf score of each term
    tf_score: dict[str, float] = {}

    # calculates the total number of occurances of each term 
    for token in tokens:
        if not token in term_total:
            term_total[token] = 1
        else:
            term_total[token] += 1
    
    # calculates the tf score of each term (total occurances / total terms in page)
    for term in term_total:
        tf_score[term] = term_total[term] / total
    
    return tf_score

def compute_idf(all_token_lists: list[list[str]]) -> dict[str, float]:
    # total number of token lists
    num_token_lists = len(all_token_lists)

    # stores the number of occurances of each term in the all_tokens_list
    occurances: dict[str, int] = {}

    # idf score for each term
    idf_score: dict[str, float] = {}

    # builds the occurances dictionary
    for token_list in all_token_lists:
        # list of all terms in the token_list
        terms: list[str] = []
        # adds unique terms to the terms list
        for token in token_list:
            if not token in terms:
                terms.append(token)
        # adds number of occurances of each term to occurances
        for term in terms:
            if not term in occurances:
                occurances[term] = 1
            else:
                occurances[term] += 1
    
    # calculates the idf score for each term (log(total num of token lists / num of token lists containing the term))
    for term in occurances:
        idf_score[term] = math.log(num_token_lists / occurances[term])
    
    return idf_score

def build_index(documents: dict[str, dict[str, str]]) -> dict[str, dict[str, float]]:
    # builds a list of document texts
    all_token_lists: list[list[str]] = []

    # adds progress bar for tokenising documents
    for document in tqdm(documents, desc="Tokenising documents"):
        tokens = clean(document["text"])
        all_token_lists.append(tokens)

    # inverted index dictionary
    index: dict[str, dict[str, float]] = {}

    # the idf score of each term in the documents
    idf_score = compute_idf(all_token_lists)

    # builds the index and adds progress bar
    for document in tqdm(documents, desc="Building inverted index"):
        # computes the tf score for a document
        tf_score = compute_tf(clean(document["text"]))
        # adds the tf-idf score to the index at the [term][url] location
        for term in tf_score:
            if term not in index:
                index[term] = {}
            index[term][document["url"]] = tf_score[term] * idf_score[term]
    
    return index