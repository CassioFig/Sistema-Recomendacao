import pandas as pd
import random
import operator
import json

filmes = pd.read_csv('arquivos/movies.csv', index_col=['movieId'])
notas = pd.read_csv('arquivos/ratings.csv')

filmes['genres'] = filmes['genres'].str.split('|')

generos = {}
generos_p = {}
filmesId = filmes.index.values
filmesAssistidos = []
topGeneros = []
generosA = []
recomendados = []

dados = []

def lista_generos():
    for generosLista in filmes['genres']:
        for genero in range(len(generosLista)):
            if generosLista[genero] not in generos:
                generos[f'{generosLista[genero]}'] = 0


def filmes_assistidos(user):
    for i in notas['movieId'][notas['userId'] == user]:
        filmesAssistidos.append(i)
        for j in range(len(filmes['genres'][i])):
            generos[f'{filmes["genres"][i][j]}'] += 1

    calcula_porcentagem()


def calcula_porcentagem():
    for i in generos.keys():
        generos_p[i] = round((generos[i] * 100) / sum(generos.values()), 2)


def top_generos(n):
    aux = sorted(generos_p.items(), key=operator.itemgetter(1), reverse=True)

    for i in range(n):
        topGeneros.append(aux[i][0])

    for i in range(n, len(generos_p) - 1):
        generosA.append(aux[i][0])


def recomenda(n):
    while n > 0:
        if n > 30:
            i = random.choice(filmesId)
            for j in filmes['genres'][i]:
                if j in topGeneros and i not in filmesAssistidos and i not in recomendados:
                    recomendados.append(i)
                    n -= 1
        else:
            i = random.choice(filmesId)
            for j in filmes['genres'][i]:
                if j in generosA and i not in filmesAssistidos and i not in recomendados:
                    recomendados.append(i)
                    n -= 1


def inserir_dados(userid):
    filmes_assistidos(userid)
    top_generos(5)
    recomenda(100)

    recomendados_str = str(recomendados).strip('[]')
    dados_user = {'userId': userid, 'filmes': recomendados_str}

    dados.append(dados_user)


def limpar_listas():
    recomendados.clear()
    topGeneros.clear()
    generosA.clear()
    filmesAssistidos.clear()

    for i in generos.keys():
        generos[i] = 0


def escreve_json():
    with open('dados.json', 'w') as f:
        json.dump(dados, f)


def main():
    lista_generos()

    for i in range(610):
        limpar_listas()
        inserir_dados(i + 1)

    escreve_json()
        

main()
