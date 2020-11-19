import pandas as pd
import json

links = pd.read_csv('../Arquivos/links.csv', index_col=['movieId'])

links_imdb = []


def salva_links():

    for movieId in links.index.values:
        filme = {'movieId': int(movieId), 'imdbId': ''}

        imdbid = links['imdbId'][movieId]
        if len(str(imdbid)) == 7:
            filme['imdbId'] = f'tt{imdbid}'
        elif len(str(imdbid)) == 6:
            filme['imdbId'] = f'tt0{imdbid}'
        elif len(str(imdbid)) == 5:
            filme['imdbId'] = f'tt00{imdbid}'

        links_imdb.append(filme)


def salva_json():
    salva_links()

    with open('../DadosJSON/linksImdb.json', 'w') as f:
        json.dump(links_imdb, f)


# salva_json()

