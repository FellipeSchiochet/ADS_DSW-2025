from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Lista de produtos de exemplo (substitui a lista de tarefas)
produtos = [
    {
        'id': 1,
        'nome': 'Camiseta Básica',
        'preco': 29.99,
        'estoque': 50
    },
    {
        'id': 2,
        'nome': 'Calça Jeans',
        'preco': 79.90,
        'estoque': 30
    },
    {
        'id': 3,
        'nome': 'Tênis Esportivo',
        'preco': 129.99,
        'estoque': 15
    }
]

# >>> Construção de Rotas para Produtos <<<

# Rota para obter todos os produtos (GET /produtos)
@app.route('/produtos', methods=['GET'])
def obter_produtos():
    return jsonify(produtos)

# Rota para obter um produto específico pelo ID (GET /produtos/<int:id>)
@app.route('/produtos/<int:produto_id>', methods=['GET'])
def obter_produto(produto_id):
    produto = next((p for p in produtos if p['id'] == produto_id), None)
    if produto is None:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    return jsonify(produto)

# Rota para criar um novo produto (POST /produtos)
@app.route('/produtos', methods=['POST'])
def criar_produto():
    if not request.json or not 'nome' in request.json or not 'preco' in request.json or not 'estoque' in request.json:
        return jsonify({'erro': 'A requisição deve ser JSON e conter os campos: nome, preco, estoque.'}), 400
    novo_produto = {
        'id': produtos[-1]['id'] + 1 if produtos else 1,
        'nome': request.json['nome'],
        'preco': float(request.json['preco']),  # Converte para float
        'estoque': int(request.json['estoque']) # Converte para int
    }
    produtos.append(novo_produto)
    return jsonify(novo_produto), 201

# Rota para atualizar um produto existente (PUT /produtos/<int:id>)
@app.route('/produtos/<int:produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    produto = next((p for p in produtos if p['id'] == produto_id), None)
    if produto is None:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    if not request.json:
        return jsonify({'erro': 'A requisição deve ser JSON.'}), 400
    produto['nome'] = request.json.get('nome', produto['nome'])
    # Converte para float/int apenas se o campo estiver presente no JSON
    if 'preco' in request.json:
        produto['preco'] = float(request.json['preco'])
    if 'estoque' in request.json:
        produto['estoque'] = int(request.json['estoque'])
    return jsonify(produto)

# Rota para deletar um produto (DELETE /produtos/<int:id>)
@app.route('/produtos/<int:produto_id>', methods=['DELETE'])
def deletar_produto(produto_id):
    global produtos
    produto = next((p for p in produtos if p['id'] == produto_id), None)
    if produto is None:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    produtos = [p for p in produtos if p['id'] != produto_id]
    return jsonify({'resultado': 'Produto deletado com sucesso'})

# Desafio Extra: Rota para simular a compra de uma unidade de um produto (POST /produtos/<int:id>/comprar)
@app.route('/produtos/<int:produto_id>/comprar', methods=['POST'])
def comprar_produto(produto_id):
    produto = next((p for p in produtos if p['id'] == produto_id), None)
    if produto is None:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    if produto['estoque'] <= 0:
        return jsonify({'erro': 'Produto fora de estoque'}), 400
    produto['estoque'] -= 1 # Diminui o estoque em 1
    return jsonify(produto), 200 # Retorna o produto atualizado

# >>> Fim da Construção de Rotas <<<

if __name__ == '__main__':
    app.run(debug=True)