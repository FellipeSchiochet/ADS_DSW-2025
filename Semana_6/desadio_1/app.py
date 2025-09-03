# -*- coding: utf-8 -*-

# --- Passo 1: Importações e Configuração ---
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy  # Corrigido (antes tinha "SQLALchemy")

# Inicializa a aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Sua-Seguranca-Mora-Aqui'  # Chave de segurança da aplicação

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meuapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa a conexão com o banco de dados
db = SQLAlchemy(app)


# --- Passo 2: Criação do Modelo (Tabela do Banco de Dados) ---
class Postagem(db.Model):
    # Colunas da tabela "usuario"
    id = db.Column(db.Integer, primary_key=True)  # Coluna de ID (chave primária)
    titulo = db.Column(db.String(80), unique=False)  # Título da postagem
    descricao = db.Column(db.String(120), unique=False)  # Descrição da postagem

    # Representação em string do objeto (para debug e exibição)
    def __repr__(self):
        return f'<Título: {self.titulo}>'


# --- Passo 3: Rotas da Aplicação ---
# Rota principal que exibe o formulário e a lista de postagens
@app.route('/')
def index():
    postagens = Postagem.query.all()  # Consulta todos os usuários cadastrados
    return render_template('index.html', postagens=postagens)


# Rota para adicionar uma nova postagem ao banco de dados
@app.route('/adicionar', methods=['POST'])
def adicionar_postagem():
    # Captura os dados do formulário HTML
    titulo = request.form['titulo']
    descricao = request.form['descricao']
    
    # Cria um novo objeto Postagem
    novo_postagem = Postagem(titulo=titulo, descricao=descricao)
    
    # Adiciona o postagem no banco e confirma a transação
    db.session.add(novo_postagem)
    db.session.commit()
    
    # Redireciona de volta para a página inicial
    return redirect(url_for('index'))  # corrigido (não é 'index.html', é 'index')


# Passo 3: Criando o Banco de Dados Físico
if __name__ == '__main__':
    with app.app_context():
        #db.drop_all()  # Remove todas as tabelas do banco (use com cuidado!)
        db.create_all() # Cria todas as tabelas definidas nos Models (se não existirem)
        

# --- Passo 4: Iniciando o Servidor ---
if __name__ == '__main__':
    # Inicia o servidor Flask em modo de desenvolvimento
    app.run(host='0.0.0.0', port=5000, debug=True)
