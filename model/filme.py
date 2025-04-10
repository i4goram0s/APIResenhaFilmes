from sqlalchemy import Column, String, DateTime, Integer
from datetime import datetime
from typing import Union

from  model import Base


class Filme(Base):
    __tablename__ = 'filme'

    id = Column(String(20), primary_key=True)
    resenha = Column(String(10000))

    def __init__(self, id:str, resenha:str):
        """
        Cadastra um filme

        Arguments:
            resenha: Resenha do filme a ser informada pelo usuário do sistema
        """
        self.id = id
        self.resenha = resenha


