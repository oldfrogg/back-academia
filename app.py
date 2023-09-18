# ARQUIVO CONTROLADOR. BASE DA APLICACAO

from flask_openapi3 import OpenAPI, Info, Tag
from flask import Flask, redirect, request, make_response, jsonify
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Alunos
from schemas import *
from flask_cors import CORS

from datetime import datetime, timedelta


info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)



# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
aluno_tag = Tag(name="Aluno", description="Adição, visualização e remoção de alunos à base")



@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/add_aluno', tags=[aluno_tag], responses={"200": AlunosViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_aluno(form: AlunosSchema):
    """Adiciona um novo Aluno à base de dados.

    Retorna a lista de alunos
    """
    aluno = Alunos(
        cpf=form.cpf,
        nome=form.nome,
        telefone=form.telefone
    )

    try:
        # Conecta-se com o BD
        session = Session()
        # Adiciona o aluno à lista
        session.add(aluno)
        # Commita
        session.commit()
        
        return apresenta_aluno(aluno), 200

    except IntegrityError as e:
        # como a duplicidade do cpf é a provável razão do IntegrityError
        error_msg = "CPF já cadsatrado"
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        return {"mesage": error_msg}, 400


@app.get('/get_alunos', tags=[aluno_tag],
         responses={"200": ListagemAlunosSchema, "404": ErrorSchema})
def get_alunos():
    """Faz a busca por todos os Alunos cadastrados

    Retorna uma representação da listagem de alunos.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    alunos = session.query(Alunos).all()
    # SELECT * FROM Alunos 


    if not alunos:
        # se não há alunos cadastrados
        return {"alunos": []}, 200
    else:
        # retorna a representação de aluno
        return apresenta_alunos(alunos), 200


@app.get('/get_aluno', tags=[aluno_tag], responses={"200": AlunosViewSchema, "404": ErrorSchema})
def get_aluno(query:AlunosBuscaSchema):
    """Procura um aluno a partir do seu CPF

    Retorna o aluno buscado.
    """
    aluno_cpf = query.cpf

    session = Session()
    aluno = session.query(Alunos).filter(Alunos.cpf == aluno_cpf).first()
    # SELECT * FROM Alunos WHERE cpf_digitado == cpf__aluno__d-base passando um resultado
    # Caso ao invés do first() fosse um all(), teria uma lista de resultados
    # Se eu quiser ver a query:
    # print (session.query(Alunos).filter(Aluno.cpf == aluno_cpf)

    # Se não achar nenhum
    if not aluno:
        # Se não encontrou o aluno buscado
        error_msg = "Não há aluno cadastrado com o CPF informado."
        return {"message": error_msg}, 404

    else:
        # Retornando resposta
        return apresenta_aluno(aluno), 200


@app.delete('/del_aluno', tags=[aluno_tag], responses={"200": AlunosDelSchema, "404": ErrorSchema})
def del_aluno (query: AlunosBuscaSchema):
    """Deleta um Aluno a partir do CPF informado.

    Retorna a confirmação da remoção
    """ 
    aluno_cpf = query.cpf
    session = Session()
    aluno = session.query(Alunos).filter(Alunos.cpf == aluno_cpf).first()
    count = session.query(Alunos).filter(Alunos.cpf == aluno_cpf).delete()
    session.commit()

    if count:
        return {"message": "Aluno removido da base", "nome": aluno.nome, "cpf": aluno_cpf}


    else: 
        # Para aluno não encontrado:
        error_msg = "Aluno não encontrado na base :/"
        return {"mesage": error_msg}, 404


@app.put('/update_aluno', tags=[aluno_tag], responses={"200": AlunosViewSchema, "404": ErrorSchema})
def update_aluno(query:AlunosSchema):
    """Altera os dados cadastrais de um aluno a partir do CPF.

    Retorna o aluno com os dados modificados.
    """
    aluno_cpf = query.cpf
    session = Session()
    aluno = session.query(Alunos).filter(Alunos.cpf==aluno_cpf).first()

    if not aluno:
        error_msg = "Aluno não encontrado"
        return {"message": error_msg}, 404

    else:
        aluno.cpf = query.cpf
        aluno.nome = query.nome
        aluno.telefone = query.telefone
        session.commit()
        return apresenta_aluno(aluno), 200


@app.put('/contrata_plano', tags=[aluno_tag], responses={"200":AlunosViewSchema, "404": ErrorSchema})
def contrata_plano(query:AlunosContrataPlanoSchema):
    """Adiciona a quantidade de meses contratado no plano do aluno.

    Retorna os dados do aluno com a validade do seu plano atualizada.
    """
    aluno_cpf = query.cpf
    qnt_meses = query.qtd_meses
    session = Session()
    aluno = session.query(Alunos).filter(Alunos.cpf==aluno_cpf).first()
    
    if not aluno:
        error_msg = "Aluno não encontrado"
        return {"message": error_msg}, 404

    else:
        if aluno.validade < datetime.now():
            aluno.validade = datetime.now()+timedelta(days=30*query.qtd_meses)
            session.commit()
        else:
            aluno.validade += timedelta(days=30*query.qtd_meses)
            session.commit()
        return apresenta_aluno(aluno), 200

