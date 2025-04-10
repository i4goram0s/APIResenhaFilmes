from pydantic import BaseModel
from typing import Optional, List
from model.filme import Filme


class FilmeSchema(BaseModel):
    """ Define como um novo filme a ser inserido deve ser representado
    """
    id: str = "tt0080684"
    resenha: str = "lorem ipsum dolor sit amet..."


class FilmeBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no código do filme a partir do IMDB.
    """
    id: str = "tt0080684"


class ListagemFilmesSchema(BaseModel):
    """ Definição da listagem de filmes.
    """
    filmes:List[FilmeSchema]


def apresenta_filmes(filmes: List[Filme]):
    """ Retorna uma representação do filme seguindo o schema definido em
        filmeViewSchema.
    """
    result = []
    for filme in filmes:
        result.append({
            "id": filme.id,
            "resenha": filme.resenha
        })

    return {"filmes": result}


class FilmeViewSchema(BaseModel):
    """ Definição de retorno de uma única resenha de filme
    """
    id: str = "tt0080684"
    resenha: str = "lorem ipsum"


class FilmeDelSchema(BaseModel):
    """ Definição do retorno após a exclusão de uma resenha de filme
    """
    mesage: str
    id: str

def apresenta_filme(filme: Filme):
    """ Retorno dos dados do filme
    """
    return {
        "id": filme.id,
        "resenha": filme.resenha
    }
