from pydantic import BaseModel, Field
from typing import Optional, List
from model.alunos import Alunos
from datetime import datetime


class AlunosSchema(BaseModel):
    """ Define como um novo aluno será representado
    """
    cpf: int = Field(default=12345678900)
    nome: str = Field(default="Neil Peart")
    telefone: Optional[str] = Field(default="79 999999999")



class AlunosBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no cpf do aluno.
    """
    cpf: int = Field(default=12345678900)



class ListagemAlunosSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    alunos:List[AlunosSchema]


class AlunosViewSchema(BaseModel):
    """ Define como um aluno será retornado
    """
    matricula: int = Field(default=000000)
    cpf: int = Field(default=12345678900)
    nome: str = Field(default="Jhonatta Tavares")
    telefone: Optional[str] = Field(default="79 999998888")
    validade: datetime = Field(default=datetime.now())



class AlunosDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str
    cpf: int


class AlunosContrataPlanoSchema(BaseModel):
    """ Define a estrutura a ser informada para a contratacao de plano mensal
    """
    cpf: int = Field(default=12345678900)
    qtd_meses: int = Field(default=3)



def apresenta_alunos(alunos: List[Alunos]):
    """ Retorna uma representação do aluno seguindo o schema definido em
        AlunosViewSchema.
    """
    result = []
    for aluno in alunos:
        result.append({
            "matricula": aluno.matricula,
            "cpf": aluno.cpf,
            "nome": aluno.nome,
            "telefone": aluno.telefone,
            "validade": aluno.validade
        })

    return {"alunos": result}




def apresenta_aluno(aluno: Alunos):
    """ Retorna uma representação do aluno seguindo o schema definido em
        AlunosViewSchema.
    """
    return {
            "matricula": aluno.matricula,
            "cpf": aluno.cpf,
            "nome": aluno.nome,
            "telefone": aluno.telefone,
            "validade": aluno.validade
        }


