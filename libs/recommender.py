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

    genre_cos_sim_counter = Counter(genre_cos_sim_dic)
    mawid_cos_sim_counter = Counter(mawid_cos_sim_dic)
    releaseyear_cos_sim_counter = Counter(releaseyear_cos_sim_dic)

    combined_cos_sim_counter = genre_cos_sim_counter + mawid_cos_sim_counter

    # 乘上rating和releaseYear产生的系数
    imdbrating_file = open(os.path.split(os.path.realpath(__file__))[0] + "/imdbrating.json")
    imdbrating_dict = json.loads(imdbrating_file.readline())
    for item in combined_cos_sim_counter:
        try:
            combined_cos_sim_counter[item] *= imdbrating_dict[item]
            if releaseyear_cos_sim_dic[item] < 1990:
                combined_cos_sim_counter[item] *= 0.6
            elif releaseyear_cos_sim_dic[item] >= 1990 and releaseyear_cos_sim_dic[item] < 2000:
                combined_cos_sim_counter[item] *= 0.7
            elif releaseyear_cos_sim_dic[item] >= 2000 and releaseyear_cos_sim_dic[item] < 2010:
                combined_cos_sim_counter[item] *= 0.8
            elif releaseyear_cos_sim_dic[item] >= 2010 and releaseyear_cos_sim_dic[item] < 2020:
                combined_cos_sim_counter[item] *= 0.9
        except KeyError:
            continue

    print "///////", genre_cos_sim_counter["tt1905041"], mawid_cos_sim_counter["tt1905041"], combined_cos_sim_counter["tt1905041"]

    # for key in user_liked_movie_id_list:    
    #     del combined_cos_sim_counter[key]
    #     del genre_cos_sim_counter[key]
    #     del mawid_cos_sim_counter[key]

    final_co_recommended_movies = combined_cos_sim_counter.most_common(num_of_recommended_movies)
    final_genre_recommended_movies = genre_cos_sim_counter.most_common(num_of_recommended_movies)
    final_mawid_recommended_movies = mawid_cos_sim_counter.most_common(num_of_recommended_movies)
    final_releaseyear_recommended_movies = releaseyear_cos_sim_counter.most_common(num_of_recommended_movies)

    # 分数分析
    for item in final_co_recommended_movies:
        print item, ":", genre_cos_sim_counter[item[0]], mawid_cos_sim_counter[item[0]], releaseyear_cos_sim_counter[item[0]]



    print 'final_co_recommended_movies:', final_co_recommended_movies
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
    print "+++++++", sum(genre_cos_sim_dic.values())
    mawid_cos_sim_dic = mawid_recommender.recommend(user_liked_movie_id_list)
    releaseyear_cos_sim_dic = releaseyear_recommender.recommend(user_liked_movie_id_list)

    num_of_recommended_movies = 20
    result = generate_result(genre_cos_sim_dic, mawid_cos_sim_dic, releaseyear_cos_sim_dic, num_of_recommended_movies, user_liked_movie_id_list)
    print result
    return dict(result[recommend_method]).keys()



###########################################################################
###########################################################################







user_liked_movie_id_list = ["tt0133093","tt0137523","tt0468569","tt0172495","tt0114369","tt1375666","tt0361862","tt0482571","tt0268978","tt0110322"]

id_list = recommend(user_liked_movie_id_list)

print "final recommend:", id_list



