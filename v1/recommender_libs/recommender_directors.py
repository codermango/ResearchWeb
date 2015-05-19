#!coding=utf-8
from __future__ import division
import json
import math
import os


def generate_user_directorid_preference_dict(user_liked_movieid_list, movieid_directorid_dict):
    user_directorid_preference_dict = {}

    user_directorid_list = []

    for movieid in user_liked_movieid_list:
        try:
            user_directorid_list += movieid_directorid_dict[movieid]
        except KeyError:
            continue

    user_directorid_set_list = list(set(user_directorid_list))

    for item in user_directorid_set_list:
        director_count = user_directorid_list.count(item)
        # 把数量为1的全部去除
        if director_count > 1:
            user_directorid_preference_dict[item] = director_count

    return user_directorid_preference_dict


def get_sum_of_every_directorid_dict(directorid_with_imdbid_file_path):
    directorid_with_imdbid_file = open(directorid_with_imdbid_file_path)
    directorid_imdbid_dict = json.loads(directorid_with_imdbid_file.readline())

    return directorid_imdbid_dict


def get_cos_sim(user_directorid_preference_dict, movieid_directorid_dict, directorid_list, user_liked_movie_id_list, sum_of_every_directorid_dict):
    user_directorid_preference_dict_keys = user_directorid_preference_dict.keys()
    # 首先把两个列表的元素组合在一起
    difference_list = list(set(directorid_list).difference(set(user_directorid_preference_dict_keys)))
    # print 'difference_list:', difference_list

    user_directorid_preference_dict_tmp = {}
    user_directorid_preference_dict_tmp.update(user_directorid_preference_dict)
    map(lambda x: user_directorid_preference_dict_tmp.update({x: 0}), difference_list)
    
    
    directorid_list_dict = {}
    map(lambda x: directorid_list_dict.update({x: 0}), user_directorid_preference_dict_tmp.keys())

    # print directorid_list_dict.values()

    map(lambda x: directorid_list_dict.update({x: 1}), directorid_list)

    # print 'directorid_list_dict:', directorid_list_dict


    # 然后算出tf-idf
    sum_of_user_liked_movies = len(user_liked_movie_id_list)
    sum_of_all_movies = len(movieid_directorid_dict)

    tf_dic = {}
    for k, v in user_directorid_preference_dict_tmp.items():
        tf_dic[k] = v / sum_of_user_liked_movies

    # print 'tf_idc:', tf_dic

    idf_dic = {}
    for i, j in user_directorid_preference_dict_tmp.items():
        idf_dic[i] = sum_of_all_movies / len(sum_of_every_directorid_dict[i])
    # print 'idf_dic:', idf_dic

    tfidf_dic = {}
    for key in tf_dic.keys():
        tfidf_dic[key] = (tf_dic[key] * idf_dic[key]) ** 2
    # print 'tfidf_dic:', tfidf_dic
    # print 'directorid_list_dict:', directorid_list_dict
    #最后算出cos相似度
    
    user_directorid_preference_dict_tmp_keys = user_directorid_preference_dict_tmp.keys()
    directorid_list_dict_value = directorid_list_dict.values()
    tfidf_dic_value = tfidf_dic.values()

    num1 = sum(map(lambda x: directorid_list_dict[x] * tfidf_dic[x], user_directorid_preference_dict_tmp_keys))
    # print 'num1:', num1
    tmp1 = math.sqrt(sum([x ** 2 for x in directorid_list_dict_value]))
    tmp2 = math.sqrt(sum([x ** 2 for x in tfidf_dic_value]))
    num2 = tmp1 * tmp2  # num2=sqrt(a1^2+a2^2+a3^2) * sqrt(b1^2+b2^2+b3^2)
    # print 'num2:', num2
    cos_value = num1 / num2

    return cos_value


def get_cos_sim_dict(user_directorid_preference_dict, movieid_directorid_dict, user_liked_movieid_list, sum_of_every_directorid_dict):

    user_directorid_preference_dict_keys = user_directorid_preference_dict.keys()

    movieid_sim_dict = {}
    for k, v in movieid_directorid_dict.items():

        directorid_list = v
        intersection_list = list(set(directorid_list).intersection(set(user_directorid_preference_dict_keys)))

        if not intersection_list:
            movieid_sim_dict[k] = 0
            continue

        sim = get_cos_sim(user_directorid_preference_dict, movieid_directorid_dict, directorid_list, user_liked_movie_id_list, sum_of_every_directorid_dict)

        movieid_sim_dict[k] = sim

    return movieid_sim_dict


def recommend(user_liked_movieid_list):
    
    movieid_with_directorid_file = open(os.path.split(os.path.realpath(__file__))[0] + '/imdbid_directors.json')
    movieid_directorid_dict = json.loads(movieid_with_directorid_file.readline())
    user_directorid_preference_dict = generate_user_directorid_preference_dict(user_liked_movieid_list, movieid_directorid_dict)
    print user_directorid_preference_dict

    sum_of_every_directorid_dict = get_sum_of_every_directorid_dict(os.path.split(os.path.realpath(__file__))[0] + '/director_imdbids.json')


    cos_sim_dict = get_cos_sim_dict(user_directorid_preference_dict, movieid_directorid_dict, user_liked_movieid_list, sum_of_every_directorid_dict)

    return cos_sim_dict
###################################################################################################




user_liked_movie_id_list = ["tt0133093","tt0137523","tt0468569","tt0172495","tt0114369","tt1375666","tt0361862","tt0482571","tt0268978","tt0110322"]

# id_list = recommend(user_liked_movie_id_list)

# print "final recommend:", id_list