#!coding=utf-8
from __future__ import division
import json
import math
import os

with open("../info/!imdbgenre.txt") as imdbgenre_file:
    imdbgenre_dict = {}
    for line1 in imdbgenre_file:
        imdbid = line1[0: 9]
        genres = line1[9: ].strip()
        genre_list = genres.split(" ")
        imdbgenre_dict[imdbid] = genre_list


with open("../recommender_libs/all_movies.dat") as all_movies_file, open("../recommender_libs/all_movies_tmp.dat", "w") as all_movies_tmp_file:
    count = 0
    for line2 in all_movies_file:
        movie = json.loads(line2)
        imdbid2 = movie["imdbId"]
        try:
            movie["genres"] = imdbgenre_dict[imdbid2]
        except KeyError:
            continue
        movie_json = json.dumps(movie)
 
        all_movies_tmp_file.write(movie_json + "\n")
    






