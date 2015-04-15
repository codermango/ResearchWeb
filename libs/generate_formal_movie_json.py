#!coding=utf-8
import json
import math
from collections import Counter
import os

'''This file is used to generate the following format movie json file
    {
        "imdbId": "ttxxxxxx",
        "genres": [xxx, xxx, ...],
        "mawid": [xxx, xxx, ...],
        "releaseYear": 2014,
        "directors": [xxx, xxx],
        "imdbRating": 0
    }
'''


tagdb_after_neaten_genres_file = open("tagdb_after_neaten_genres.json")

movieid_with_mawid_file = open("movie_id_with_mawid.json")
movieid_with_mawid_dict = json.loads(movieid_with_mawid_file.readline())

movieid_with_releaseyear_file = open("movieid_with_releaseyear.json")
movieid_with_releaseyear_dict = json.loads(movieid_with_releaseyear_file.readline())

all_movies_file = open("all_movies.dat", "w")

for line in tagdb_after_neaten_genres_file:
    movie = json.loads(line)
    genres = movie["genres"]
    ids = movie["ids"]
    imdbid = ids["imdbId"]

    new_movie_format = dict()
    new_movie_format["imdbId"] = imdbid
    new_movie_format["genres"] = genres
    new_movie_format["mawid"] = movieid_with_mawid_dict[imdbid]
    new_movie_format["releaseYear"] = int(movieid_with_releaseyear_dict[imdbid])
    new_movie_format["directors"] = []
    new_movie_format["imdbRating"] = 0

    new_movie_format_json = json.dumps(new_movie_format)
    all_movies_file.write(new_movie_format_json + "\n")

all_movies_file.close()
tagdb_after_neaten_genres_file.close()


