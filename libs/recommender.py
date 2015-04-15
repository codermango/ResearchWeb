#!coding=utf-8
import json
import math
import genre_recommender
import mawid_recommender
import releaseyear_recommender
from collections import Counter
import os


def generate_result(genre_cos_sim_dic, mawid_cos_sim_dic, releaseyear_cos_sim_dic, num_of_recommended_movies, user_liked_movie_id_list):
    final_cos_sim_dic = {}

    if not genre_cos_sim_dic.values()[0]:
        genre_cos_sim_dic = {}


    genre_cos_sim_counter = Counter(genre_cos_sim_dic)
    mawid_cos_sim_counter = Counter(mawid_cos_sim_dic)
    releaseyear_cos_sim_counter = Counter(releaseyear_cos_sim_dic)

    combined_cos_sim_counter = genre_cos_sim_counter + mawid_cos_sim_counter + releaseyear_cos_sim_counter
    
    # for key in user_liked_movie_id_list:    
    #     del combined_cos_sim_counter[key]
    #     del genre_cos_sim_counter[key]
    #     del mawid_cos_sim_counter[key]

    final_co_recommended_movies = combined_cos_sim_counter.most_common(num_of_recommended_movies)
    final_genre_recommended_movies = genre_cos_sim_counter.most_common(num_of_recommended_movies)
    final_mawid_recommended_movies = mawid_cos_sim_counter.most_common(num_of_recommended_movies)
    final_releaseyear_recommended_movies = releaseyear_cos_sim_counter.most_common(num_of_recommended_movies)

    # print 'final_co_recommended_movies:', final_co_recommended_movies
    # print final_genre_recommended_movies
    # print final_mawid_recommended_movies

    dic_result = dict()
    dic_result["all"] = final_co_recommended_movies
    dic_result["genre"] = final_genre_recommended_movies
    dic_result["mawid"] = final_mawid_recommended_movies
    dic_result["releaseyear"] = final_releaseyear_recommended_movies

    return dic_result



def recommend(user_liked_movie_id_list, recommend_method="all"):

    # 以下可分别得到根据genre和mawid推荐出的结果，均为（movied_id: cos_sim_value）这种的字典
    genre_cos_sim_dic = genre_recommender.recommend(user_liked_movie_id_list)
    mawid_cos_sim_dic = mawid_recommender.recommend(user_liked_movie_id_list)
    releaseyear_cos_sim_dic = releaseyear_recommender.recommend(user_liked_movie_id_list)

    num_of_recommended_movies = 10
    result = generate_result(genre_cos_sim_dic, mawid_cos_sim_dic, releaseyear_cos_sim_dic, num_of_recommended_movies, user_liked_movie_id_list)
    print result
    return dict(result[recommend_method]).keys()



###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################




# my_liked_movie_id_file = open("mark_liked_movie_id.txt")
# 把文件中的id放入list
user_liked_movie_id_list = ["tt0348124","tt0401398","tt0486761","tt0181196","tt0389074","tt0279967","tt0969647","tt0097757","tt0103639"]
# # # for line_of_my_liked_movie_list in my_liked_movie_id_file:
# # #     user_liked_movie_id_list.append(line_of_my_liked_movie_list.strip())
# # # print user_liked_movie_id_list

#user_liked_movie_id_list = ["tt1229821","tt0401398"]
id_list = recommend(user_liked_movie_id_list)

print "final recommend:", id_list



