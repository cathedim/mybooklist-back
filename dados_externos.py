import requests

from schemas import *

open_library = 'https://openlibrary.org'
headers = {
    "User-Agent": "mybooklist/1.0 (twcoacc@gmail.com)"
}

def busca_livros(nome):
    url = open_library + '/search.json?title=' + nome.replace(' ', '+')
    response = requests.get(url, headers=headers).json()
    
    return response

def busca_autor(autor):
    url = open_library + '/search.json?author=' + autor.replace(' ', '+')
    response = requests.get(url, headers=headers).json()

    return response

def busca_geral(autor):
    url = open_library + '/search.json?q=' + autor.replace(' ', '+')
    response = requests.get(url, headers=headers).json()

    return response

def busca_especifica(ol_id):
    url = open_library + '/works/' + ol_id + '.json'
    response = requests.get(url, headers=headers).json()

    return response