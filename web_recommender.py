import sys
sys.path.append(".")
from flask import Flask, url_for, render_template, request
import libs.recommender 

app = Flask(__name__)

@app.route("/web_recommender/", methods=["GET"])
def web_recommender():
    return render_template("web_recommender.html")


@app.route("/web_recommender/result/", methods=["POST"])
def web_recommender_result():
    if request.method == "POST":
        ids = request.form["ids"]
        ids_list = ids.split("\n")
        trimed_ids_list = map(lambda x: x.strip(), ids_list)

        recommended_ids = libs.recommender.recommend(trimed_ids_list)

        return render_template("web_recommender.html", liked_ids=trimed_ids_list, recommended_ids=recommended_ids)
        


if __name__ == '__main__':
    app.run(debug=True)