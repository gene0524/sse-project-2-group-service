## Just for reference, copied from lab10
from flask import Flask, jsonify, request
from books import books

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    query = request.args.get("query")
    filter = request.args.get("filter")

    if query and filter:
        filtered_data = [i for i in books if str.lower(query) in str.lower(str(i[filter]))]
        return jsonify(filtered_data)

    return jsonify(books)
