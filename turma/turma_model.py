from config import db

class Turma(db.Model):
    __tablename__ = "turmas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    # Relacionamento com a classe Aluno
    alunos = db.relationship("Aluno", back_populates="turma")


    def __init__(self, nome, desc, ativo):
      self.nome = nome
      self.desc = desc
      self.ativo = ativo

class TurmaNaoEncontrado(Exception):
  pass

  def to_dict(self):
    return {'id': self.id, 'nome': self.nome, 'desc': self.desc, "ativo": self.ativo}
  
  def turma_por_id(turma_id):
    turma = turma.query.get(turma_id)

    if not turma:
      raise AlunoNaoEncontrado
    return Turma.to_dict()

  def listar_turmas():
    turmas = Aluno.query.all()
    return [turma.to_dict() for turma in turmas]