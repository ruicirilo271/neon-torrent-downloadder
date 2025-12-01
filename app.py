# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
import cloudscraper

app = Flask(__name__)

YTS_LIST = "https://yts.lt/api/v2/list_movies.json"
YTS_DETAILS = "https://yts.lt/api/v2/movie_details.json"
YTS_SUGGESTIONS = "https://yts.lt/api/v2/movie_suggestions.json"

# Cloudflare bypass
scraper = cloudscraper.create_scraper(
    browser={
        "browser": "chrome",
        "platform": "windows",
        "mobile": False
    }
)

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

    try:
        r = scraper.get(YTS_LIST, params=params, timeout=10)
        data = r.json()
    except Exception as e:
        return jsonify({"error": "Invalid JSON from YTS", "details": str(e)}), 500

    if data.get("status") != "ok":
        return jsonify({"error": "API failed"}), 400

    return jsonify(data["data"].get("movies", []))


@app.route("/movie/<int:movie_id>")
def movie_page(movie_id):
    return render_template("movie.html", movie_id=movie_id)


@app.route("/api/details/<int:movie_id>")
def get_details(movie_id):
    params = {"movie_id": movie_id, "with_images": True, "with_cast": True}

    try:
        r = scraper.get(YTS_DETAILS, params=params, timeout=10)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": "Invalid JSON from YTS", "details": str(e)}), 500


@app.route("/api/suggestions/<int:movie_id>")
def get_suggestions(movie_id):
    params = {"movie_id": movie_id}

    try:
        r = scraper.get(YTS_SUGGESTIONS, params=params, timeout=10)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": "Invalid JSON from YTS", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
