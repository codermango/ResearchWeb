#!coding=utf-8
import json
import math

imdbids_in_imdbinfo = []
with open("../info/!imdbinfojson.json") as imdbinfo_file:
    for line1 in imdbinfo_file:
        movie = json.loads(line1)
        externalIds = movie["externalIds"]
        imdbid1 = externalIds["imdbId"]
        imdbids_in_imdbinfo.append(imdbid1)
        
print len(imdbids_in_imdbinfo)

imdbids_in_allmovies = []
with open("../recommender_libs/all_movies.dat") as allmovies_file:
    for line2 in allmovies_file:
        movie = json.loads(line2)
        imdbid2 = movie["imdbId"]
        imdbids_in_allmovies.append(imdbid2)

print len(imdbids_in_allmovies)

needed_ids = list(set(imdbids_in_imdbinfo).difference(set(imdbids_in_allmovies)))
print len(needed_ids)

with open("needed_ids.txt", "w") as needed_ids_file:
    for item in needed_ids:
        needed_ids_file.write(item + "\n")