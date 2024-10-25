from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .turmas_model import (
    TurmaNaoEncontrado, listar_turmas, turma_por_id,
    adicionar_turma, atualizar_turma, excluir_turma
)
from config import db

turmas_blueprint = Blueprint('turmas', __name__)

@turmas_blueprint.route('/', methods=['GET'])
def get_index():
    return "Index de Turmas"

## LISTAR TODAS AS TURMAS
@turmas_blueprint.route('/turmas', methods=['GET'])
def get_turmas():
    turmas = listar_turmas()
    return render_template('turmas.html', turmas=turmas)

## OBTÉM UMA TURMA PELO ID
@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['GET'])
def get_turma(id_turma):
    try:
        turma = turma_por_id(id_turma)
        return render_template('turma_id.html', turma=turma)
    except TurmaNaoEncontrado:
        return jsonify({'message': 'Turma não encontrada'}), 404

## FORMULÁRIO PARA CRIAR NOVA TURMA
@turmas_blueprint.route('/turmas/adicionar', methods=['GET'])
def adicionar_turma_page():
    return render_template('criarTurma.html')

## CRIA UMA NOVA TURMA
@turmas_blueprint.route('/turmas', methods=['POST'])
def create_turma():
    descricao = request.form['descricao']
    professor_id = int(request.form['professor_id'])
    nova_turma = {'descricao': descricao, 'professor_id': professor_id}
    adicionar_turma(nova_turma)
    return redirect(url_for('turmas.get_turmas'))

## FORMULÁRIO PARA EDITAR TURMA
@turmas_blueprint.route('/turmas/<int:id_turma>/editar', methods=['GET'])
def editar_turma_page(id_turma):
    try:
        turma = turma_por_id(id_turma)
        return render_template('turma_update.html', turma=turma)
    except TurmaNaoEncontrado:
        return jsonify({'message': 'Turma não encontrada'}), 404

## EDITAR UMA TURMA
@turmas_blueprint.route('/turmas/<int:id_turma>', methods=['PUT', 'POST'])
def update_turma(id_turma):
    try:
        turma = turma_por_id(id_turma)
        turma['descricao'] = request.form['descricao']
        turma['professor_id'] = int(request.form['professor_id'])
        atualizar_turma(id_turma, turma)
        return redirect(url_for('turmas.get_turma', id_turma=id_turma))
    except TurmaNaoEncontrado:
        return jsonify({'message': 'Turma não encontrada'}), 404

## DELETAR UMA TURMA
@turmas_blueprint.route('/turmas/delete/<int:id_turma>', methods=['DELETE', 'POST'])
def delete_turma(id_turma):
    try:
        excluir_turma(id_turma)
        return redirect(url_for('turmas.get_turmas'))
    except TurmaNaoEncontrado:
        return jsonify({'message': 'Turma não encontrada'}), 404