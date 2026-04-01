from pydantic import BaseModel
from typing import Optional, List
from model.livro import Livro


class LivroSchema(BaseModel):
    """ Atributos referentes ao livro
    """
    nome: str
    autor: str
    ano_publicacao: int
    capa: str


class LivroBuscaSchema(BaseModel):
    """ Estrutura da busca
    """
    nome: str


class ListaLivrosSchema(BaseModel):
    """ Formato de lista de livros
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


class LivroViewSchema(BaseModel):
    """ Retorno do livro
    """
    id: int
    nome: str
    autor: str
    ano_publicacao: int
    capa: str
    total_livros: int


class LivroDeleteSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def retornar_livro(livro: Livro):
    """ Retorna uma representação do produto seguindo o schema definido em
        LivroViewSchema.
    """
    return {
        "id": livro.id,
        "nome": livro.nome,
        "autor": livro.autor,
        "ano_publicacao": livro.ano_publicacao,
        "capa": livro.capa,
        "total_livros": len(livro)
    }