#!coding=utf-8
import json
import math
from collections import Counter
import os

'''This file is used to generate the following format movie json file
    {
        "imdbId": "ttxxxxxx",
        "genres": [xxx, xxx, ...],
        "imdbMainactors": [xxx, xxx, ...],
        "releaseYear": 2014,
        "imdbDirectors": [xxx, xxx],
        "imdbRating": 0
    }
'''


tagdb_after_neaten_genres_file = open("tagdb_after_neaten_genres.json")

movieid_with_mawid_file = open("movie_id_with_mawid.json")
movieid_with_mawid_dict = json.loads(movieid_with_mawid_file.readline())

imdbmainactors_file = open("imdbmainactors.json")
imdbmainactors_dict = json.loads(imdbmainactors_file.readline())

movieid_with_releaseyear_file = open("movieid_with_releaseyear.json")
movieid_with_releaseyear_dict = json.loads(movieid_with_releaseyear_file.readline())

imdbrating_file = open("imdbrating.json")
imdbrating_dict = json.loads(imdbrating_file.readline())

imdbdirectors_file = open("imdbdirectors.json")
imdbdirectors_dict = json.loads(imdbdirectors_file.readline())


all_movies_file = open("all_movies.dat", "w")

count = 0
for line in tagdb_after_neaten_genres_file:
    movie = json.loads(line)
    genres = movie["genres"]
    ids = movie["ids"]
    imdbid = ids["imdbId"]

    new_movie_format = dict()
    new_movie_format["imdbId"] = imdbid
    new_movie_format["genres"] = genres
    new_movie_format["releaseYear"] = int(movieid_with_releaseyear_dict[imdbid])
    
    
    try:
        new_movie_format["imdbRating"] = imdbrating_dict[imdbid]
        new_movie_format["imdbDirectors"] = imdbdirectors_dict[imdbid]
        new_movie_format["imdbMainactors"] = imdbmainactors_dict[imdbid]
    except KeyError:
        print imdbid
        continue

    new_movie_format_json = json.dumps(new_movie_format)
    all_movies_file.write(new_movie_format_json + "\n")

print count

all_movies_file.close()
tagdb_after_neaten_genres_file.close()
movieid_with_mawid_file.close()
movieid_with_releaseyear_file.close()
imdbrating_file.close()
imdbdirectors_file.close()
imdbmainactors_file.close()