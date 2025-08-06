from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    usuario = "João Cana Brava"
    return render_template('index.html', nome_usuario = usuario)

@app.route('/perfil/<nome>')
def perfil(nome):
    logado = True
    usuario = nome
    return render_template('perfil.html', logado = logado, nome_usuario = usuario )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)