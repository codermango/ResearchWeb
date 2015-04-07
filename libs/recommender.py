#!coding=utf-8
import json
import math
import genre_recommender
import mawid_recommender
from collections import Counter
import os

def generate_user_genre_preference_vector(list_user_liked_movie_id, dic_id_with_genre):
    
    list_of_liked_movie_genre_vector = []
    dimension_of_genre_vector = len(dic_id_with_genre.values()[0]) #用于下面生成0向量

    for id in list_user_liked_movie_id:
        try:
            list_of_liked_movie_genre_vector.append(dic_id_with_genre[id])
        except KeyError:
            continue

    #print list_of_liked_movie_genre_vector
    if list_of_liked_movie_genre_vector:   #如果为空，则以下reduce计算不了
        user_preference_vector = reduce(lambda x, y: [m + n for m, n in zip(x, y)], list_of_liked_movie_genre_vector)
    else:
        user_preference_vector = [0] * dimension_of_genre_vector

    #print 'user_preference_vector: ', user_preference_vector

    return user_preference_vector


def generate_user_mawid_preference_dic(user_liked_movie_id_list, dic_id_with_mawid):
    user_mawid_preference_dic = {}

    user_mawid_list = []

    for movie_id in user_liked_movie_id_list:
        try:
            user_mawid_list += dic_id_with_mawid[movie_id]
        except KeyError:
            continue

    user_mawid_set_list = list(set(user_mawid_list))

    for item in user_mawid_set_list:
        mawid_count = user_mawid_list.count(item)
        # 把数量为1的全部去除
        if mawid_count > 1:
            user_mawid_preference_dic[item] = user_mawid_list.count(item)

    return user_mawid_preference_dic


def get_sum_of_all_mawid_in_all_movies(dic_id_with_mawid):

    mawid_list = dic_id_with_mawid.values()
    result = sum(map(lambda x: len(x), mawid_list))
    # print 'sum_of_all_mawid_in_all_movies:',result
    return result


def get_sum_of_every_mawid_dic(mawid_with_count_file):
    mawid_with_count_file = open(mawid_with_count_file)
    content = json.loads(mawid_with_count_file.readline())

    return content



def generate_result(genre_cos_sim_dic, mawid_cos_sim_dic, num_of_recommended_movies, user_liked_movie_id_list):
    final_cos_sim_dic = {}

    if not genre_cos_sim_dic.values()[0]:
        genre_cos_sim_dic = {}


    genre_cos_sim_counter = Counter(genre_cos_sim_dic)
    mawid_cos_sim_counter = Counter(mawid_cos_sim_dic)

    combined_cos_sim_counter = genre_cos_sim_counter + mawid_cos_sim_counter
    
    for key in user_liked_movie_id_list:    
        del combined_cos_sim_counter[key]
        del genre_cos_sim_counter[key]
        del mawid_cos_sim_counter[key]

    final_co_recommended_movies = combined_cos_sim_counter.most_common(num_of_recommended_movies)
    final_genre_recommended_movies = genre_cos_sim_counter.most_common(num_of_recommended_movies)
    final_mawid_recommended_movies = mawid_cos_sim_counter.most_common(num_of_recommended_movies)

    # print 'final_co_recommended_movies:', final_co_recommended_movies
    # print final_genre_recommended_movies
    # print final_mawid_recommended_movies

    dic_result = dict()
    dic_result["all"] = final_co_recommended_movies
    dic_result["genre"] = final_genre_recommended_movies
    dic_result["mawid"] = final_mawid_recommended_movies

    return dic_result



def recommend(user_liked_movie_id_list, recommend_method="all"):
    ################################################################################
    # 为genre推荐的前期处理
    movie_genre_vector_file = open(os.path.split(os.path.realpath(__file__))[0] + "/movie_genre_vector.json")
    id_with_genre_dic = json.loads(movie_genre_vector_file.readline())
    user_genre_preference_vector = generate_user_genre_preference_vector(user_liked_movie_id_list, id_with_genre_dic)


    ##########################################################################################
    # 为mawid推荐的前期处理
    movie_id_with_mawid_file = open(os.path.split(os.path.realpath(__file__))[0] + '/movie_id_with_mawid.json')
    id_with_mawid_dic = json.loads(movie_id_with_mawid_file.readline())
    user_mawid_preference_dic = generate_user_mawid_preference_dic(user_liked_movie_id_list, id_with_mawid_dic)

    # 此值在外部算好，避免进入循环增大计算量
    sum_of_all_mawid_in_all_movies = get_sum_of_all_mawid_in_all_movies(id_with_mawid_dic)
    # generate_sum_of_every_mawid_dic(id_with_mawid_dic)  此操作很费时，提前算好存入文件mawid_with_count.json
    sum_of_every_mawid_dic = get_sum_of_every_mawid_dic(os.path.split(os.path.realpath(__file__))[0] + '/mawid_with_count.json')

    # 以下可分别得到根据genre和mawid推荐出的结果，均为（movied_id: cos_sim_value）这种的字典
    genre_cos_sim_dic = genre_recommender.recommend(user_genre_preference_vector, id_with_genre_dic)
    mawid_cos_sim_dic = mawid_recommender.recommend(user_mawid_preference_dic, id_with_mawid_dic, sum_of_all_mawid_in_all_movies, sum_of_every_mawid_dic)

    num_of_recommended_movies = 20
    result = generate_result(genre_cos_sim_dic, mawid_cos_sim_dic, num_of_recommended_movies, user_liked_movie_id_list)
    return dict(result[recommend_method]).keys()



###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################




# my_liked_movie_id_file = open("mark_liked_movie_id.txt")
# 把文件中的id放入list
# user_liked_movie_id_list = ["tt2820852", "tt2820852"]
# # for line_of_my_liked_movie_list in my_liked_movie_id_file:
# #     user_liked_movie_id_list.append(line_of_my_liked_movie_list.strip())
# # print user_liked_movie_id_list

# id_list = recommend(user_liked_movie_id_list)

# print id_list



