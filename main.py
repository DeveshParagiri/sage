from flask import Flask, render_template, request
from utils import setup_dbqa

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    try:
        return get_chat_response(input)
    except ValueError:
        return "You have exceeded the token limit! Sorry for the inconvenience!"

def get_chat_response(input):
    response = dbqa({'query': input})
    return response['result']

if __name__ == "__main__":
    dbqa = setup_dbqa()
    app.run(debug=True, port=2000)