from bs4 import BeautifulSoup
import re

# A set of common words to filter out of html (a set has O(1) lookup)
stop_words: set[str] = {
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and',
    'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below',
    'between', 'both', 'but', 'by', 'can', 'did', 'do', 'does', 'doing', 'don',
    'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'has',
    'have', 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself',
    'his', 'how', 'if', 'in', 'into', 'is', 'it', 'its', 'itself', 'let\'s',
    'me', 'more', 'most', 'mustn', 'my', 'myself', 'no', 'nor', 'not', 'of',
    'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves',
    'out', 'over', 'own', 'same', 'shan', 'she', 'should', 'so', 'some', 'such',
    'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then',
    'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under',
    'until', 'up', 'very', 'was', 'we', 'were', 'what', 'when', 'where', 'which',
    'while', 'who', 'whom', 'why', 'with', 'you', 'your', 'yours', 'yourself',
    'yourselves', 'could', 'would', 'should', 'might', 'must', 'need', 'dare',
    'used', 'via', 'vs', 'etc', 'including', 'particularly', 'especially',
    'thus', 'hence', 'whereas', 'wherever', 'whoever', 'whichever', 'whenever',
    'whereupon', 'wherewith', 'whereby', 'wherein', 'whereof', 'wheresoever',
    'thyself', 'thy', 'thine', 'ye', 'upon', 'among', 'amongst', 'throughout',
    'along', 'without', 'within', 'beyond', 'plus', 'minus', 'times', 'per',
    'by', 'via', 'versus', 'circa', 'apropos', 'regarding', 'notwithstanding'
}

# Takes raw html and returns the individual words separated by spaces, also removes boilerplate HTML
def strip_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")
    
    # Remove script, style and navigation elements
    for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
        element.decompose()
    
    return soup.get_text(separator=" ", strip=True)

# Takes a string of words and lowercases them, removing punctuation
def tokenise(text: str) -> list[str]:
    return re.findall(r'[a-z]+', text.lower())

# Removes common words from a pre-defined set
def remove_stop_words(tokens: list[str]) -> list[str]:
    return [word for word in tokens if word not in stop_words]

# Puts the functions together to return the processed text from raw html
def clean(raw_html: str) -> list[str]:
    text = strip_html(raw_html)
    tokens = tokenise(text)
    return remove_stop_words(tokens)