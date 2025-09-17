import os
from flask import Flask, render_template, request, redirect, url_for
from extensions import db  # agora importamos o db de extensions.py

def create_app():
    app = Flask(__name__)
    
    # Caminho base do projeto
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Configurações do banco
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'receitas.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Cria a pasta 'instance' se não existir
    instance_path = os.path.join(basedir, 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)

    # Inicializa o SQLAlchemy com a aplicação
    db.init_app(app)

    # Importa os modelos e cria as tabelas
    with app.app_context():
        from models import Chef, PerfilChef, Receita, Ingrediente, ReceitaIngrediente
        db.create_all()

    # --- Rotas ---
    @app.route('/')
    def index():
        from models import Receita
        receitas = Receita.query.all()
        return render_template('index.html', receitas=receitas)

    @app.route('/receita/nova', methods=['GET', 'POST'])
    def criar_receita():
        from models import Receita, Ingrediente, ReceitaIngrediente, Chef
        if request.method == 'POST':
            titulo = request.form['titulo']
            instrucoes = request.form['instrucoes']
            chef_id = request.form['chef_id']

            # Cria a receita
            nova_receita = Receita(titulo=titulo, instrucoes=instrucoes, chef_id=chef_id)
            db.session.add(nova_receita)

            # Processa ingredientes
            ingredientes_str = request.form['ingredientes']
            pares_ingredientes = [par.strip() for par in ingredientes_str.split(',') if par.strip()]
            
            for par in pares_ingredientes:
                if ':' in par:
                    nome, qtd = par.split(':', 1)
                    nome_ingrediente = nome.strip().lower()
                    quantidade = qtd.strip()

                    ingrediente = Ingrediente.query.filter_by(nome=nome_ingrediente).first()
                    if not ingrediente:
                        ingrediente = Ingrediente(nome=nome_ingrediente)
                        db.session.add(ingrediente)

                    associacao = ReceitaIngrediente(
                        receita=nova_receita,
                        ingrediente=ingrediente,
                        quantidade=quantidade
                    )
                    db.session.add(associacao)

            db.session.commit()
            return redirect(url_for('index'))

        chefs = Chef.query.all()
        return render_template('criar_receita.html', chefs=chefs)

    @app.route('/chef/<int:chef_id>')
    def detalhes_chef(chef_id):
        from models import Chef
        chef = Chef.query.get_or_404(chef_id)
        return render_template('detalhes_chef.html', chef=chef)

    # --- Comando CLI ---
    @app.cli.command('init-db')
    def init_db_command():
        """Cria as tabelas e popula com dados de exemplo."""
        from models import Chef, PerfilChef, Receita, Ingrediente, ReceitaIngrediente

        db.drop_all()
        db.create_all()

        chef1 = Chef(nome='Ana Maria')
        perfil1 = PerfilChef(especialidade='Culinária Brasileira', anos_experiencia=25, chef=chef1)

        chef2 = Chef(nome='Érick Jacquin')
        perfil2 = PerfilChef(especialidade='Culinária Francesa', anos_experiencia=30, chef=chef2)

        ingredientes = {
            'tomate': Ingrediente(nome='tomate'),
            'cebola': Ingrediente(nome='cebola'),
            'farinha': Ingrediente(nome='farinha'),
            'ovo': Ingrediente(nome='ovo'),
            'manteiga': Ingrediente(nome='manteiga')
        }

        db.session.add_all([chef1, chef2] + list(ingredientes.values()))

        receita1 = Receita(titulo='Molho de Tomate Clássico', instrucoes='Cozinhe os tomates e a cebola por 20 minutos.', chef=chef1)
        receita2 = Receita(titulo='Bolo Simples', instrucoes='Misture todos os ingredientes e asse por 40 minutos.', chef=chef1)
        receita3 = Receita(titulo='Petit Gâteau', instrucoes='Derreta a manteiga com chocolate e asse em forno alto.', chef=chef2)

        db.session.add_all([receita1, receita2, receita3])

        db.session.add_all([
            ReceitaIngrediente(receita=receita1, ingrediente=ingredientes['tomate'], quantidade='5 unidades'),
            ReceitaIngrediente(receita=receita1, ingrediente=ingredientes['cebola'], quantidade='1 unidade'),
            ReceitaIngrediente(receita=receita2, ingrediente=ingredientes['farinha'], quantidade='2 xicaras'),
            ReceitaIngrediente(receita=receita2, ingrediente=ingredientes['ovo'], quantidade='3 unidades'),
            ReceitaIngrediente(receita=receita3, ingrediente=ingredientes['manteiga'], quantidade='150g')
        ])

        db.session.commit()
        print('Banco de dados inicializado com sucesso!')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

