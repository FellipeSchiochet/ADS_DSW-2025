from flask import Flask, render_template, flash, redirect, url_for
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "segredo123"  # Necessário para usar flash() e session

@app.route("/")
def index():
    return render_template("base.html")

@app.route("/nova-receita", methods=["GET", "POST"])
def nova_receita():
    if request.method == "POST":
        nome = request.form.get("nome")
        ingredientes = request.form.get("ingredientes")
        preparo = request.form.get("preparo")

        # Validação
        if not nome or not ingredientes or not preparo:
            flash("⚠️ Todos os campos são obrigatórios!", "erro")
            return redirect(url_for("nova_receita"))

        # Armazena na sessão (poderia ser em banco de dados também)
        session["nome"] = nome
        session["ingredientes"] = ingredientes
        session["preparo"] = preparo

        return redirect(url_for("receita_criada"))

    return render_template("receita.html")


@app.route("/receita-criada")
def receita_criada():
    nome = session.get("nome")
    ingredientes = session.get("ingredientes")
    preparo = session.get("preparo")
    return render_template("receita_criada.html",
                           nome=nome,
                           ingredientes=ingredientes,
                           preparo=preparo)


if __name__ == "__main__":
    app.run(debug=True)
