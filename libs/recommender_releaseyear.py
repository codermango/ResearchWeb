#!coding=utf-8
from __future__ import division
import json
import math
import os


def generate_yearvector(releaseyear):
    result = []
    if releaseyear < 1990:
        result = [1, 0, 0, 0]
    elif releaseyear >= 1990 and releaseyear < 2000:
        result = [0, 1, 0, 0]
    elif releaseyear >= 2000 and releaseyear < 2010:
        result = [0, 0, 1, 0]
    elif releaseyear >= 2010 and releaseyear < 2020:
        result = [0, 0, 0, 1]

    return result


def get_user_preference_vector(user_liked_movie_id_list, movieid_with_yearvector_dict):
    user_preference_vector = [0, 0, 0, 0]
    for movieid in user_liked_movie_id_list:
        try:
            yearvector = movieid_with_yearvector_dict[movieid]
            user_preference_vector = [x + y for x, y in zip(user_preference_vector, yearvector)]
        except KeyError:
            continue
    print user_preference_vector, "--"
    return user_preference_vector



def generate_tfidf_vector(user_liked_movie_id_list, movieid_with_yearvector_dict):

    user_preference_vector = get_user_preference_vector(user_liked_movie_id_list, movieid_with_yearvector_dict)

    
    sum_of_user_liked_movies = len(user_liked_movie_id_list)
    sum_of_all_movies = len(movieid_with_yearvector_dict)

    if sum(user_preference_vector):
        tf_vector = map(lambda x: x / sum_of_user_liked_movies, user_preference_vector)
        print "tf_vector:", tf_vector

        list_of_yearvector = movieid_with_yearvector_dict.values()

        sum_of_every_releaseduration = reduce(lambda x, y: [m + n for m, n in zip(x, y)], list_of_yearvector)
        print sum_of_every_releaseduration

        idf_vector = map(lambda x: sum_of_all_movies / x, sum_of_every_releaseduration)
        print "idf_vector:", idf_vector

        tfidf_vector = [x * y for x, y in zip(tf_vector, idf_vector)]
        print 'tfidf_vector:', tfidf_vector
    else:
        tfidf_vector = user_preference_vector

    return tfidf_vector


def get_cos_values_dict(movieid_with_yearvector_dict, tfidf_vector):
    cos_values_dict = dict()
    for k, v in movieid_with_yearvector_dict.items():
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
        
    return cos_values_dict



def recommend(user_liked_movie_id_list):

    movieid_with_releaseyear_file = open(os.path.split(os.path.realpath(__file__))[0] + "/movieid_with_releaseyear.json")
    movieid_with_releaseyear_dict = json.loads(movieid_with_releaseyear_file.readline())
    print len(movieid_with_releaseyear_dict)

    movieid_with_yearvector_dict = dict()
    for k, v in movieid_with_releaseyear_dict.items():
        movieid_with_yearvector_dict[k] = generate_yearvector(v)

    print movieid_with_yearvector_dict.items()[0]

    

    tfidf_vector = generate_tfidf_vector(user_liked_movie_id_list, movieid_with_yearvector_dict)

    cos_values_dict = get_cos_values_dict(movieid_with_yearvector_dict, tfidf_vector)
    
    return cos_values_dict




user_liked_movie_id_list = ["tt0348124","tt0401398","tt0486761","tt0181196","tt0389074","tt0279967","tt0969647","tt0097757","tt0103639"]
recommend(user_liked_movie_id_list)