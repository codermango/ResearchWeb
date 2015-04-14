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

    print result
    return result


def get_user_preference_vector(user_liked_movie_id_list, movieid_with_releaseyear_dict):
    user_preference_vector = [0, 0, 0, 0]
    for movieid in user_liked_movie_id_list:
        releaseyear = movieid_with_releaseyear_dict[movieid]
        yearvector = generate_yearvector(releaseyear)
        user_preference_vector = [x + y for x, y in zip(user_preference_vector, yearvector)]

    print user_preference_vector
    return user_preference_vector



def recommend(user_liked_movie_id_list):

    movieid_with_releaseyear_file = open("movieid_with_releaseyear.json")
    movieid_with_releaseyear_dict = json.loads(movieid_with_releaseyear_file.readline())

    user_preference_vector = get_user_preference_vector(user_liked_movie_id_list, movieid_with_releaseyear_dict)

    # tfidf_vector = generate_tfidf_vector(user_preference_vector, dic_id_with_genre)
    
    # print "tfidf_vector： ", tfidf_vector

    # cos_values_dict = get_cos_values_dict(dic_id_with_genre, tfidf_vector)

    # # print len(cos_values_dict)

    # return cos_values_dict







user_liked_movie_id_list = ["tt0348124","tt0401398","tt0486761","tt0181196","tt0389074","tt0279967","tt0969647","tt0097757","tt0103639"]
recommend(user_liked_movie_id_list)