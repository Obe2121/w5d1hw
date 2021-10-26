from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html.j2')

@app.route('/pokemon', methods = ['GET', 'POST'])
def pokemon():
    if request.method == 'POST':
        name = request.form.get('name')
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

