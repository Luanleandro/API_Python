from config import db
from professor.professor_model import Professor
class Turma(db.Model):
    __tablename__ = "turmas"

    id = db.Column(db.Integer, primary_key=True)
    materia = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(100))
    ativo = db.Column(db.Boolean(), nullable=False)

    alunos = db.relationship("Aluno", back_populates="turma", lazy=True)
    professor_id = db.Column(db.Integer, db.ForeignKey("professor.id"), nullable=False)

    def __init__(self, materia, descricao, ativo, professor_id):
      self.materia = materia
      self.descricao = descricao
      self.ativo = ativo
      self.professor_id = professor_id

    def to_dict(self):
      return {
        'id': self.id, 
        'materia': self.materia, 
        'descricao': self.descricao,
        "ativo": self.ativo, 
        'professor_id': self.professor_id 
      }
class TurmaNaoEncontrado(Exception):
  pass

def turma_por_id(turma_id):
  turma = Turma.query.get(turma_id)
  if not turma:
    raise TurmaNaoEncontrado(f'Turma com ID {turma_id} não encontrada.')
  return turma.to_dict()

def listar_turmas():
  turmas = Turma.query.all()
  return [turma.to_dict() for turma in turmas]

def adicionar_turma(turma_data):
  nova_turma = Turma(
    materia=turma_data['materia'],
    descricao=turma_data['descricao'],
    ativo=turma_data['ativo'],
    professor_id=turma_data['professor_id']
  )

  db.session.add(nova_turma)
  db.session.commit()

def atualizar_turma(turma_id, novos_dados):
  turma = Turma.query.get(turma_id)

  if not turma:
    raise TurmaNaoEncontrado(f'Turma com ID {turma_id} não encontrada.')
    
  turma.materia = novos_dados['materia']
  turma.descricao = novos_dados['descricao']
  turma.ativo = novos_dados['ativo']
  turma.professor_id = novos_dados['professor_id']
    
  db.session.commit()

def excluir_turma(turma_id):
  turma = Turma.query.get(turma_id)
  if not turma:
    raise TurmaNaoEncontrado(f'Turma com ID {turma_id} não encontrada.')
  db.session.delete(turma)
  db.session.commit()