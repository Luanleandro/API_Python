from config import db

class Professor(db.Model):
    __tablename__ = 'professor'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    materia = db.Column(db.String(100), nullable=False)
    observacoes = db.Column(db.Text)

    turmas = db.relationship('Turma', backref='professor', lazy=True)

    def __init__(self, nome, idade, materia, observacoes=None):
        self.nome = nome
        self.idade = idade
        self.materia = materia
        self.observacoes = observacoes

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'materia': self.materia,
            'observacoes': self.observacoes,
            'turmas': self.turmas
        }
class ProfessorNaoEncontrado(Exception):
    pass
    
def professor_por_id(professor_id):
    professor = Professor.query.get(professor_id)
    if not professor:
        raise ProfessorNaoEncontrado(f'Professor com ID {professor_id} não encontrado.')
    return professor.to_dict()


def listar_professores():
    professores = Professor.query.all()
    return [professor.to_dict() for professor in professores]

def adicionar_professor(professor_data):
    novo_professor = Professor(
        nome=professor_data['nome'],
        idade=professor_data['idade'],
        materia=professor_data['materia'],
        observacoes=professor_data.get('observacoes')
    )
    db.session.add(novo_professor)
    db.session.commit()

def atualizar_professor(professor_id, novos_dados):
    professor = Professor.query.get(professor_id)
    if not professor:
        raise ProfessorNaoEncontrado(f'Professor com ID {professor_id} não encontrado.')

    professor.nome = novos_dados['nome']
    professor.idade = novos_dados['idade']
    professor.materia = novos_dados['materia']
    professor.observacoes = novos_dados.get('observacoes')
    
    db.session.commit()


def excluir_professor(professor_id):
    professor = Professor.query.get(professor_id)
    if not professor:
        raise ProfessorNaoEncontrado(f'Professor com ID {professor_id} não encontrado.')

    db.session.delete(professor)
    db.session.commit()
