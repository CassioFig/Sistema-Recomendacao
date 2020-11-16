from builtins import super

import pandas as pd

links = pd.read_csv('arquivos/links.csv', index_col=['movieId'])
filmes = pd.read_csv('arquivos/movies.csv', index_col=['movieId'])
notas = pd.read_csv('arquivos/ratings.csv')
tags = pd.read_csv('arquivos/tags.csv', index_col=['movieId'])

filmes['genres'] = filmes['genres'].str.split('|')

generos = {}


def lista_generos():
    for generosLista in filmes['genres']:
        for genero in range(len(generosLista)):
            if generosLista[genero] not in generos:
                generos[f'{generosLista[genero]}'] = 0


def generos_assistidos(user):
    for i in notas['movieId'][notas['userId'] == user]:
        for j in range(len(filmes['genres'][i])):
            generos[f'{filmes["genres"][i][j]}'] += 1


def main():
    lista_generos()
    generos_assistidos(1)
    print(generos)


main()