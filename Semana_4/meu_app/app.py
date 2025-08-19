# Importa as classes e funções necessárias do Flask e WTForms
from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

# --------------------------
# CONFIGURAÇÃO DO APP
# --------------------------
app = Flask(__name__)  # Cria a aplicação Flask
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-dificil-de-adivinhar'
# A SECRET_KEY é usada pelo Flask-WTF para gerar tokens CSRF e proteger o formulário

# --------------------------
# FORMULÁRIO ANTIGO (simples)
# --------------------------
class MeuFormulario(FlaskForm):
    nome = StringField('Nome Completo', validators=[DataRequired(message="Este campo é obrigatório.")])
    # Campo de texto para o nome, obrigatório
    email = StringField('Seu Melhor E-mail', validators=[
        DataRequired(message="Este campo é obrigatório."),  # Não permite vazio
        Email(message="Por favor, insira um e-mail válido.")  # Valida o formato de e-mail
    ])
    submit = SubmitField('Enviar Cadastro')  # Botão de envio do formulário

# --------------------------
# NOVO FORMULÁRIO DE REGISTRO
# --------------------------
class FormularioRegistro(FlaskForm):
    nome = StringField('Nome Completo', validators=[DataRequired(message="Este campo é obrigatório.")])
    # Campo obrigatório para nome
    email = StringField('E-mail', validators=[
        DataRequired(message="Este campo é obrigatório."),
        Email(message="Insira um e-mail válido.")
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(message="Senha obrigatória."),
        Length(min=8, message="A senha deve ter pelo menos 8 caracteres.")  # Valida tamanho mínimo
    ])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[
        DataRequired(message="Confirme sua senha."),
        EqualTo('senha', message="As senhas não conferem.")  # Confirma se é igual à senha
    ])
    biografia = TextAreaField('Biografia (opcional)')
    # Campo opcional para escrever sobre si
    aceitar_termos = BooleanField('Aceito os Termos de Serviço', validators=[
        DataRequired(message="Você deve aceitar os termos para continuar.")  # Obrigatório marcar
    ])
    submit = SubmitField('Registrar')  # Botão de envio do registro

# --------------------------
# ROTAS EXISTENTES
# --------------------------

# Formulário simples
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    form = MeuFormulario()  # Instancia o formulário simples
    if form.validate_on_submit():  # Se o formulário foi enviado e válido
        nome_usuario = form.nome.data
        email_usuario = form.email.data
        flash(f'Cadastro recebido com sucesso para {nome_usuario} ({email_usuario})!', 'success')
        return redirect(url_for('formulario'))  # Redireciona para a mesma página
    return render_template('formulario.html', form=form)  # Renderiza o template

# Exemplo com valores pré-preenchidos por argumentos
@app.route('/formulario/preenchido-args', methods=['GET', 'POST'])
def formulario_com_argumentos():
    form = MeuFormulario(nome="Fulano de Tal", email="fulano@exemplo.com")  # Valores iniciais
    if form.validate_on_submit():
        flash(f'Dados de "{form.nome.data}" atualizados com sucesso!', 'success')
        return redirect(url_for('formulario_com_argumentos'))
    return render_template('formulario.html', form=form)

# Exemplo com valores pré-preenchidos por objeto
@app.route('/formulario/preenchido-obj', methods=['GET', 'POST'])
def formulario_com_objeto():
    class UsuarioMock:
        def __init__(self, nome, email):
            self.nome = nome
            self.email = email
    usuario_do_banco = UsuarioMock(nome="Ciclano da Silva", email="ciclano@banco.com")
    form = MeuFormulario(obj=usuario_do_banco)  # Popula formulário com dados do objeto
    if form.validate_on_submit():
        flash(f'Dados de "{form.nome.data}" atualizados com sucesso!', 'success')
        return redirect(url_for('formulario_com_objeto'))
    return render_template('formulario.html', form=form)

# --------------------------
# NOVA ROTA DE REGISTRO
# --------------------------
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = FormularioRegistro()  # Instancia o formulário de registro
    if form.validate_on_submit():  # Se o formulário foi enviado e válido
        flash(f"Registro realizado com sucesso para {form.nome.data} ({form.email.data})!", "success")
        return redirect(url_for('registro'))  # Redireciona para a mesma página
    return render_template('registro.html', form=form)  # Renderiza o template do registro

# --------------------------
# ROTA PRINCIPAL
# --------------------------
@app.route('/')
def index():
    return render_template('index.html')  # Página inicial com links para os formulários

# --------------------------
# EXECUÇÃO DO APP
# --------------------------
if __name__ == '__main__':
    app.run(debug=True)  # Executa o servidor Flask em modo debug
