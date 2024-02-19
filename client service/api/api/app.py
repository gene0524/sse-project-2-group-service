## Not Done Yet / Copied from lab10

from flask import Flask, render_template, request
import requests
import os
import urllib.parse

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/books", methods=["GET"])
def book_search():
    url_api = os.getenv("BOOK_API_URL")

    query = urllib.parse.quote(request.args.get("query"), safe='')
    filter = urllib.parse.quote(request.args.get("filter"), safe='')

    if query and filter:
        url_api += f"/?query={query}&filter={filter}"

    response = requests.get(url_api)
    data = response.json()
    
    return render_template("books.html", results=data)