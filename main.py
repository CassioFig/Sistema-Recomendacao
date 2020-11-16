import pandas as pd
import random
import operator

links = pd.read_csv('arquivos/links.csv', index_col=['movieId'])
filmes = pd.read_csv('arquivos/movies.csv', index_col=['movieId'])
notas = pd.read_csv('arquivos/ratings.csv')
tags = pd.read_csv('arquivos/tags.csv', index_col=['movieId'])

filmes['genres'] = filmes['genres'].str.split('|')

generos = {}
generos_p = {}
filmesId = filmes.index.values
filmesAssistidos = []
topGeneros = []
generosA = []
recomendados = []


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
        if n > 3:
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


def main():
    lista_generos()
    filmes_assistidos(1)
    top_generos(5)
    recomenda(10)
    print(recomendados)
    print(len(recomendados))


main()
