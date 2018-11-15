from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/api/articles', methods=['POST'])
def post_article():
    data = request.json
    print(data.get('header'), data.get('signature'), data.get('body'))
    return "Ok"

@app.route('api/articles', methods=['PUT'])
def update_article():
    pass

if __name__ == "__main__":
    app.run(debug=True)
