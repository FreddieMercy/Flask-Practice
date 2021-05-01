from flask import Flask, render_template

app = Flask(__name__)  # only referencing this file
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)