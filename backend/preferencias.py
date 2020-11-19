import json
import pandas as pd
import operator


def generos_json():
    with open('../DadosJSON/generos.json', 'r') as json_file:
        dados = json.load(json_file)

    return dados


filmes = pd.read_csv('../Arquivos/movies.csv', index_col=['movieId'])
filmes['genres'] = filmes['genres'].str.split('|')
notas = pd.read_csv('../Arquivos/ratings.csv')
generos = generos_json()
generos_stats = {}


def generos_estatisticas():
    for genero in generos:
        generos_stats[genero] = 0


filmesAssistidos = []


def filmes_assistidos(userid):
    filmesuser = {'filmes': []}
    for movieid in notas['movieId'][notas['userId'] == userid]:
        filmesuser['filmes'].append(int(movieid))
        for j in range(len(filmes['genres'][movieid])):
            generos_stats[f'{filmes["genres"][movieid][j]}'] += 1

    filmesAssistidos.append(filmesuser)


preferencias = []


def top_generos(n):
    aux = sorted(generos_stats.items(), key=operator.itemgetter(1), reverse=True)

    aux2 = {'topGeneros': [], 'outros': [], 'stats': []}
    for i in range(n):
        aux2['topGeneros'].append(aux[i][0])

    for i in range(n, len(generos_stats) - 1):
        aux2['outros'].append(aux[i][0])

    for i in generos_stats.values():
        aux2['stats'].append(i)

    preferencias.append(aux2)


def salva_json():
    with open('../DadosJSON/filmesAssistidos.json', 'w') as f:
        json.dump(filmesAssistidos, f)

    with open('../DadosJSON/preferencias.json', 'w') as f:
        json.dump(preferencias, f)


def salva_dados():
    for i in range(10):
        generos_estatisticas()
        filmes_assistidos(i + 1)
        top_generos(5)

    salva_json()


salva_dados()


