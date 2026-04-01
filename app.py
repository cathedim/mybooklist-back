from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError
from sqlalchemy import update

from model import Session, Livro
from schemas import *
from flask_cors import CORS

from typing import List

info = Info(title="mybooklist API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

@app.get('/')
def home():
    """Redireciona para o Swagger (Documentação)
    """
    return redirect('/openapi/swagger')

@app.get("/listar_livros")
def listar_livros():
    """Lista todos os livros cadastrados
    """
    try:
        session = Session()
        lista_livros = session.query(Livro).all()
        
        return retornar_lista_livros(lista_livros), 200
    except Exception as e:
        return "Erro ao listar livros.", 400

@app.get("/buscar_livro")
def buscar_livro():
    """Busca um livro a partir do seu nome
    """
    try:
        nome = request.args.get("nome")
        session = Session()
        busca = session.query(Livro).filter(Livro.nome.ilike(f'%{nome}%')).all()
        
        return retornar_lista_livros(busca), 200
    except Exception as e:
        return "Erro ao buscar livro.", 400

@app.post("/adicionar_livro")
def adicionar_livro():
    """Adiciona novo livro, recebendo nome, autor, ano de publicação e capa
    """
    dados_requisicao = request.get_json()

    if not dados_requisicao['ano_publicacao'].isnumeric():
        return f"Erro: ano de publicação precisa ser um número!", 400
    
    if (".jpg" not in dados_requisicao["capa"]) and (".png" not in dados_requisicao["capa"]) and (".jpeg" not in dados_requisicao["capa"]):
        return f"Erro: endereço de imagem para capa precisa terminar em '.jpg', '.png' ou '.jpeg'!", 401

    livro = Livro(
        nome=dados_requisicao["nome"],
        autor=dados_requisicao["autor"],
        ano_publicacao=dados_requisicao["ano_publicacao"],
        capa=dados_requisicao["capa"])
    
    try:
        session = Session()
        session.add(livro)
        session.commit()

        return f"Livro {livro.nome} adicionado com sucesso!", 200
    except IntegrityError as ie:
        if "livro.nome" in str(ie):
            return f"O livro '{livro.nome}' já foi adicionado.", 401
        else:
            return f"Erro ao adicionar livro novo. {e}", 400
    except Exception as e:
        return f"Erro ao adicionar livro novo. {e.message}", 400
    finally:
        session.close()

@app.delete("/deletar_livro")
def deletar_livro():
    """Deleta um livro a partir do seu nome
    """
    nome = request.args.get("nome")

    try:
        session = Session()
        session.query(Livro).filter(Livro.nome == nome).delete()
        session.commit()

        return f"Livro '{nome}' deletado com sucesso!", 200
    except Exception as e:
        return f"Erro ao deletar livro. {e.message}", 400
    finally:
        session.close()