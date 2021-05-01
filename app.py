from flask import Flask

app = Flask(__name__)  # only referencing this file
@app.route('/')
def index():
    return "Hello, World"


if __name__ == "__main__":
    app.run(debug=True)