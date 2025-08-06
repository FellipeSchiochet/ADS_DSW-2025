from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hobby ():
    return """
    <h1> Meu Hobby </h1>

    <p>Os meus hobbies são jogar vídeo games e jogar basquete</p>
    """

@app.route('/filme')
def filme():
    return """
    <h1> Meu filme preferido </h1>

    <p>O meu filme preferido é ratatui</p>
    """

@app.route('/musica')
def musica():
    return """
    <h1> Minha musica preferida </h1>    

    <p>A minha musica preferida é Thousend Years</p>
    """

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)