# Importa as classe e funções necessarias das bibliotecas
from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

# Criando/Instanciando a aplicação Flask
app = Flask (__name__)

app.config['SECRET_KEY'] = 'uma_chave_de_segurança_muito_dificil'

class MeuFormulario(FlaskForm):
    nome = StringField('Nome completo', validators=[DataRequired(message='Campo obrigatório')])
    email = StringField('E-mail', validators=[
        DataRequired(message='Campo obrigatório'),
        Email(message='Por favor, ensira um e-mail valido!')
    ])
    submit = SubmitField('Enviar')

# Definindo as rotas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formulario', methods= ['GET', 'POST'])
def formulario():
    form = MeuFormulario()

    if form.validate_on_submit():
        nome_usuario = form.nome.data
        email_usuario = form.email.data
        flash(f'Cadastro Recebido para { nome_usuario } e { email_usuario }')


        return redirect(url_for('formulario'))
    return render_template('formulario.html', form=form)

# Definindo a execução
if __name__ == '__main__':
    app.run(debug=True)   