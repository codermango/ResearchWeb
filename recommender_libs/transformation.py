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



def transform(all_movies_file_path):

    imdbid_directors_dict = {}
    imdbid_mainactors_dict = {}
    imdbid_ratings_dict = {}
    imdbid_releaseyear_dict = {}

    with open(all_movies_file_path) as all_movies_file:
        for line in all_movies_file:
            movie = json.loads(line)
            imdbid = movie["imdbId"]
            mainactors = movie["imdbMainactors"]
            ratings = movie["imdbRating"]
            directors = movie["imdbDirectors"]
            releaseyear = movie["releaseYear"]

            imdbid_directors_dict[imdbid] = directors
            imdbid_mainactors_dict[imdbid] = mainactors
            imdbid_ratings_dict[imdbid] = ratings
            imdbid_releaseyear_dict[imdbid] = releaseyear

    imdbid_directors_json = json.dumps(imdbid_directors_dict)
    imdbid_mainactors_json = json.dumps(imdbid_mainactors_dict)
    imdbid_ratings_json = json.dumps(imdbid_ratings_dict)
    imdbid_releaseyear_json = json.dumps(imdbid_releaseyear_dict)
    
    with open("imdbid_directors.json", "w") as imdbid_directors_file, \
            open("imdbid_mainactors.json", "w") as imdbid_mainactors_file, \
            open("imdbid_ratings.json", "w") as imdbid_ratings_file, \
            open("imdbid_releaseyear.json", "w") as imdbid_releaseyear_file:
        imdbid_directors_file.write(imdbid_directors_json)
        imdbid_mainactors_file.write(imdbid_mainactors_json)
        imdbid_ratings_file.write(imdbid_ratings_json)
        imdbid_releaseyear_file.write(imdbid_releaseyear_json)


    # 生成director_imdbids.json和mainactor_imdbids.json
    director_imdbids_dict = exchange_key_value_of_dict(imdbid_directors_dict)
    mainactor_imdbids_dict = exchange_key_value_of_dict(imdbid_mainactors_dict)
    director_imdbids_json = json.dumps(director_imdbids_dict)
    mainactor_imdbids_json = json.dumps(mainactor_imdbids_dict)
    with open("director_imdbids.json", "w") as director_imdbids_file, open("mainactor_imdbids.json", "w") as mainactor_imdbids_file:
        director_imdbids_file.write(director_imdbids_json)
        mainactor_imdbids_file.write(mainactor_imdbids_json)



###############################################################################################

transform("all_movies.dat")


