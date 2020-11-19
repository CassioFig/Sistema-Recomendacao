import pandas as pd
import requests
import json


def links_json():
    with open('../DadosJSON/linksImdb.json', 'r') as json_file:
        dados = json.load(json_file)

    return dados


filmes = pd.read_csv('../Arquivos/movies.csv', index_col=['movieId'])
links = links_json()


def request(imdbid, s):
    url = requests.get(f"https://api.themoviedb.org/3/find/{imdbid}?api_key=254c6407feb51fd7f478ec3e6b1abc23"
                       "&language=en-US&external_source=imdb_id")

    data = url.json()
    data = data['movie_results'][0]

    return data[s]


i = 0
j = 0
for link in links:
    nota = request(link['imdbId'], "vote_average")

    if nota >= 6.5:
        print('-------------')
        print('i: ', i)
        print('-------------')
        i += 1
    else:
        print('j: ', j)
        j += 1

    if i == 100:
        break




