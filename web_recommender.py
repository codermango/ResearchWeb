import sys
import os
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
        ids = request.form["movieId"]

        ids_list = ids.split(",")
        trimed_ids_list = map(lambda x: x.strip(), ids_list)

        genre_recommended_ids = libs.recommender.recommend(trimed_ids_list, "genre")
        mawid_recommended_ids = libs.recommender.recommend(trimed_ids_list, "mawid")
        all_recommended_ids = libs.recommender.recommend(trimed_ids_list, "all")

        return render_template("web_recommender.html", liked_ids=trimed_ids_list, genre_recommended_ids=genre_recommended_ids, mawid_recommended_ids=mawid_recommended_ids, all_recommended_ids=all_recommended_ids)



#====================================================================================================
def get_file_count(dir):
    return sum([len(files) for root,dirs,files in os.walk(dir)])


if __name__ == '__main__':
    app.run(debug=True)