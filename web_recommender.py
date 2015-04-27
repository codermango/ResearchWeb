import sys
import os
sys.path.append(".")
from flask import Flask, url_for, render_template, request, Response
import recommender_libs.recommender 

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

        genre_recommended_ids = recommender_libs.recommender.recommend(trimed_ids_list, "genre")
        actor_recommended_ids = recommender_libs.recommender.recommend(trimed_ids_list, "actor")
        director_recommended_ids = recommender_libs.recommender.recommend(trimed_ids_list, "director")
        all_recommended_ids = recommender_libs.recommender.recommend(trimed_ids_list, "all")

        return render_template("web_recommender.html", liked_ids=trimed_ids_list, genre_recommended_ids=genre_recommended_ids, actor_recommended_ids=actor_recommended_ids, director_recommended_ids=director_recommended_ids, all_recommended_ids=all_recommended_ids)

        # return Response(render_template("web_recommender.html"),generate_recommend_movies(trimed_ids_list))



def generate_recommend_movies(trimed_ids_list):
    all_recommended_ids = recommender_libs.recommender.recommend(trimed_ids_list, "all")
    yield "all_recommended_ids"
    #yield render_template("web_recommender.html")
    





#====================================================================================================
def get_file_count(dir):
    return sum([len(files) for root,dirs,files in os.walk(dir)])


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)