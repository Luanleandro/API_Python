from flask import Blueprint, request, jsonify,render_template,redirect, url_for
from datetime import datetime
from .alunos_model import AlunoNaoEncontrado, listar_alunos, aluno_por_id, adicionar_aluno, atualizar_aluno, excluir_aluno
from turma.turma_model import Turma, listar_turmas
from config import db

alunos_blueprint = Blueprint('alunos', __name__)

@alunos_blueprint.route('/', methods=['GET'])
def get_index():
    return render_template("index.html")

@alunos_blueprint.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = listar_alunos()
    return render_template("alunos.html", alunos=alunos)

@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        turma = Turma.query.get(aluno['turma_id'])
        return render_template('aluno_id.html', aluno=aluno, turma=turma)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

@alunos_blueprint.route('/alunos/adicionar', methods=['GET'])
def adicionar_aluno_page():
    turmas = listar_turmas()
    return render_template('criarAlunos.html', turmas=turmas)

@alunos_blueprint.route('/alunos', methods=['POST'])
def create_aluno():
    nome = request.form['nome']
    data_nascimento_str = request.form['data_nascimento'] 
    nota_primeiro_semestre = float(request.form['nota_primeiro_semestre'])
    nota_segundo_semestre = float(request.form['nota_segundo_semestre'])
    turma_id = int(request.form['turma_id'])
    data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()

    media_final = (nota_primeiro_semestre + nota_segundo_semestre) / 2

    novo_aluno = {
        'nome': nome,
        'data_nascimento': data_nascimento,
        'nota_primeiro_semestre': nota_primeiro_semestre,
        'nota_segundo_semestre': nota_segundo_semestre,
        'media_final': media_final,
        'turma_id': turma_id,
    }

    adicionar_aluno(novo_aluno)
    return redirect(url_for('alunos.get_alunos'))

@alunos_blueprint.route('/alunos/<int:id_aluno>/editar', methods=['GET'])
def editar_aluno_page(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        turmas = listar_turmas()
        return render_template('aluno_update.html', aluno=aluno, turmas=turmas)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['PUT',"POST"])
def update_aluno(id_aluno):
        try:
            aluno = aluno_por_id(id_aluno)
            if not aluno:
                return jsonify({'message': 'Aluno não encontrado'}), 404

            nome = request.form['nome']
            data_nascimento_str = request.form['data_nascimento'] 
            nota_primeiro_semestre = float(request.form['nota_primeiro_semestre'])
            nota_segundo_semestre = float(request.form['nota_segundo_semestre'])
            turma_id = int(request.form['turma_id'])
            data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()

            aluno['nome'] = nome
            aluno['data_nascimento'] = data_nascimento
            aluno['nota_primeiro_semestre'] = nota_primeiro_semestre
            aluno['nota_segundo_semestre'] = nota_segundo_semestre
            aluno['turma_id'] = turma_id

            atualizar_aluno(id_aluno, aluno)
            
            return redirect(url_for('alunos.get_aluno', id_aluno=id_aluno))
        except AlunoNaoEncontrado:
            return jsonify({'message': 'Aluno não encontrado'}), 404
   
@alunos_blueprint.route('/alunos/delete/<int:id_aluno>', methods=['DELETE','POST'])
def delete_aluno(id_aluno):
        try:
            excluir_aluno(id_aluno)
            return redirect(url_for('alunos.get_alunos'))
        except AlunoNaoEncontrado:
            return jsonify({'message': 'Aluno não encontrado'}), 404