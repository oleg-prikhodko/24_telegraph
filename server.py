from uuid import uuid1
import os

import articles
from flask import Flask, render_template, request, session, abort, redirect

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

NOT_FOUND_STATUS = 404
FORBIDDEN_STATUS = 403
INTERNAL_ERROR_STATUS = 500

DEFAULT_PORT = 5000

def authenticate():
    if "userid" not in session:
        session["userid"] = uuid1().hex


@app.route("/")
def form():
    authenticate()
    return render_template("form.html")


@app.route("/articles/")
def list_articles():
    authenticate()
    article_list = articles.load_all_articles()
    return render_template("index.html", article_list=article_list)


@app.route("/articles/<article_id>")
def get_article_page(article_id):
    authenticate()
    article = articles.load_article(article_id)
    if article is None:
        abort(NOT_FOUND_STATUS)

    return render_template("article.html", article=article)


@app.route("/post", methods=["POST"])
def save_article():
    authenticate()
    article_id = articles.save_article(
        session.get("userid"),
        request.form.get("header"),
        request.form.get("signature"),
        request.form.get("body"),
    )

    return redirect("/articles/{}".format(article_id))


@app.route("/edit/<article_id>")
def get_edit_page(article_id):
    authenticate()
    article = articles.load_article(article_id)
    if article is None:
        abort(NOT_FOUND_STATUS)
    if article["userid"] != session.get("userid"):
        abort(FORBIDDEN_STATUS)

    return render_template("form.html", article=article)


@app.route("/edit/<article_id>", methods=["POST"])
def edit_article(article_id):
    authenticate()
    article = articles.load_article(article_id)
    if article is None:
        abort(NOT_FOUND_STATUS)
    if article["userid"] != session.get("userid"):
        abort(FORBIDDEN_STATUS)

    success = articles.update_article(
        article_id,
        request.form.get("header"),
        request.form.get("signature"),
        request.form.get("body"),
    )

    if success:
        return redirect("/articles/{}".format(article_id))
    else:
        abort(INTERNAL_ERROR_STATUS)


@app.route("/sessiontest")
def session_test():
    return "userid: {}".format(session.get("userid"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", DEFAULT_PORT))
    app.run(debug=True, host="0.0.0.0", port=port)
