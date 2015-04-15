#!coding=utf-8
from __future__ import division
import json
import math
import os


def get_sum_of_all_mawid_in_all_movies(dic_id_with_mawid):

    mawid_list = dic_id_with_mawid.values()
    result = sum(map(lambda x: len(x), mawid_list))
    # print 'sum_of_all_mawid_in_all_movies:',result
    return result


def get_sum_of_every_mawid_dic(mawid_with_count_file):
    mawid_with_count_file = open(mawid_with_count_file)
    content = json.loads(mawid_with_count_file.readline())

    return content



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


def generate_sum_of_every_mawid_dic(dic_id_with_mawid):   # 太耗时！！！！！！！！！！
    mawid_list = []
    dic_id_with_mawid_values = dic_id_with_mawid.values()
    mawid_list = reduce(lambda x, y: x + y, dic_id_with_mawid_values)
    mawid_list = list(set(mawid_list))

    # print len(mawid_list)
    # print len(dic_id_with_mawid), 'aaa'

    mawid_with_count_dic = {}
    for mawid in mawid_list:
        num = 0
        for k, v in dic_id_with_mawid.items():
            num += v.count(mawid)
        mawid_with_count_dic[mawid] = num
        print 0

    mawid_with_count_file = open('mawid_with_count.json', 'w')
    mawid_with_count_json = json.dumps(mawid_with_count_dic)
    mawid_with_count_file.write(mawid_with_count_json + "\n")

    mawid_with_count_file.close()




def get_cos_sim(user_mawid_preference_dic, mawid_list, sum_of_all_mawid_in_all_movies, sum_of_every_mawid_dic):

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
    sum_of_user_liked_mawid = sum(user_mawid_preference_dic.values())
    # print sum_of_user_liked_mawid
    tf_dic = {}
    for k, v in user_mawid_preference_dic_tmp.items():
        tf_dic[k] = v / sum_of_user_liked_mawid

    # print 'tf_idc:', tf_dic

    idf_dic = {}
    for i, j in user_mawid_preference_dic_tmp.items():
        idf_dic[i] = sum_of_all_mawid_in_all_movies / sum_of_every_mawid_dic[i]
    # print 'idf_dic:', idf_dic

    tfidf_dic = {}
    for key in tf_dic.keys():
        tfidf_dic[key] = tf_dic[key] * idf_dic[key]
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



def get_cos_sim_dict(user_mawid_preference_dic, dic_id_with_mawid, sum_of_all_mawid_in_all_movies, sum_of_every_mawid_dic):
    # print 'user_mawid_preference_dic:', user_mawid_preference_dic
    # print 'user_mawid_preference_dic values:', user_mawid_preference_dic.values()
    # print 'length of user_mawid_preference_dic:', len(user_mawid_preference_dic)

    count = 0
    user_mawid_preference_dic_keys = user_mawid_preference_dic.keys()

    
    cos_sim_dic = {}
    for k, v in dic_id_with_mawid.items():

        count += 1
        mawid_list = v
        intersection_list = list(set(mawid_list).intersection(set(user_mawid_preference_dic_keys)))

        if not intersection_list:
            continue

        cos_sim = get_cos_sim(user_mawid_preference_dic, mawid_list, sum_of_all_mawid_in_all_movies, sum_of_every_mawid_dic)

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
    movie_id_with_mawid_file = open(os.path.split(os.path.realpath(__file__))[0] + '/movie_id_with_mawid.json')
    id_with_mawid_dic = json.loads(movie_id_with_mawid_file.readline())
    user_mawid_preference_dic = generate_user_mawid_preference_dic(user_liked_movie_id_list, id_with_mawid_dic)

     # 此值在外部算好，避免进入循环增大计算量
    sum_of_all_mawid_in_all_movies = get_sum_of_all_mawid_in_all_movies(id_with_mawid_dic)
    # generate_sum_of_every_mawid_dic(id_with_mawid_dic)  此操作很费时，提前算好存入文件mawid_with_count.json
    sum_of_every_mawid_dic = get_sum_of_every_mawid_dic(os.path.split(os.path.realpath(__file__))[0] + '/mawid_with_count.json')


    cos_sim_dict = get_cos_sim_dict(user_mawid_preference_dic, id_with_mawid_dic, sum_of_all_mawid_in_all_movies, sum_of_every_mawid_dic)

    return cos_sim_dict
###################################################################################################










