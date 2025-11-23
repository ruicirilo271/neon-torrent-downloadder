# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

YTS_LIST = "https://yts.lt/api/v2/list_movies.json"
YTS_DETAILS = "https://yts.lt/api/v2/movie_details.json"
YTS_SUGGESTIONS = "https://yts.lt/api/v2/movie_suggestions.json"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search_movies():
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "query missing"}), 400

    params = {
        "query_term": query,
        "limit": 50,
        "sort_by": "download_count"
    }

    r = requests.get(YTS_LIST, params=params, timeout=10).json()

    if r.get("status") != "ok":
        return jsonify({"error": "API failed"}), 400

    return jsonify(r["data"].get("movies", []))


@app.route("/movie/<int:movie_id>")
def movie_page(movie_id):
    return render_template("movie.html", movie_id=movie_id)


@app.route("/api/details/<int:movie_id>")
def get_details(movie_id):
    params = {"movie_id": movie_id, "with_images": True, "with_cast": True}
    data = requests.get(YTS_DETAILS, params=params, timeout=10).json()
    return jsonify(data)


@app.route("/api/suggestions/<int:movie_id>")
def get_suggestions(movie_id):
    params = {"movie_id": movie_id}
    data = requests.get(YTS_SUGGESTIONS, params=params, timeout=10).json()
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
