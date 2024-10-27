from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .turma_model import TurmaNaoEncontrado, listar_turmas, turma_por_id, adicionar_turma, atualizar_turma, excluir_turma
from professor.professor_model import listar_professores, Professor
from config import db

turmas_blueprint = Blueprint('turmas', __name__)

@turmas_blueprint.route('/', methods=['GET'])
def get_index():
    return render_template("index.html")

@turmas_blueprint.route('/turmas', methods=['GET'])
def get_turmas():
    turmas = listar_turmas()
    return render_template('turmas.html', turmas=turmas)

@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['GET'])
def get_turma(id_turma):
    try:
        turma = turma_por_id(id_turma)
        professor = Professor.query.get(turma['professor_id'])
        return render_template('turma_id.html', turma=turma, professor=professor)
    except TurmaNaoEncontrado:
        return jsonify({'message': 'Turma não encontrada'}), 404

@turmas_blueprint.route('/turmas/adicionar', methods=['GET'])
def adicionar_turma_page():
    professores = listar_professores()
    return render_template('criarTurma.html', professores=professores)

@turmas_blueprint.route('/turmas', methods=['POST'])
def create_turma():
    materia = request.form['materia']
    descricao = request.form['descricao']
    professor_id = int(request.form['professor_id'])
    ativo = request.form.get('ativo') == 'true'
    nova_turma = {'materia': materia, 'descricao': descricao, 'professor_id': professor_id, "ativo": ativo}

    adicionar_turma(nova_turma)
    return redirect(url_for('turmas.get_turmas'))

@turmas_blueprint.route('/turmas/<int:id_turma>/editar', methods=['GET'])
def editar_turma_page(id_turma):
    try:
        turma = turma_por_id(id_turma)
        professores = listar_professores()
        return render_template('turma_update.html', turma=turma, professores=professores)
    except TurmaNaoEncontrado:
        return jsonify({'message': 'Turma não encontrada'}), 404

@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['PUT', 'POST'])
def update_turma(id_turma):
    try:
        turma = turma_por_id(id_turma)
        if not turma:
            return jsonify({'message': 'Aluno não encontrado'}), 404

        turma['materia'] = request.form['materia']
        turma['descricao'] = request.form['descricao']
        turma['professor_id'] = int(request.form['professor_id'])

        atualizar_turma(id_turma, turma)

        return redirect(url_for('turmas.get_turma', id_turma=id_turma))
    except TurmaNaoEncontrado:
        return jsonify({'message': 'Turma não encontrada'}), 404

@turmas_blueprint.route('/turmas/delete/<int:id_turma>', methods=['DELETE', 'POST'])
def delete_turma(id_turma):
    try:
        print(id_turma)
        excluir_turma(id_turma)
        return redirect(url_for('turmas.get_turmas'))
    except TurmaNaoEncontrado:
        return jsonify({'message': 'Turma não encontrada'}), 404