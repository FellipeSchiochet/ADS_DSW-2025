# -*- coding: utf-8 -*-

# Passo 1: Importações e Configuração
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Inicializa a aplicação Flask
app = Flask(__name__)

# Chave secreta para segurança das sessões e formulários
app.config['SECRET_KEY'] = 'sua-chave-secreta-pode-ser-qualquer-coisa'

# Configuração do Banco de Dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meuapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa a extensão do banco de dados com a aplicação
db = SQLAlchemy(app)


# Passo 2: Criando o Modelo
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Alteração aqui: lazy='subquery' garante que postagens sejam carregadas junto
    postagens = db.relationship('Postagem', backref='autor', lazy='subquery')

    def __repr__(self):
        return f'<Usuário {self.nome}>'

class Postagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(80), unique=True, nullable=False)
    descricao = db.Column(db.String(120), unique=True, nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def __repr__(self):
        return f'<Postagem {self.titulo}>'


# --- Rotas da Aplicação ---
@app.route('/')
def index():
    usuarios = Usuario.query.all()
    return render_template('index.html', usuarios=usuarios)

@app.route('/adicionar', methods=['POST'])
def adicionar_usuario():
    nome = request.form['nome']
    email = request.form['email']
    novo_usuario = Usuario(nome=nome, email=email)
    db.session.add(novo_usuario)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/postagens')
def postagens():
    postagens = Postagem.query.all()
    usuarios = Usuario.query.all()
    return render_template('postagens.html', postagens=postagens, usuarios=usuarios)

@app.route('/adicionar_postagem', methods=['POST'])
def adicionar_postagem():
    titulo = request.form['titulo']
    descricao = request.form['descricao']
    usuario_id = request.form['usuario_id']

    nova_postagem = Postagem(titulo=titulo, descricao=descricao, usuario_id=usuario_id)
    db.session.add(nova_postagem)
    db.session.commit()
    return redirect(url_for('postagens'))


# Passo 3: Criando o Banco de Dados Físico
if __name__ == '__main__':
    with app.app_context():
        print("Apagando o banco de dados antigo (se existir)...")
        db.drop_all()
        print("Criando todas as tabelas do zero...")
        db.create_all()
        print("Banco de dados e tabelas criados com sucesso!")

    app.run(host='0.0.0.0', port=5001, debug=True)
