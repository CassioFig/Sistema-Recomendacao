import pandas as pd
import json

filmes = pd.read_csv('../Arquivos/movies.csv', index_col=['movieId'])
filmes['genres'] = filmes['genres'].str.split('|')


generos_lista = []
filmes_generos = []


def lista_generos():
    aux = []
    for generos in filmes['genres']:
        aux.extend(generos)

    generos_lista.extend(sorted(list(set(aux))))

    aux = {}
    for genero in generos_lista:
        aux[genero] = []

    filmes_generos.append(aux)


def filmes_por_genero():
    for movieId in filmes.index.values:
        for genero in filmes['genres'][movieId]:
            filmes_generos[0][genero].append(int(movieId))


def salva_json():
    lista_generos()
    filmes_por_genero()

    with open('../DadosJSON/filmesGenero.json', 'w') as f:
        json.dump(filmes_generos, f)

    with open('../DadosJSON/generos.json', 'w') as f:
        json.dump(generos_lista, f)


# salva_json()

