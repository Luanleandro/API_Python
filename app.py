import os
from config import app,db
from alunos.alunos_routes import alunos_blueprint

# from professor.index import professor
app.register_blueprint(alunos_blueprint, url_prefix='/')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
  app.run(host=app.config["HOST"], port = app.config['PORT'],debug=app.config['DEBUG'] )