from flask import Blueprint, request, jsonify,render_template,redirect, url_for
from datetime import datetime
from .alunos_model import AlunoNaoEncontrado, listar_alunos, aluno_por_id, adicionar_aluno, atualizar_aluno, excluir_aluno
from config import db

alunos_blueprint = Blueprint('alunos', __name__)

@alunos_blueprint.route('/', methods=['GET'])
def getIndex():
    return "Meu index"

## ROTA PARA TODOS OS ALUNOS
@alunos_blueprint.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = listar_alunos()
    return render_template("alunos.html", alunos=alunos)

## ROTA PARA UM ALUNO
@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return render_template('aluno_id.html', aluno=aluno)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

## ROTA ACESSAR O FORMULARIO DE CRIAÇÃO DE UM NOVO ALUNOS   
@alunos_blueprint.route('/alunos/adicionar', methods=['GET'])
def adicionar_aluno_page():
    return render_template('criarAlunos.html')

## ROTA QUE CRIA UM NOVO ALUNO
@alunos_blueprint.route('/alunos', methods=['POST'])
def create_aluno():
    nome = request.form['nome']
    idade = int(request.form['idade'])
    data_nascimento = request.form['data_nascimento']  # Formato esperado: 'dd/mm/yyyy'
    nota_primeiro_semestre = float(request.form['nota_primeiro_semestre'])
    nota_segundo_semestre = float(request.form['nota_segundo_semestre'])
    turma_id = int(request.form['turma_id'])

    media_final = (nota_primeiro_semestre + nota_segundo_semestre) / 2

    novo_aluno = {
        'nome': nome,
        'idade': idade,
        'data_nascimento': data_nascimento,
        'nota_primeiro_semestre': nota_primeiro_semestre,
        'nota_segundo_semestre': nota_segundo_semestre,
        'media_final': media_final,
        'turma_id': turma_id,
    }
    print(novo_aluno)

    adicionar_aluno(novo_aluno)
    return redirect(url_for('alunos.get_alunos'))

## ROTA PARA O FORMULARIO PARA EDITAR UM NOVO ALUNO
@alunos_blueprint.route('/alunos/<int:id_aluno>/editar', methods=['GET'])
def editar_aluno_page(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return render_template('aluno_update.html', aluno=aluno)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

## ROTA QUE EDITA UM ALUNO
@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['PUT',"POST"])
def update_aluno(id_aluno):
        print("Dados recebidos no formulário:", request.form)
        try:
            aluno = aluno_por_id(id_aluno)
        
            if not aluno:
                return jsonify({'message': 'Aluno não encontrado'}), 404

            # Coletando dados do formulário
            nome = request.form['nome']
            idade = int(request.form['idade'])
            data_nascimento_str = request.form['data_nascimento']  # Ex: '04/08/2004'
            nota_primeiro_semestre = float(request.form['nota_primeiro_semestre'])
            nota_segundo_semestre = float(request.form['nota_segundo_semestre'])
            turma_id = int(request.form['turma_id'])

            # Convertendo data_nascimento para objeto date
            data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()

            # Atualizando os dados do aluno
            aluno['nome'] = nome
            aluno['idade'] = idade
            aluno['data_nascimento'] = data_nascimento
            aluno['nota_primeiro_semestre'] = nota_primeiro_semestre
            aluno['nota_segundo_semestre'] = nota_segundo_semestre
            aluno['media_final'] = (nota_primeiro_semestre + nota_segundo_semestre) / 2
            aluno['turma_id'] = turma_id

            # Atualizando no banco de dados
            atualizar_aluno(id_aluno, aluno)
            
            return redirect(url_for('alunos.get_aluno', id_aluno=id_aluno))
        except AlunoNaoEncontrado:
            return jsonify({'message': 'Aluno não encontrado'}), 404
   
## ROTA QUE DELETA UM ALUNO
@alunos_blueprint.route('/alunos/delete/<int:id_aluno>', methods=['DELETE','POST'])
def delete_aluno(id_aluno):
        try:
            excluir_aluno(id_aluno)
            return redirect(url_for('alunos.get_alunos'))
        except AlunoNaoEncontrado:
            return jsonify({'message': 'Aluno não encontrado'}), 404