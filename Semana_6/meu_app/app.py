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
class Usuario(db.Model):
    # Colunas da tabela "usuario"
    id = db.Column(db.Integer, primary_key=True)  # Coluna de ID (chave primária)
    nome = db.Column(db.String(80), unique=True, nullable=False)  # Nome do usuário
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email do usuário

    # Representação em string do objeto (para debug e exibição)
    def __repr__(self):
        return f'<Usuário: {self.nome}>'


# --- Passo 3: Rotas da Aplicação ---
# Rota principal que exibe o formulário e a lista de usuários
@app.route('/')
def index():
    usuarios = Usuario.query.all()  # Consulta todos os usuários cadastrados
    return render_template('index.html', usuarios=usuarios)


# Rota para adicionar um novo usuário ao banco de dados
@app.route('/adicionar', methods=['POST'])
def adicionar_usuario():
    # Captura os dados do formulário HTML
    nome = request.form['nome']
    email = request.form['email']
    
    # Cria um novo objeto Usuario
    novo_usuario = Usuario(nome=nome, email=email)
    
    # Adiciona o usuário no banco e confirma a transação
    db.session.add(novo_usuario)
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
