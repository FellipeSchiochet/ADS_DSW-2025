from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def ola_mundo():
    return "<h1>Olá Galera!11!11!</h1>"

@app.route('/sobre')
def sobre():
    return "Esta é a página sobre!"

@app.route('/perfil/<usuario>')
def perfil(usuario):
    return f'Exibindo perfil de: {usuario}'

@app.route('/produto/<int:id_produto>')
def consultar_produto(id_produto):
    return f'Exibindo o produto com o ID: {id_produto}'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        return f'<h1>Usuario: {usuario}</h1>'
    else:
        return '''
            <form method="post">
                <input type="text" name="usuario">
                <input type="submit" value="Login">
            </form>
        '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

