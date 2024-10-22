from turma.turma_model import Turma
from datetime import datetime
from config import db

class Aluno(db.Model):
  __tablename__ = "alunos"
   
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(100), nullable=False)
  idade = db.Column(db.Integer, nullable=False)
  data_nasc = db.Column(db.Date, nullable=False)
  nota_primeiro_semestre = db.Column(db.Float, nullable=False)
  nota_segundo_semestre = db.Column(db.Float, nullable=False)
  media_final = db.Column(db.Float, nullable=False)
  
  turma_id = db.Column(db.Integer, db.ForeignKey("turmas.id"), nullable=False)

  turma = db.relationship("Turma", back_populates="alunos")

  def __init__(self, nome, idade, data_nasc, nota_primeiro_semestre, nota_segundo_semestre, media_final, turma_id):
    self.nome = nome
    self.idade = idade
    self.data_nasc = data_nasc
    self.nota_primeiro_semestre = nota_primeiro_semestre
    self.nota_segundo_semestre = nota_segundo_semestre
    self.media_final = media_final
    self.turma_id = turma_id

  def to_dict(self):  
    return {'id': self.id, 'nome': self.nome, "idade": self.idade, 'data_nasc': self.data_nasc.isoformat(), "nota_primeiro_semestre": self.nota_primeiro_semestre, "nota_segundo_semestre": self.nota_segundo_semestre, "media_final": self.media_final, "turma": self.turma_id}

class AlunoNaoEncontrado(Exception):
  pass

def aluno_por_id(id_aluno):
  aluno = Aluno.query.get(id_aluno)

  if not aluno:
    raise AlunoNaoEncontrado
  return aluno.to_dict()

def listar_alunos():
  alunos = Aluno.query.all()
  return [aluno.to_dict() for aluno in alunos]

def adicionar_aluno(aluno_data):
  novo_aluno = Aluno(
    nome=aluno_data['nome'], 
    idade=aluno_data['idade'], 
    turma_id=aluno_data['turma_id'], 
    data_nasc= datetime.strptime(aluno_data["data_nasc"], '%d/%m/%Y').date(), 
    nota_primeiro_semestre=aluno_data['nota_primeiro_semestre'], 
    nota_segundo_semestre=aluno_data['nota_segundo_semestre'], 
    media_final=aluno_data['media_final'])

  db.session.add(novo_aluno)
  db.session.commit()

def atualizar_aluno(id_aluno, novos_dados):
  aluno = Aluno.query.get(id_aluno)
  if not aluno:
    raise AlunoNaoEncontrado
  aluno.nome = novos_dados['nome']
  db.session.commit()

def excluir_aluno(id_aluno):
  aluno = Aluno.query.get(id_aluno)
  if not aluno:
    raise AlunoNaoEncontrado
  db.session.delete(aluno)
  db.session.commit()