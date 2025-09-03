# app.py
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField

# === Configuração da Aplicação ===
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# === Modelos ===
class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    livros = db.relationship('Livro', backref='autor_rel', lazy=True)

    def __repr__(self):
        return f'<Autor {self.nome}>'


class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    ano_publicacao = db.Column(db.Integer, nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey('autor.id'), nullable=False)

    def __repr__(self):
        return f'<Livro {self.titulo}>'


# Função para popular o QuerySelectField
def carregar_autores():
    return Autor.query.all()


# === Formulários ===
class AutorForm(FlaskForm):
    nome = StringField('Nome do Autor', validators=[DataRequired()])
    submit = SubmitField('Cadastrar Autor')


class LivroForm(FlaskForm):
    titulo = StringField('Título do Livro', validators=[DataRequired()])
    ano_publicacao = IntegerField('Ano de Publicação', validators=[DataRequired()])
    autor = QuerySelectField('Autor', query_factory=carregar_autores, get_label='nome', allow_blank=False)
    submit = SubmitField('Cadastrar Livro')


# === Rotas ===
@app.route('/', methods=['GET', 'POST'])
@app.route('/livros', methods=['GET', 'POST'])
def listar_livros():
    form = LivroForm()
    if form.validate_on_submit():
        novo_livro = Livro(
            titulo=form.titulo.data,
            ano_publicacao=form.ano_publicacao.data,
            autor_id=form.autor.data.id  # form.autor.data é o objeto Autor
        )
        db.session.add(novo_livro)
        db.session.commit()
        flash('Livro cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_livros'))

    livros = Livro.query.all()
    return render_template('livros.html', form=form, livros=livros)


@app.route('/autores', methods=['GET', 'POST'])
def listar_autores():
    form = AutorForm()
    if form.validate_on_submit():
        # Verifica se o autor já existe
        autor_existente = Autor.query.filter_by(nome=form.nome.data).first()
        if autor_existente:
            flash('Este autor já está cadastrado.', 'warning')
        else:
            novo_autor = Autor(nome=form.nome.data)
            db.session.add(novo_autor)
            db.session.commit()
            flash('Autor cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_autores'))

    autores = Autor.query.all()
    return render_template('autores.html', form=form, autores=autores)


# === Inicialização do banco de dados ===
with app.app_context():
    db.create_all()
    
# No final do arquivo app.py
if __name__ == '__main__':
    app.run(debug=True)