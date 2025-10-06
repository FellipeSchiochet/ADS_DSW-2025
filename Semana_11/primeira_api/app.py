from flask import Flask, jsonify, request

from flask_cors import CORS

app = Flask(__name__)

CORS(app)

tarefas = [
    {
        'id': 1,
        'titulo': 'Aprender a criar API com Flask',
        'concluida': True
    },
    {
        'id': 2,
        'titulo': 'Testar API no Hoppscoth',
        'concluida': False
    }
]

# >>> ROTAS <<<

# Rota para obter todas as tarefas (GET /tarefas)
@app.route('/tarefas', methods=['GET'])
def obter_tarefas():
    return jsonify(tarefas)

# Rota para obter uma tarefa pelo seu ID (GET /tarefas/<id> | /tarefas/2)
@app.route('/tarefas/<int:tarefa_id>', methods=['GET'])
def obter_tarefa(tarefa_id):
    tarefa = next((t for t in tarefas if t['id'] == tarefa_id), None)
    
    if tarefa == None:
        return jsonify({'erro': 'Tarefa não encontrada!'}), 404
    
    return jsonify(tarefa)

#  Rota de criação de tarefa nova (POST /tarefas)
@app.route('/tarefas', methods=['POST'])
def criar_tarefa():
    if not request.json or not 'titulo' in request.json:
        return jsonify({'erro': 'A requisição deve ser um JSON e conter um atríbuto chamado título.'}), 400
    nova_tarefa = {
        'id': tarefas[-1]['id'] + 1 if tarefas else 1,
        'titulo': request.json['titulo'],
        'concluida': False
    }
    tarefas.append(nova_tarefa)
    return jsonify(nova_tarefa), 201

# Rota de atualização de tarefa existente (PUT /tarefas/<id>)
@app.route('/tarefas/<int:tarefa_id>', methods=['PUT'])
def atualizar_tarefa(tarefa_id):
    tarefa = next((t for t in tarefas if t['id'] == tarefa_id), None)
    if tarefa == None:
        return jsonify({'erro': 'Tarefa não encontrada!'}), 404
    
    tarefa['titulo'] = request.json.get('titulo', tarefa['titulo'])
    tarefa['concluida'] = request.json.get('concluida', tarefa['concluida'])
    
    return jsonify(tarefa)

# Rota de exclusão de tarefa existente (DELETE /tarefas/<id>)
@app.route('/tarefas/<int:tarefa_id>', methods=['DELETE'])
def excluir_tarefa(tarefa_id):
    tarefa = next((t for t in tarefas if t['id'] == tarefa_id), None)
    if tarefa == None:
        return jsonify({'erro': 'Tarefa não encontrada!'}), 404
    
    tarefas.remove(tarefa)
    
    return jsonify({'resultado': 'Tarefa excluída com sucesso!'})

if __name__ == '__main__':
    app.run(debug=True)
