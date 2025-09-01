# -*- coding: utf-8 -*-

# Passo 1: Importações e Configuração
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLALchemy, SQLAlchemy

# Inicializa a aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Sua-Seguranca-Mora-Aqui'

# Configuração correta do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meuapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Usuário: {self.nome}>'

# --- Rotas da Aplicação ---

# Rota principal que exibe o formulário e a lista de usuários
@app.route('/')
def index():
    usuarios = Usuario.query.all()
    return render_template('index.html', usuarios=usuarios)

@app.route('/adicionar', methods = ['POST'])
def adicionar_usuario():
    nome = request.form['nome']
    
    

# Passo 3: Criando o Banco de Dados Físico
if __name__ == '__main__':
    # Inicia o servidor de desenvolvimento do Flask
    app.run(host='0.0.0.0', port=5000, debug=True)