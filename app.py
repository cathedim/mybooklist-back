from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect

from sqlalchemy.exc import IntegrityError

from model import Session, Livro
from schemas import *
from flask_cors import CORS

info = Info(title="mybooklist API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

tag_doc = Tag(name="Documentação")
tag_livro = Tag(name="Livro")

@app.get('/', tags=[tag_doc])
def home():
    """Redireciona para o Swagger (Documentação)
    """
    return redirect('/openapi/swagger')

@app.get("/listar_livros", 
         tags=[tag_livro],
         responses={"200": ListaLivrosSchema, "400": ErroSchema})
def listar_livros():
    """Lista todos os livros cadastrados
    """
    try:
        session = Session()
        lista_livros = session.query(Livro).all()
        
        return retornar_lista_livros(lista_livros), 200
    except Exception as e:
        return {"mensagem": "Erro ao listar livros."}, 400

@app.get('/buscar_livro', 
         tags=[tag_livro], 
         responses={"200": ListaLivrosSchema, "400": ErroSchema})
def buscar_livro(query: LivroNomeSchema):
    """Busca um livro a partir do seu nome
    """
    try:
        nome = query.nome
        session = Session()
        busca = session.query(Livro).filter(Livro.nome.ilike(f'%{nome}%')).all()
        
        return retornar_lista_livros(busca), 200
    except Exception as e:
        return {"mensagem": "Erro ao buscar livro."}, 400

@app.post("/adicionar_livro", 
         tags=[tag_livro], 
         responses={"200": ListaLivrosSchema, "400": ErroSchema})
def adicionar_livro(form: LivroSchema):
    """Adiciona novo livro, recebendo nome, autor, ano de publicação e capa
    """    
    if not str(form.ano_publicacao).isnumeric():
        return f"Erro: ano de publicação precisa ser um número!", 400
    
    if (".jpg" not in form.capa) and (".png" not in form.capa) and (".jpeg" not in form.capa):
        return f"Erro: endereço de imagem para capa precisa terminar em '.jpg', '.png' ou '.jpeg'!", 400
    
    livro = Livro(
        nome=form.nome,
        autor=form.autor,
        ano_publicacao=form.ano_publicacao,
        capa=form.capa)

    try:
        session = Session()
        session.add(livro)
        session.commit()

        return f"Livro {livro.nome} adicionado com sucesso!", 200
    except IntegrityError as ie:
        if "livro.nome" in str(ie):
            return f"O livro '{livro.nome}' já foi adicionado.", 400
        else:
            return f"Erro ao adicionar livro novo. {e}", 400
    except Exception as e:
        return f"Erro ao adicionar livro novo. {e.message}", 400
    finally:
        session.close()

@app.delete("/deletar_livro", 
         tags=[tag_livro], 
         responses={"200": ListaLivrosSchema, "400": ErroSchema})
def deletar_livro(form: LivroNomeSchema):
    """Deleta um livro a partir do seu nome
    """
    nome = form.nome

    try:
        session = Session()
        session.query(Livro).filter(Livro.nome == nome).delete()
        session.commit()

        return f"Livro '{nome}' deletado com sucesso!", 200
    except Exception as e:
        return f"Erro ao deletar livro. {e.message}", 400
    finally:
        session.close()