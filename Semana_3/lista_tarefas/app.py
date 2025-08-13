from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tarefas = []

@app.route('/')
def index():
    return render_template('index.html', tarefas=tarefas)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form['tarefa']
    data = request.form['data']
    tarefas.append({'nome': nome, 'data': data})
    return render_template('sucesso.html', tarefa=nome)

@app.route('/voltar')
def voltar():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
