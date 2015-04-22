#!coding=utf-8
import json
import math
import recommender_genres
import recommender_actors
import recommender_directors
from collections import Counter
import os


def generate_result(genre_movieid_sim_dict, actor_movieid_sim_dict, director_movieid_sim_dict, num_of_recommended_movies, user_liked_movie_id_list):
    # final_cos_sim_dic = {}

    genre_movieid_sim_counter = Counter(genre_movieid_sim_dict)
    actor_movieid_sim_counter = Counter(actor_movieid_sim_dict)
    director_movieid_sim_counter = Counter(director_movieid_sim_dict)

    combined_movieid_sim_counter = genre_movieid_sim_counter + actor_movieid_sim_counter + director_movieid_sim_counter

    # 乘上rating和releaseYear产生的系数
    imdbrating_file = open(os.path.split(os.path.realpath(__file__))[0] + "/imdbrating.json")
    imdbrating_dict = json.loads(imdbrating_file.readline())
    movieid_releaseyear_file = open(os.path.split(os.path.realpath(__file__))[0] + "/movieid_with_releaseyear.json")
    movieid_releaseyear_dict = json.loads(movieid_releaseyear_file.readline())
    for item in combined_movieid_sim_counter:
        try:
            combined_movieid_sim_counter[item] *= imdbrating_dict[item]
            if movieid_releaseyear_dict[item] < 1990:
                combined_movieid_sim_counter[item] *= 0.6
            elif movieid_releaseyear_dict[item] >= 1990 and movieid_releaseyear_dict[item] < 2000:
                combined_movieid_sim_counter[item] *= 0.7
            elif movieid_releaseyear_dict[item] >= 2000 and movieid_releaseyear_dict[item] < 2010:
                combined_movieid_sim_counter[item] *= 0.8
            elif movieid_releaseyear_dict[item] >= 2010 and movieid_releaseyear_dict[item] < 2020:
                combined_movieid_sim_counter[item] *= 0.9
        except KeyError:
            continue

    print "///////", genre_movieid_sim_counter["tt1905041"], actor_movieid_sim_counter["tt1905041"], combined_movieid_sim_counter["tt1905041"]

    for key in user_liked_movie_id_list:    
        del combined_movieid_sim_counter[key]
        del genre_movieid_sim_counter[key]
        del actor_movieid_sim_counter[key]
        del director_movieid_sim_counter[key]

    final_co_recommended_movies = combined_movieid_sim_counter.most_common(num_of_recommended_movies)
    final_genre_recommended_movies = genre_movieid_sim_counter.most_common(num_of_recommended_movies)
    final_actor_recommended_movies = actor_movieid_sim_counter.most_common(num_of_recommended_movies)
    final_director_recommended_movies = director_movieid_sim_counter.most_common(num_of_recommended_movies)

    # 分数分析
    for item in final_co_recommended_movies:
        print item, ":", genre_movieid_sim_counter[item[0]], actor_movieid_sim_counter[item[0]]


    

    dic_result = dict()
    dic_result["all"] = final_co_recommended_movies
    dic_result["genre"] = final_genre_recommended_movies
    dic_result["actor"] = final_actor_recommended_movies
    dic_result["director"] = final_director_recommended_movies

    return dic_result



def recommend(user_liked_movie_id_list, recommend_method="all"):

    # 以下可分别得到根据genre和mawid推荐出的结果，均为（movied_id: cos_sim_value）这种的字典
    genre_movieid_sim_dict = recommender_genres.recommend(user_liked_movie_id_list)
    actor_movieid_sim_dict = recommender_actors.recommend(user_liked_movie_id_list)
    director_movieid_sim_dict = recommender_directors.recommend(user_liked_movie_id_list)

    num_of_recommended_movies = 10
    result = generate_result(genre_movieid_sim_dict, actor_movieid_sim_dict, director_movieid_sim_dict, num_of_recommended_movies, user_liked_movie_id_list)

    return dict(result[recommend_method]).keys()



###########################################################################
###########################################################################







# user_liked_movie_id_list = ["tt0133093","tt0137523","tt0468569","tt0172495","tt0114369","tt1375666","tt0361862","tt0482571","tt0268978","tt0110322"]
user_liked_movie_id_list = ["tt0468569","tt0137523","tt0114369","tt0110322","tt0172495","tt0133093","tt1375666","tt1345836","tt0109830","tt0814314"]


id_list = recommend(user_liked_movie_id_list)

print "final recommend:", id_list



