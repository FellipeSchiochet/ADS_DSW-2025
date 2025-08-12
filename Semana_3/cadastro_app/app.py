from flask import Flask, render_template, request

app = Flask (__name__)

@app.route("/", methods={ "GET", "POST"})
@app.route("/cadastro", methods={ "GET", "POST"})
def cadastro():
    if request.method == "POST":
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        return render_template('sucesso.html', nome=nome, email=email, senha=senha)

    return render_template('cadastro.html')

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5001, debug=True)