#!coding=utf-8
from __future__ import division
import json
import math
import os



def get_sum_of_every_actorid_dic(actorid_with_imdbid_file):
    actorid_with_imdbid_f = open(actorid_with_imdbid_file)
    actorid_imdbid_dict = json.loads(actorid_with_imdbid_f.readline())

    return actorid_imdbid_dict



def generate_user_actorid_preference_dic(user_liked_movie_id_list, dic_id_with_mawid):
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



def get_cos_sim(user_mawid_preference_dic, id_with_mawid_dict, mawid_list, user_liked_movie_id_list, sum_of_every_actorid_dic):

    user_mawid_preference_dic_keys = user_mawid_preference_dic.keys()
    # 首先把两个列表的元素组合在一起
    difference_list = list(set(mawid_list).difference(set(user_mawid_preference_dic_keys)))
    # print 'difference_list:', difference_list

    user_mawid_preference_dic_tmp = {}
    user_mawid_preference_dic_tmp.update(user_mawid_preference_dic)
    map(lambda x: user_mawid_preference_dic_tmp.update({x: 0}), difference_list)
    # print user_mawid_preference_dic_tmp
    
    mawid_list_dic = {}
    map(lambda x: mawid_list_dic.update({x: 0}), user_mawid_preference_dic_tmp.keys())

    # print mawid_list_dic.values()

    map(lambda x: mawid_list_dic.update({x: 1}), mawid_list)

    # print 'mawid_list_dic:', mawid_list_dic


    # 然后算出tf-idf
    sum_of_user_liked_movies = len(user_liked_movie_id_list)
    sum_of_all_movies = len(id_with_mawid_dict)
    
    tf_dic = {}
    for k, v in user_mawid_preference_dic_tmp.items():
        tf_dic[k] = v / sum_of_user_liked_movies

    # print 'tf_idc:', tf_dic

    idf_dic = {}
    for i, j in user_mawid_preference_dic_tmp.items():
        idf_dic[i] = sum_of_all_movies / len(sum_of_every_actorid_dic[i])
    # print 'idf_dic:', idf_dic

    tfidf_dic = {}
    for key in tf_dic.keys():
        tfidf_dic[key] = (tf_dic[key] * idf_dic[key]) ** 2
    # print 'tfidf_dic:', tfidf_dic
    # print 'mawid_list_dic:', mawid_list_dic
    #最后算出cos相似度
    
    user_mawid_preference_dic_tmp_keys = user_mawid_preference_dic_tmp.keys()
    mawid_list_dic_value = mawid_list_dic.values()
    tfidf_dic_value = tfidf_dic.values()

    num1 = sum(map(lambda x: mawid_list_dic[x] * tfidf_dic[x], user_mawid_preference_dic_tmp_keys))
    # print 'num1:', num1
    tmp1 = math.sqrt(sum([x ** 2 for x in mawid_list_dic_value]))
    tmp2 = math.sqrt(sum([x ** 2 for x in tfidf_dic_value]))
    num2 = tmp1 * tmp2  # num2=sqrt(a1^2+a2^2+a3^2) * sqrt(b1^2+b2^2+b3^2)
    # print 'num2:', num2
    cos_value = num1 / num2

    return cos_value



def get_cos_sim_dict(user_actorid_preference_dic, id_with_actorid_dict, user_liked_movie_id_list, sum_of_every_actorid_dic):

    user_actorid_preference_dic_keys = user_actorid_preference_dic.keys()

    cos_sim_dic = {}
    for k, v in id_with_actorid_dict.items():

        mawid_list = v
        intersection_list = list(set(mawid_list).intersection(set(user_actorid_preference_dic_keys)))

        if not intersection_list:
            cos_sim_dic[k] = 0
            continue

        cos_sim = get_cos_sim(user_actorid_preference_dic, id_with_actorid_dict, mawid_list, user_liked_movie_id_list, sum_of_every_actorid_dic)

        cos_sim_dic[k] = cos_sim
        #print cos_sim, intersection_list, 'dd'

    return cos_sim_dic

    # recommended_cos_value = [cos_value_sorted_tuple_list[x] for x in range(0, num_of_recommended_movies)]
    # print recommended_cos_value

    # recommended_movie_id_list = [recommended_cos_value[x][0] for x in range(0, len(recommended_cos_value))]
    # print recommended_movie_id_list
    # return recommended_movie_id_list


def recommend(user_liked_movie_id_list):
    # 为mawid推荐的前期处理
    movie_id_with_actorid_file = open(os.path.split(os.path.realpath(__file__))[0] + '/imdbid_mainactors.json')
    id_with_actorid_dic = json.loads(movie_id_with_actorid_file.readline())
    user_actorid_preference_dic = generate_user_actorid_preference_dic(user_liked_movie_id_list, id_with_actorid_dic)

    sum_of_every_actorid_dic = get_sum_of_every_actorid_dic(os.path.split(os.path.realpath(__file__))[0] + '/mainactor_imdbids.json')


    cos_sim_dict = get_cos_sim_dict(user_actorid_preference_dic, id_with_actorid_dic, user_liked_movie_id_list, sum_of_every_actorid_dic)

    return cos_sim_dict
###################################################################################################




user_liked_movie_id_list = ["tt0133093","tt0137523","tt0468569","tt0172495","tt0114369","tt1375666","tt0361862","tt0482571","tt0268978","tt0110322"]

# id_list = recommend(user_liked_movie_id_list)

# print "final recommend:", id_list





