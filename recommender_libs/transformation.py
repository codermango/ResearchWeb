#!coding=utf-8
import json
import math
from collections import Counter
import os




def exchange_key_value_of_dict(input_dict):
    '''此函数作用:
        把{"a": [1, 2, 3], "b": [1, 3, 5]}转化成{1: ["a", "b"], 2: ["a"], 3: ["a", "b"], 5: ["b"]}
    '''
    union_of_input_dict_values = []
    input_dict_values = input_dict.values()

    for k, v in input_dict.items():
        union_of_input_dict_values += v

    union_of_input_dict_values = set(union_of_input_dict_values)
    print len(union_of_input_dict_values)

    output_dict = {}
    for item in union_of_input_dict_values:
        output_value = []
        for k1, v1 in input_dict.items():
            if item in v1:
                output_value.append(k1)
        output_dict[item] = output_value
        print len(output_dict)

    return output_dict


def generate_imdbid_directors(imdbid_directors_dict):
    imdbid_directors_json = json.dumps(imdbid_directors_dict)
    with open("imdbid_directors.json", "w") as imdbid_directors_file:
         imdbid_directors_file.write(imdbid_directors_json)


def generate_imdbid_mainactors(imdbid_mainactors_dict):
    imdbid_mainactors_json = json.dumps(imdbid_mainactors_dict)
    with open("imdbid_mainactors.json", "w") as imdbid_mainactors_file:
        imdbid_mainactors_file.write(imdbid_mainactors_json)


def genreate_imdbid_ratings(imdbid_ratings_dict):
    imdbid_ratings_json = json.dumps(imdbid_ratings_dict)
    with open("imdbid_ratings.json", "w") as imdbid_ratings_file:
        imdbid_ratings_file.write(imdbid_ratings_json)


def genreate_imdbid_releaseyear(imdbid_releaseyear_dict):
    imdbid_releaseyear_json = json.dumps(imdbid_releaseyear_dict)
    with open("imdbid_releaseyear.json", "w") as imdbid_releaseyear_file:
        imdbid_releaseyear_file.write(imdbid_releaseyear_json)


def generate_director_imdbids(imdbid_directors_dict):
    director_imdbids_dict = exchange_key_value_of_dict(imdbid_directors_dict)
    director_imdbids_json = json.dumps(director_imdbids_dict)
    with open("director_imdbids.json", "w") as director_imdbids_file:
        director_imdbids_file.write(director_imdbids_json)


def generate_mainactor_imdbids(imdbid_mainactors_dict):
    mainactor_imdbids_dict = exchange_key_value_of_dict(imdbid_mainactors_dict)
    mainactor_imdbids_json = json.dumps(mainactor_imdbids_dict)
    with open("mainactor_imdbids.json", "w") as mainactor_imdbids_file:
        mainactor_imdbids_file.write(mainactor_imdbids_json)


def generate_imdbid_genrevector(imdbid_genres_dict):
    all_genre_list = []
    for imdbid in imdbid_genres_dict:
        all_genre_list += imdbid_genres_dict[imdbid]

    sorted_all_genre_list = sorted(list(set(all_genre_list)))
    num_of_genre = len(sorted_all_genre_list)

    genre_index_dict = {}
    for i in range(0, num_of_genre):
        genre_index_dict[sorted_all_genre_list[i]] = i

    # print genre_index_dict

    imdbid_genrevector_dict = {}
    for k, v in imdbid_genres_dict.items():
        # print k
        genrevector = [0] * num_of_genre
        for item in v:
            index = genre_index_dict[item]
            genrevector[index] = 1

        imdbid_genrevector_dict[k] = genrevector

    imdbid_genrevector_json = json.dumps(imdbid_genrevector_dict)
    with open("imdbid_genrevector.json", "w") as imdbid_genrevector_file:
        imdbid_genrevector_file.write(imdbid_genrevector_json + "\n")


def generate_imdbid_language(imdbid_language_dict):
    imdbid_language_json = json.dumps(imdbid_language_dict)
    with open("imdbid_language.json", "w") as imdbid_language_file:
        imdbid_language_file.write(imdbid_language_json)


def transform(all_movies_file_path):

    imdbid_directors_dict = {}
    imdbid_mainactors_dict = {}
    imdbid_ratings_dict = {}
    imdbid_releaseyear_dict = {}
    imdbid_genres_dict = {}
    imdbid_language_dict = {}

    with open(all_movies_file_path) as all_movies_file:
        for line in all_movies_file:
            movie = json.loads(line)
            imdbid = movie["imdbId"]
            mainactors = movie["imdbMainactors"]
            ratings = movie["imdbRating"]
            directors = movie["imdbDirectors"]
            releaseyear = movie["releaseYear"]
            genres = movie["genres"]
            language = movie["language"]

            imdbid_directors_dict[imdbid] = directors
            imdbid_mainactors_dict[imdbid] = mainactors
            imdbid_ratings_dict[imdbid] = ratings
            imdbid_releaseyear_dict[imdbid] = releaseyear
            imdbid_genres_dict[imdbid] = genres
            imdbid_language_dict[imdbid] = language

    # generate_imdbid_directors(imdbid_directors_dict)
    # generate_imdbid_mainactors(imdbid_mainactors_dict)
    # genreate_imdbid_ratings(imdbid_ratings_dict)
    # genreate_imdbid_releaseyear(imdbid_releaseyear_dict)

    # # 生成director_imdbids.json和mainactor_imdbids.json
    # generate_director_imdbids(imdbid_directors_dict)
    # generate_mainactor_imdbids(imdbid_mainactors_dict)

    # # 生成imdbid_genrevector
    # generate_imdbid_genrevector(imdbid_genres_dict)

    # 生成imdbid_language
    generate_imdbid_language(imdbid_language_dict)


###############################################################################################




transform("all_movies.dat")


