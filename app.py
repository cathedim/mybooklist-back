from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect

from sqlalchemy.exc import IntegrityError
from sqlalchemy import update

from model import Session, Livro
from schemas import *
from flask_cors import CORS

from dados_externos import busca_livros, busca_autor, busca_geral, busca_especifica

info = Info(title="mybooklist API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

tag_doc = Tag(name="Documentação")
tag_livro = Tag(name="Livro")
tag_api = Tag(name="API")

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

@app.put("/atualizar_livro", 
         tags=[tag_livro], 
         responses={"200": ListaLivrosSchema, "400": ErroSchema})
def atualizar_livro(form: LivroAtualizacaoSchema):
    """Atualiza um livro a partir do seu nome
    """
    nome_antigo = form.nome_antigo
    nome_novo = form.nome_novo
    autor_novo = form.autor_novo
    capa_nova = form.capa_nova
    ano_publicacao_novo = form.ano_publicacao_novo

    try:
        session = Session()

        if autor_novo is not None:
            session.execute(update(Livro).where(Livro.nome == nome_antigo).values(autor=autor_novo))

        if capa_nova is not None:
            session.execute(update(Livro).where(Livro.nome == nome_antigo).values(capa=capa_nova))

        if ano_publicacao_novo is not None:
            session.execute(update(Livro).where(Livro.nome == nome_antigo).values(ano_publicacao=ano_publicacao_novo))
        
        if nome_novo is not None:
            session.execute(update(Livro).where(Livro.nome == nome_antigo).values(nome=nome_novo))
        
        session.commit()

        return f"Livro '{nome_antigo}' atualizado com sucesso!", 200
    except Exception as e:
        return f"Erro ao atualizar livro. {e}", 400

@app.get("/buscar_nome", 
         tags=[tag_api],
         responses={"200": ListaLivrosSchema, "400": ErroSchema})
def buscar_nome(query: LivroBuscaSchema):
    """Busca livro na API através do título
    """
    try:
        busca = query.busca

        return busca_livros(busca), 200
    except Exception as e:
        return {"mensagem": {e}}, 400

@app.get("/buscar_autor", 
         tags=[tag_api],
         responses={"200": ListaLivrosSchema, "400": ErroSchema})
def buscar_autor(query: LivroBuscaSchema):
    """Busca livro na API através do autor
    """
    try:
        busca = query.busca
        
        return busca_autor(busca), 200
    except Exception as e:
        return {"mensagem": {e}}, 400

@app.get("/buscar_geral", 
         tags=[tag_api],
         responses={"200": ListaLivrosSchema, "400": ErroSchema})
def buscar_geral(query: LivroBuscaSchema):
    """Busca livro na API através do nome e autor
    """
    try:
        busca = query.busca
        
        return busca_geral(busca), 200
    except Exception as e:
        return {"mensagem": {e}}, 400

@app.get("/buscar_especifica", 
         tags=[tag_api],
         responses={"200": ListaLivrosSchema, "400": ErroSchema})
def buscar_especifica(query: LivroBuscaSchema):
    """Busca informações sobre livro na API através do seu ID
    """
    try:
        busca = query.busca
        
        return busca_especifica(busca), 200
    except Exception as e:
        return {"mensagem": {e}}, 400