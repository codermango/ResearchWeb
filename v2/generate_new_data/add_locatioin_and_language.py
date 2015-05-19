#!coding=utf-8
from __future__ import division
import json
import math
import os


imdbid_languageandcountry_dict = {}
with open("../info/!imdblocationandlanguage.json") as imdblocationandlanguage_file:
    for line in imdblocationandlanguage_file:
        movie = json.loads(line)
        # print movie
        imdbid = movie["imdbid"]
        try:
            language = movie["Language"]
        except KeyError:
            language = []
        try:
            country = movie["Country"]
        except KeyError:
            country = []
        language_country_dict = {}
        language_country_dict["language"] = language
        language_country_dict["country"] = country

        imdbid_languageandcountry_dict[imdbid] = language_country_dict
        # print imdbid_languageandcountry_dict

print len(imdbid_languageandcountry_dict)


with open("../recommender_libs/all_movies.dat") as all_movies_file, open("../recommender_libs/all_movies_tmp.dat", "w") as all_movies_tmp_file:
    for line2 in all_movies_file:
        movie2 = json.loads(line2)
        imdbid2 = movie2["imdbId"]
        # print movie2
        language_country_dict2 = imdbid_languageandcountry_dict[imdbid2]
        language2 = language_country_dict2["language"]
        country2 = language_country_dict2["country"]

        movie2["language"] = language2
        movie2["country"] = country2
        # print movie2
        movie2_json = json.dumps(movie2)
        all_movies_tmp_file.write(movie2_json + "\n")
