import os
from config import app,db
from alunos.alunos_routes import alunos_blueprint
from turma.turma_routes import turmas_blueprint
from professor.professor_routes import professores_blueprint

app.register_blueprint(alunos_blueprint, url_prefix='/')
app.register_blueprint(turmas_blueprint, url_prefix='/')
app.register_blueprint(professores_blueprint, url_prefix='/')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
  app.run(host=app.config["HOST"], port = app.config['PORT'],debug=app.config['DEBUG'] )