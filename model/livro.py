from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base


class Livro(Base):
    __tablename__ = 'livro'

    id = Column("pk_livro", Integer, primary_key=True)
    nome = Column(String(100), unique=True)
    autor = Column(String(150))
    ano_publicacao = Column(Integer)
    capa = Column(String(300))
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, nome:str, autor:str, ano_publicacao:int, capa:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Livro
        """
        self.nome = nome
        self.autor = autor
        self.ano_publicacao = ano_publicacao
        self.capa = capa

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
