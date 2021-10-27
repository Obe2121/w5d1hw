from flask import render_template, request
import requests
from app import app
from .forms import LoginForm
@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html.j2')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        #do Login stuff
        email = request.form.get("email").lower()
        password = request.form.get("password")
        if email in app.config.get("REGISTERED_USERS") and \
            password == app.config.get("REGISTERED_USERS").get(email).get('password'):
            return f"Login success Welcome {app.config.get('REGISTERED_USERS').get(email).get('name')}"
        error_string = "Invalid Email password combo"
        return render_template('login.html.j2', error = error_string, form=form)

    return render_template('login.html.j2', form=form)

@app.route('/pokemon', methods = ['GET', 'POST'])
def pokemon():
    if request.method == 'POST':
        name = request.form.get('pokemon_name')
        url = f'https://pokeapi.co/api/v2/pokemon/{name}/'
        response = requests.get(url)
        if response.ok:
            if not response.json()['stats']:
                return "We had an error loding your data"
            data = response.json()['stats']
            pokemon_stats=[]
            for pokemon in data:
                pokemon_dict={
                    'poke_name':pokemon['forms']['name'],
                    'base_hp':pokemon['stats'][0]['base_stat'],
                    'base_defense':pokemon['stats'][2]['base_stat'],
                    'base_attack':pokemon['stats'][1]['base_stat'],
                    }
                pokemon_stats.append(pokemon_dict)
            print(pokemon_stats)
            return render_template('pokemon.html.j2', pokemons=pokemon_stats)
        else:
            return "Houston we have a problem. Please try again"

    return render_template('pokemon.html.j2')

