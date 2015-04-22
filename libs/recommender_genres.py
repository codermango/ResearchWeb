#!coding=utf-8
from __future__ import division
import json
import math
import os

####################################################################################################

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

    print 'user_preference_vector: ', user_preference_vector

    return user_preference_vector


     
def get_sum_of_all_genre_in_all_movies(dic_id_with_genre):
    num_of_genre = 0
    values = dic_id_with_genre.values()
    num_list = map(lambda x: x.count(1), values)
    num_of_genre = sum(num_list)
    return num_of_genre



def generate_tfidf_vector(user_liked_movie_ids, dic_id_with_genre):
    list_of_all_movie_genre = dic_id_with_genre.values()
    sum_of_every_genre_vector = reduce(lambda x, y: [m + n for m, n in zip(x, y)], list_of_all_movie_genre)
    # print sum_of_every_genre_vector

    sum_of_user_liked_movies = len(user_liked_movie_ids) 
    sum_of_all_movies = len(dic_id_with_genre)

    user_preference_vector = generate_user_genre_preference_vector(user_liked_movie_ids, dic_id_with_genre)

    if sum(user_preference_vector):
        tf_vector = map(lambda x: x / sum_of_user_liked_movies, user_preference_vector)
        print 'tf_vector:', tf_vector

        idf_vector = map(lambda x: sum_of_all_movies / x, sum_of_every_genre_vector)
        print 'idf_vector：', idf_vector

        tfidf_vector = [(x * y) ** 2 for x, y in zip(tf_vector, idf_vector)]
        print 'tfidf_vector:', tfidf_vector

    else:
        tfidf_vector = user_preference_vector

    return tfidf_vector



def get_recommended_movie_id(num_of_recommended_movies, cos_values_dict):
    cos_value_sorted_tuple_list = sorted(cos_values_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    recommended_cos_value = [cos_value_sorted_tuple_list[x] for x in range(0, num_of_recommended_movies)]
    # print recommended_cos_value

    recommended_movie_id_list = [recommended_cos_value[x][0] for x in range(0, len(recommended_cos_value))]
    #print recommended_movie_id_list
    return recommended_movie_id_list

def get_cos_values_dict(user_liked_movie_ids, dic_id_with_genre):
    tfidf_vector = generate_tfidf_vector(user_liked_movie_ids, dic_id_with_genre)
    
    print "tfidf_vector： ", tfidf_vector

    cos_values_dict = dict()
    for k, v in dic_id_with_genre.items():
        # 计算余弦值
        num1 = sum([x * y for x, y in zip(v, tfidf_vector)])  # num1=a1*b1+a2*b2+a3*b3
        tmp1 = math.sqrt(sum([x ** 2 for x in v]))
        tmp2 = math.sqrt(sum([x ** 2 for x in tfidf_vector]))
        num2 = tmp1 * tmp2  # num2=sqrt(a1^2+a2^2+a3^2) * sqrt(b1^2+b2^2+b3^2)

        if num2:
            cos_value = num1 / num2
        else:
            cos_value = 0
        cos_values_dict[k] = cos_value
    # print len(cos_values_dict)
    return cos_values_dict

    # recommended_movie_id_list = get_recommended_movie_id(num_of_recommended_movies, cos_values_dict)
    # print recommended_movie_id_list

    # recommended_movie_id_list_file = open('recommended_movie_list.txt', 'w')
    # map(lambda x: recommended_movie_id_list_file.write(x+'\n'), recommended_movie_id_list)


def recommend(user_liked_movie_ids):
    # 为genre推荐的前期处理
    movie_genre_vector_file = open(os.path.split(os.path.realpath(__file__))[0] + "/movie_genre_vector.json")
    id_with_genre_dic = json.loads(movie_genre_vector_file.readline())
    

    cos_values_dict = get_cos_values_dict(user_liked_movie_ids, id_with_genre_dic)

    return cos_values_dict

#####################################################################################################


