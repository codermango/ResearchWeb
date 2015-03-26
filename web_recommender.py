from flask import Flask, url_for, render_template, request

app = Flask(__name__)

@app.route("/recommender/", methods=["GET"])
def recommender():
    return render_template("recommender.html")


@app.route("/recommender/result/", methods=["POST"])
def recommender_result():
    if request.method == "POST":
        ids = request.form["ids"]
        return ids


if __name__ == '__main__':
    app.run(debug=True)