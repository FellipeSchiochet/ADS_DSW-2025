import os
from datetime import date
from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField
from wtforms.validators import DataRequired


# --- Configuração da Aplicação Flask ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


# --- Validador Personalizado: Impede datas passadas ---
def data_futura(form, field):
    """Validador que impede o cadastro de eventos com data no passado."""
    if field.data < date.today():
        raise ValueError("A data do evento não pode ser no passado.")


# --- Definição do Formulário com WTForms ---
class EventoForm(FlaskForm):
    """Formulário para cadastro de eventos."""
    nome_evento = StringField(
        'Nome do Evento',
        validators=[DataRequired(message="O nome do evento é obrigatório.")]
    )
    data_evento = DateField(
        'Data do Evento',
        format='%Y-%m-%d',
        validators=[
            DataRequired(message="A data do evento é obrigatória."),
            data_futura  # ← Validador personalizado
        ]
    )
    organizador_evento = StringField(
        'Organizador do Evento',
        validators=[DataRequired(message="O campo organizador é obrigatório.")]
    )
    mensagem = TextAreaField('Mensagem')
    enviar = SubmitField('Enviar')


# --- Definição de um Objeto para Simulação ---
class Usuario:
    def __init__(self, nome_evento="", data_evento=None, organizador_evento="", mensagem=""):
        self.nome_evento = nome_evento
        self.data_evento = data_evento
        self.organizador_evento = organizador_evento
        self.mensagem = mensagem


# --- Rotas da Aplicação ---
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/vazio", methods=['GET', 'POST'])
def formulario_vazio():
    """Cenário 1: Formulário Vazio."""
    form = EventoForm()

    if form.validate_on_submit():
        nome_evento = form.nome_evento.data
        flash(f"Evento '{nome_evento}' cadastrado com sucesso!", "success")
        return redirect(url_for('index'))

    return render_template(
        'formulario.html',
        form=form,
        title="1. Formulário Vazio"
    )


@app.route("/via-argumentos", methods=['GET', 'POST'])
def formulario_via_argumentos():
    """Cenário 2: Formulário Preenchido via Argumentos."""
    form = EventoForm()

    if form.validate_on_submit():
        nome_evento = form.nome_evento.data
        flash(f"Evento '{nome_evento}' cadastrado com sucesso!", "success")
        return redirect(url_for('index'))

    elif not form.is_submitted():
        # Preenche com dados iniciais usando kwargs
        form = EventoForm(**{
            'nome_evento': 'Festa de Aniversário',
            'data_evento': date(2025, 12, 25),
            'organizador_evento': 'Carlos Souza',
            'mensagem': 'Evento familiar com amigos.'
        })

    return render_template(
        'formulario.html',
        form=form,
        title="2. Formulário Preenchido via Argumentos"
    )


@app.route("/via-objeto", methods=['GET', 'POST'])
def formulario_via_objeto():
    """Cenário 3: Formulário Preenchido via Objeto."""
    form = EventoForm()

    if form.validate_on_submit():
        nome_evento = form.nome_evento.data
        flash(f"Evento '{nome_evento}' cadastrado com sucesso!", "success")
        return redirect(url_for('index'))

    elif not form.is_submitted():
        # Cria um objeto com atributos compatíveis com o formulário
        usuario_mock = Usuario(
            nome_evento="Conferência Tech 2025",
            data_evento=date(2025, 9, 15),
            organizador_evento="Ana Lima",
            mensagem="Evento corporativo em setembro."
        )
        # Preenche o formulário com o objeto
        form = EventoForm(obj=usuario_mock)

    return render_template(
        'formulario.html',
        form=form,
        title="3. Formulário Preenchido via Objeto"
    )


# --- Execução da Aplicação ---
if __name__ == '__main__':
    app.run(debug=True)