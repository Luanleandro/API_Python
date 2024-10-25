from turma.turma_model import Turma
from datetime import datetime
from config import db

class Aluno(db.Model):
  __tablename__ = "alunos"
   
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(100), nullable=False)
  idade = db.Column(db.Integer, nullable=False)
  data_nascimento = db.Column(db.Date, nullable=False)
  nota_primeiro_semestre = db.Column(db.Float, nullable=False)
  nota_segundo_semestre = db.Column(db.Float, nullable=False)
  media_final = db.Column(db.Float, nullable=False)
  
  turma_id = db.Column(db.Integer, db.ForeignKey("turmas.id"), nullable=False)

  turma = db.relationship("Turma", back_populates="alunos")

  def __init__(self, nome, idade, data_nascimento, nota_primeiro_semestre, nota_segundo_semestre, turma_id, media_final):
    self.nome = nome
    self.idade = idade
    self.data_nascimento = data_nascimento
    self.nota_primeiro_semestre = nota_primeiro_semestre
    self.nota_segundo_semestre = nota_segundo_semestre
    self.turma_id = turma_id
    self.media_final = media_final

  def to_dict(self):  
    return {'id': self.id, 'nome': self.nome, "idade": self.idade, 'data_nascimento': self.data_nascimento.isoformat(), "nota_primeiro_semestre": self.nota_primeiro_semestre, "nota_segundo_semestre": self.nota_segundo_semestre, "turma_id": self.turma_id, "media_final": self.media_final}

class AlunoNaoEncontrado(Exception):
  pass

def aluno_por_id(id_aluno):
  aluno = Aluno.query.get(id_aluno)

  if not aluno:
    raise  AlunoNaoEncontrado(f'Aluno com ID {aluno_id} não encontrado.')
  return aluno.to_dict()

def listar_alunos():
  alunos = Aluno.query.all()
  return [aluno.to_dict() for aluno in alunos]

def adicionar_aluno(novos_dados):
  novo_aluno = Aluno(
    nome=novos_dados['nome'], 
    idade=novos_dados['idade'], 
    data_nascimento= datetime.strptime(novos_dados["data_nascimento"], '%d/%m/%Y').date(), 
    nota_primeiro_semestre=novos_dados['nota_primeiro_semestre'], 
    nota_segundo_semestre=novos_dados['nota_segundo_semestre'], 
    turma_id=novos_dados['turma_id'], 
    media_final=novos_dados['media_final'],
  )

  db.session.add(novo_aluno)
  db.session.commit()

def atualizar_aluno(id_aluno, novos_dados):
  aluno = Aluno.query.get(id_aluno)
  if not aluno:
    raise AlunoNaoEncontrado

  aluno.nome = novos_dados['nome']
  aluno.idade = novos_dados['idade']
  aluno.data_nascimento = novos_dados['data_nascimento']
  aluno.nota_primeiro_semestre = novos_dados['nota_primeiro_semestre']
  aluno.nota_segundo_semestre = novos_dados['nota_segundo_semestre']
  aluno.media_final = (aluno.nota_primeiro_semestre + aluno.nota_segundo_semestre) / 2
  aluno.turma_id = novos_dados['turma_id']
  
  db.session.commit()

def excluir_aluno(id_aluno):
  aluno = Aluno.query.get(id_aluno)
  if not aluno:
    raise AlunoNaoEncontrado(f'Aluno com ID {aluno_id} não encontrado.')

  db.session.delete(aluno)
  db.session.commit()