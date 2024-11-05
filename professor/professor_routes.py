from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .professor_model import ProfessorNaoEncontrado, listar_professores, professor_por_id, adicionar_professor, atualizar_professor, excluir_professor

from config import db

professores_blueprint = Blueprint('professores', __name__)

@professores_blueprint.route('/', methods=['GET'])
def get_index():
    return render_template("index.html")

@professores_blueprint.route('/professores', methods=['GET'])
def get_professores():
    professores = listar_professores()
    return render_template('professores.html', professores=professores)

@professores_blueprint.route('/professores/<int:id_professor>', methods=['GET'])
def get_professor(id_professor):
    try:
        professor = professor_por_id(id_professor)
        return render_template('professor_id.html', professor=professor)
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404

@professores_blueprint.route('/professores/adicionar', methods=['GET'])
def adicionar_professor_page():
    return render_template('criarProfessor.html')

@professores_blueprint.route('/professores', methods=['POST'])
def create_professor():
    nome = request.form['nome']
    idade = request.form['idade']
    materia = request.form['materia']
    observacoes = request.form['observacoes']
    novo_professor = {'nome': nome, 'idade': int(idade), 'materia': materia, 'observacoes': observacoes}
    adicionar_professor(novo_professor)
    return redirect(url_for('professores.get_professores'))

@professores_blueprint.route('/professores/<int:id_professor>/editar', methods=['GET'])
def editar_professor_page(id_professor):
    try:
        professor = professor_por_id(id_professor)
        return render_template('professor_update.html', professor=professor)
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404

@professores_blueprint.route('/professores/<int:id_professor>', methods=['PUT', 'POST'])
def update_professor(id_professor):
    try:
        professor = professor_por_id(id_professor)
        if not professor:
            return jsonify({'message': 'Aluno não encontrado'}), 404

        professor['nome'] = request.form['nome']
        professor['idade'] = int(request.form['idade'])
        professor['materia'] = request.form['materia']

        atualizar_professor(id_professor, professor)
        
        return redirect(url_for('professores.get_professor', id_professor=id_professor))
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404

@professores_blueprint.route('/professores/delete/<int:id_professor>', methods=['DELETE', 'POST'])
def delete_professor(id_professor):
    try:
        excluir_professor(id_professor)
        return redirect(url_for('professores.get_professores'))
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404
