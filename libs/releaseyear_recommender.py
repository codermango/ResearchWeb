#!coding=utf-8
from __future__ import division
import json
import math



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


def get_user_preference_vector(user_liked_movie_id_list, movieid_with_releaseyear_dict):
    user_preference_vector = [0, 0, 0, 0]
    for movieid in user_liked_movie_id_list:
        releaseyear = movieid_with_releaseyear_dict[movieid]
        yearvector = generate_yearvector(releaseyear)
        user_preference_vector = [x + y for x, y in zip(user_preference_vector, yearvector)]

    print user_preference_vector
    return user_preference_vector



def generate_tfidf_vector(user_preference_vector, movieid_with_releaseyear_dict):

    movieid_with_yearvector_dict = dict()
    for k, v in movieid_with_releaseyear_dict.items():
        movieid_with_yearvector_dict[k] = generate_yearvector(v)

    print movieid_with_yearvector_dict.items()[0]

    # 喜好列表中的时间段总数
    sum_of_releaseduration_in_liked_list = sum(user_preference_vector)

    if sum_of_releaseduration_in_liked_list:
        tf_vector = map(lambda x: x / sum_of_releaseduration_in_liked_list, user_preference_vector)
        print "tf_vector:", tf_vector

        sum_of_releaseduration_in_all_movies = len(movieid_with_releaseyear_dict) #因为一个电影只有一个release year
        list_of_yearvector = movieid_with_yearvector_dict.values()

        sum_of_every_releaseduration = reduce(lambda x, y: [m + n for m, n in zip(x, y)], list_of_yearvector)
        print sum_of_every_releaseduration
        idf_vector = map(lambda x: sum_of_releaseduration_in_all_movies / x, sum_of_every_releaseduration)
        print "idf_vector:", idf_vector

        tfidf_vector = [x * y for x, y in zip(tf_vector, idf_vector)]
        print 'tfidf_vector:', tfidf_vector
    else:
        tfidf_vector = user_preference_vector

    return tfidf_vector



def recommend(user_liked_movie_id_list):

    movieid_with_releaseyear_file = open("movieid_with_releaseyear.json")
    movieid_with_releaseyear_dict = json.loads(movieid_with_releaseyear_file.readline())
    print len(movieid_with_releaseyear_dict)

    user_preference_vector = get_user_preference_vector(user_liked_movie_id_list, movieid_with_releaseyear_dict)

    tfidf_vector = generate_tfidf_vector(user_preference_vector, movieid_with_releaseyear_dict)



user_liked_movie_id_list = ["tt0348124","tt0401398","tt0486761","tt0181196","tt0389074","tt0279967","tt0969647","tt0097757","tt0103639"]
recommend(user_liked_movie_id_list)