import json
import requests
import random


def filmes_assistidos_json():
    with open('../DadosJSON/filmesAssistidos.json', 'r') as json_file:
        dados = json.load(json_file)

    return dados


def preferencias_json():
    with open('../DadosJSON/preferencias.json', 'r') as json_file:
        dados = json.load(json_file)

    return dados


def filmes_generos_json():
    with open('../DadosJSON/filmesGenero.json', 'r') as json_file:
        dados = json.load(json_file)

    return dados


def links_imdb_json():
    with open('../DadosJSON/linksImdb.json', 'r') as json_file:
        dados = json.load(json_file)

    return dados


def verificados_json():
    with open('../DadosJSON/verificados.json', 'r') as json_file:
        dados = json.load(json_file)

    return dados


def recomendados_json():
    with open('../DadosJSON/recomendacao.json', 'r') as json_file:
        dados = json.load(json_file)

    return dados


def salva_verificados(imdbid):
    verificados.append(imdbid)

    with open('../DadosJSON/verificados.json', 'w') as f:
        json.dump(verificados, f)


filmesAssistidos_users = filmes_assistidos_json()
preferencias_users = preferencias_json()
filmesPorGenero = filmes_generos_json()
linksImdb = links_imdb_json()
verificados = verificados_json()


def request(imdbid, s):
    url = requests.get(f"https://api.themoviedb.org/3/find/{imdbid}?api_key=254c6407feb51fd7f478ec3e6b1abc23"
                       "&language=en-US&external_source=imdb_id")

    data = url.json()

    try:
        data = data['movie_results'][0]

    except IndexError:
        data = data['tv_results'][0]

    finally:
        return data[s]


def retorna_imdbid(movieid):
    for i in range(len(linksImdb)):
        if linksImdb[i]['movieId'] == movieid:
            return linksImdb[i]['imdbId']


def salva_recomendacoes(lista, userid, rod):
    if rod == 1:
        recomendacao_users.append([])
        recomendacao_users[userid].extend(lista)
    else:
        recomendacao_users[userid].extend(lista)

    with open('../DadosJSON/recomendacao.json', 'w') as f:
        json.dump(recomendacao_users, f)


recomendacao_users = recomendados_json()


def recomendacao(userid, rod):
    recomendados = []

    if rod == 1:
        count = 3
        genero = preferencias_users[userid]['topGeneros'][0]
    elif rod == 2:
        count = 3
        genero = preferencias_users[userid]['topGeneros'][1]
    elif rod == 3:
        count = 2
        genero = random.choice(preferencias_users[userid]['topGeneros'])
    else:
        count = 1
        genero = random.choice(preferencias_users[userid]['outros'])

    assistidos = filmesAssistidos_users[userid]['filmes']

    while count > 0:
        movieid = random.choice(filmesPorGenero[0][genero])

        imdbid = retorna_imdbid(movieid)
        pop = request(imdbid, "popularity")

        if imdbid not in verificados and pop < 30.000:
            salva_verificados(imdbid)
            continue
        elif imdbid in verificados:
            continue

        if movieid not in assistidos and movieid not in recomendados:
            if rod > 1:
                if movieid not in recomendacao_users[userid]:
                    recomendados.append(imdbid)
                    print('..')

                    count -= 1

            else:
                print('..')
                recomendados.append(imdbid)

                count -= 1

    salva_recomendacoes(recomendados, userid, rod)


def main():
    try:
        for userid in range(len(recomendacao_users), 10):
            recomendacao(userid, 1)
            print('--')
            recomendacao(userid, 2)
            print('---')
            recomendacao(userid, 3)
            print('-----')
            recomendacao(userid, 4)
            print('-------')
            recomendacao(userid, 4)
            print('||||||||||')

    except:
        print('erro')
        if len(recomendacao_users[len(recomendacao_users) - 1]) < 10:
            recomendacao_users.pop()

            with open('../DadosJSON/recomendacao.json', 'w') as f:
                json.dump(recomendacao_users, f)

    finally:
        main()


main()
