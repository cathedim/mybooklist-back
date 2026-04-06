from pydantic import BaseModel
from typing import Optional, List
from model.livro import Livro


class LivroSchema(BaseModel):
    """ Atributos do objeto Livro
    """
    nome: str
    autor: str
    ano_publicacao: int
    capa: str


class LivroNomeSchema(BaseModel):
    """ Nome do livro para deletar e buscar
    """
    nome: str


class ListaLivrosSchema(BaseModel):
    """ Lista de livros
    """
    livros:List[LivroSchema]


def retornar_lista_livros(livros: List[Livro]):
    """ Retorna uma lista de livros
    """
    result = []
    for livro in livros:
        result.append({
            "nome": livro.nome,
            "autor": livro.autor,
            "ano_publicacao": livro.ano_publicacao,
            "capa": livro.capa,
        })

    return {"livros": result}