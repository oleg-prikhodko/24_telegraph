from uuid import uuid1

import articles
from flask import Flask, render_template, request, make_response, session, abort

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
def form():
    if "userid" not in session:
        session["userid"] = uuid1().hex

    return render_template("form.html")


@app.route("/articles")
def list_articles():
    article_list = articles.load_all_articles()
    return render_template("list.html", article_list=article_list)


@app.route("/articles/<article_id>")
def get_article_page(article_id):
    article = articles.load_article(article_id)
    if article is None:
        abort(404)

    return render_template("article.html", article=article)


@app.route("/api/articles", methods=["POST"])
def save_article():
    response = make_response("OK")

    data = request.json
    print(data.get("header"), data.get("signature"), data.get("body"))

    return response


@app.route("/sessiontest")
def session_test():
    return "userid: {}".format(session.get("userid"))


@app.route("/api/articles", methods=["PUT"])
def update_article():
    pass


if __name__ == "__main__":
    app.run(debug=True)
