#!coding=utf-8
from __future__ import division
import json
import math

####################################################################################################


     
def get_sum_of_all_genre_in_all_movies(dic_id_with_genre):
    num_of_genre = 0
    values = dic_id_with_genre.values()
    num_list = map(lambda x: x.count(1), values)
    num_of_genre = sum(num_list)
    return num_of_genre



def generate_tfidf_vector(user_preference_vector, dic_id_with_genre):
    list_of_all_movie_genre = dic_id_with_genre.values()
    sum_of_every_genre_vector = reduce(lambda x, y: [m + n for m, n in zip(x, y)], list_of_all_movie_genre)
    print sum_of_every_genre_vector

    sum_of_user_preference_vector = sum(user_preference_vector) # 也是sum_of_all_genre_in_liked_movies

    tf_vector = map(lambda x: x / sum_of_user_preference_vector, user_preference_vector)
    print 'tf_vector:', tf_vector

    sum_of_all_genre_in_all_movies = get_sum_of_all_genre_in_all_movies(dic_id_with_genre)
    idf_vector = map(lambda x: sum_of_all_genre_in_all_movies / x, sum_of_every_genre_vector)
    print 'idf_vector：', idf_vector

    tfidf_vector = [x * y for x, y in zip(tf_vector, idf_vector)]
    print 'tfidf_vector:', tfidf_vector

    return tfidf_vector


def get_cos_values_dict(dic_id_with_genre, tfidf_vector):

    cos_values_dict = dict()
    for k, v in dic_id_with_genre.items():
        # 计算余弦值
        num1 = sum([x * y for x, y in zip(v, tfidf_vector)])  # num1=a1*b1+a2*b2+a3*b3
        tmp1 = math.sqrt(sum([x ** 2 for x in v]))
        tmp2 = math.sqrt(sum([x ** 2 for x in tfidf_vector]))
        num2 = tmp1 * tmp2  # num2=sqrt(a1^2+a2^2+a3^2) * sqrt(b1^2+b2^2+b3^2)

        cos_value = num1 / num2
        cos_values_dict[k] = cos_value
        
    return cos_values_dict


def get_recommended_movie_id(num_of_recommended_movies, cos_values_dict):
    cos_value_sorted_tuple_list = sorted(cos_values_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    recommended_cos_value = [cos_value_sorted_tuple_list[x] for x in range(0, num_of_recommended_movies)]
    print recommended_cos_value

    recommended_movie_id_list = [recommended_cos_value[x][0] for x in range(0, len(recommended_cos_value))]
    #print recommended_movie_id_list
    return recommended_movie_id_list

def recommend(user_preference_vector, dic_id_with_genre):
    tfidf_vector = generate_tfidf_vector(user_preference_vector, dic_id_with_genre)
    
    cos_values_dict = get_cos_values_dict(dic_id_with_genre, tfidf_vector)

    return cos_values_dict

    # recommended_movie_id_list = get_recommended_movie_id(num_of_recommended_movies, cos_values_dict)
    # print recommended_movie_id_list

    # recommended_movie_id_list_file = open('recommended_movie_list.txt', 'w')
    # map(lambda x: recommended_movie_id_list_file.write(x+'\n'), recommended_movie_id_list)


#####################################################################################################


