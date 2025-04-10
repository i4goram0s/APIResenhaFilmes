from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Filme
from schemas import *
from flask_cors import CORS

info = Info(title="ResenhaIMDB API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Lista das rotas básicas para inserção. listagem e exclusão de resenhas de filmes avaliados pelo IMDB")
filme_tag = Tag(name="Filme", description="Adição, visualização e remoção de resenhas da base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')
    

@app.post('/filme', tags=[filme_tag],
          responses={"200": FilmeViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_filme(form: FilmeSchema):
    """Adiciona um novo filme à base de dados

    Retorna as informações do filme adicionado! 
    """
    filme = Filme(
        id=form.id,
        resenha=form.resenha)
    try:
        # criando conexão com a base
        session = Session()
        # adicionando filme
        session.add(filme)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        return apresenta_filme(filme), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Filme já cadastrado"
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Ocorreu um erro inesperado no cadastro filme\n" + str(e)
        return {"mesage": error_msg}, 400   

@app.put('/filme', tags=[filme_tag],
          responses={"200": FilmeViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def atualiza_filme(form: FilmeSchema, query: FilmeBuscaSchema):
    """Adiciona um novo filme à base de dados

    Retorna as informações do filme adicionado! 
    """
    filme = Filme(
        id=form.id,
        resenha=form.resenha)
    filme_id = filme.id
    print(filme_id)
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Filme).filter(Filme.id == filme_id).update({'resenha':form.resenha})
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Filme Atualizado", "id": filme_id, "resenha": filme.resenha}
    else:
        # se o filme não foi encontrado
        error_msg = "Filme não encontrado"
        return {"mesage": error_msg}, 404 

@app.get('/filmes', tags=[filme_tag],
         responses={"200": ListagemFilmesSchema, "404": ErrorSchema})
def get_filmes():
    """Faz a busca por todos os Filmes cadastrados

    Retorna uma  listagem de filmes já cadastrados na base.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    filmes = session.query(Filme).all()

    if not filmes:
        # se não há filmes cadastrados
        return {"filmes": []}, 200
    else:
        # retorna a representação de filme
        print(filmes)
        return apresenta_filmes(filmes), 200


@app.get('/filme', tags=[filme_tag],
         responses={"200": FilmeViewSchema, "404": ErrorSchema})
def get_filme(query: FilmeBuscaSchema):
    """Faz a busca por um filme a partir do id(nome) do filme

    Retorna um filme com base no id.
    """
    filme_id = query.id
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    filme = session.query(Filme).filter(Filme.id == filme_id).first()

    if not filme:
        # se o filme não foi encontrado
        error_msg = "Filme não encontrado"
        return {"mesage": error_msg}, 404
    else:
        # retorna a representação de filme
        return apresenta_filme(filme), 200


@app.delete('/filme', tags=[filme_tag],
            responses={"200": FilmeDelSchema, "404": ErrorSchema})
def del_filme(query: FilmeBuscaSchema):
    """Deleta um Filme a partir do nome de filme informado

    Retorna uma mensagem de confirmação da remoção.
    """
    filme_id = unquote(unquote(query.id))
    print(filme_id)
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Filme).filter(Filme.id == filme_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Filme removido", "id": filme_id}
    else:
        # se o filme não foi encontrado
        error_msg = "Filme não encontrado"
        return {"mesage": error_msg}, 404

