from flask import Flask, jsonify, request

app = Flask(__name__)

# Modelo de dados do produto
produtos = [
    {"id": 1, "nome": "Notebook Dell", "preco": 4500.00, "estoque": 10},
    {"id": 2, "nome": "Mouse Gamer", "preco": 150.00, "estoque": 50},
    {"id": 3, "nome": "Teclado Mecânico", "preco": 300.00, "estoque": 25}
]

# Rota de teste
@app.route(
    '/'
)
def hello_world():
    return 'Hello, World!'

# GET /produtos - Listar todos os produtos
@app.route(
    '/produtos',
    methods=['GET']
)
def listar_produtos():
    return jsonify(produtos)

# GET /produtos/<id> - Obter um produto específico pelo ID
@app.route(
    '/produtos/<int:id>',
    methods=['GET']
)
def obter_produto_por_id(id):
    for produto in produtos:
        if produto['id'] == id:
            return jsonify(produto)
    return jsonify({'mensagem': 'Produto não encontrado'}), 404

# POST /produtos - Criar um novo produto
@app.route(
    '/produtos',
    methods=['POST']
)
def criar_produto():
    novo_produto = request.get_json()
    if not novo_produto or 'nome' not in novo_produto or 'preco' not in novo_produto or 'estoque' not in novo_produto:
        return jsonify({'mensagem': 'Dados inválidos para o produto'}), 400
    
    novo_id = max([p['id'] for p in produtos]) + 1 if produtos else 1
    produto = {
        'id': novo_id,
        'nome': novo_produto['nome'],
        'preco': novo_produto['preco'],
        'estoque': novo_produto['estoque']
    }
    produtos.append(produto)
    return jsonify(produto), 201

# PUT /produtos/<id> - Atualizar um produto existente
@app.route(
    '/produtos/<int:id>',
    methods=['PUT']
)
def atualizar_produto(id):
    produto_atualizado = request.get_json()
    if not produto_atualizado:
        return jsonify({'mensagem': 'Dados inválidos para o produto'}), 400

    for i, produto in enumerate(produtos):
        if produto['id'] == id:
            produtos[i]['nome'] = produto_atualizado.get('nome', produtos[i]['nome'])
            produtos[i]['preco'] = produto_atualizado.get('preco', produtos[i]['preco'])
            produtos[i]['estoque'] = produto_atualizado.get('estoque', produtos[i]['estoque'])
            return jsonify(produtos[i])
    return jsonify({'mensagem': 'Produto não encontrado'}), 404

# DELETE /produtos/<id> - Deletar um produto
@app.route(
    '/produtos/<int:id>',
    methods=['DELETE']
)
def deletar_produto(id):
    global produtos
    produtos = [produto for produto in produtos if produto['id'] != id]
    return jsonify({'mensagem': 'Produto deletado com sucesso'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
