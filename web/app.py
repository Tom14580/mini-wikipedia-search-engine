from flask import Flask, request, render_template
from utils.helpers import load_json
from search.search import query as run_query
from pathlib import Path

# get template directory
SCRIPT_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = SCRIPT_DIR / "web/templates"

# setup app with template directory
app = Flask(__name__, template_folder=str(TEMPLATE_DIR))

# Load once at startup — not on every request
INDEX = load_json("data/index.json")
DOC_STORE = load_json("data/documents.json")

# return index
@app.route("/")
def home():
    return render_template("index.html", results=None)

# fetch the search results and pass them into index
@app.route("/search")
def search():
    query = request.args.get("q")
    if query == None:
        return render_template("index.html", results=None)
    response = run_query(query, INDEX, DOC_STORE, 10)
    return render_template("index.html", results=response)