from flask import Flask, url_for, render_template

app = Flask(__name__)

@app.route("/")
def recommender():
    return render_template("recommender.html")


if __name__ == '__main__':
    app.run(debug=True)