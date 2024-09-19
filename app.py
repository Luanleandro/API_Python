from flask import Flask, jsonify, request

meuApp = Flask(__name__)

usuarios = [  
    {"nome":"caio","id":1,"email":"caio@email"},
    {"nome":"lucas","id":2,"email":"lucas@email"},
]

professores = [
    {"nome": "Joao", "id":1, "idade": 45, "materia": "Desenvolvimento Web"},
    {"nome": "Carlos", "id":2, "idade": 55, "materia": "Ambiente Nuvem"},
]


@meuApp.route('/professores', methods=['GET'])
def get_users():
    return jsonify({'professores': professores})

@meuApp.route('/professores', methods=['POST'])
def create_user():
    data = request.json
    usuario = {
        'id': len(usuarios) + 1,
        'nome': data['nome'],
        'email': data['email']
    }
    usuarios.append(usuario)
    return jsonify(usuario), 201

@meuApp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    for usuario in usuarios:
        print(usuario)
        if usuario['id'] == user_id:
            return usuario
    return jsonify({'mensagem': 'Usuário não encontrado'}), 404

@meuApp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    for usuario in usuarios:
        if usuario['id'] == user_id:
            data = request.json
            usuario['nome'] = data.get('nome', usuario['nome'])
            usuario['email'] = data.get('email', usuario['email'])
            return jsonify(usuario)
    return jsonify({'mensagem': 'Usuário não encontrado'}), 404

@meuApp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    for usuario in usuarios:
        if usuario['id'] == user_id:
            usuarios.remove(usuario)
            return jsonify({'mensagem': 'Usuário removido'})
    return jsonify({'mensagem': 'Usuário não encontrado'}), 404

if __name__ == '__main__':
    meuApp.run(debug=True)