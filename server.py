from flask import Flask, render_template, request, make_response, session
from uuid import uuid1

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
def form():
    if "userid" not in session:
        session["userid"] = uuid1().hex

    return render_template("form.html")


@app.route("/api/articles", methods=["POST"])
def post_article():
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
