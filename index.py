from flask import Flask, redirect, request, render_template, json
from flask.helpers import url_for
from flask_restx import Resource, Api
import os
import random
import json

app = Flask(__name__)
api = Api(app)

# Symboles
def Symboles():
    symboles = ["Pierre","Papier","Ciseaux","Lezard","Spock"]
    return symboles

def Combinaisons():
    combis = [None, False, True, True , False], [True, None, False, False, True], [False, True, None, True, False], [False, True, False, None, True], [True, False, True, False, None]
    return combis

# Choix du Joueur 1
def Player1(symboles,x):
    if(x not in symboles):
        J1 = "Votre Choix est invalide"
        return J1
    J1 = x
    return J1

# Choix du Joueur 2
def Player2(symboles,J1):
    Choix_J2 = random.randint(0,4)
    J2 = symboles[Choix_J2]
    while(J2 == J1):
        Choix_J2 = random.randint(0,4)
        J2 = symboles[Choix_J2]
    return J2  

# Route avec Parametre dans l'url
@api.route('/Plus_One/<x>')
class Plus_One(Resource):
    def get(self,x):
        x = int(x)
        return{"x": x+1}

@api.route('/JanKenPon/stats')
class Stats(Resource):
    def get(self):
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT,"stats.json")
        data = json.load(open(json_url))
        return data
@api.route('/JanKenPon/reset_stats')
class Reset_Stats(Resource):
    def get(self):
        data = {}
        data['Game'] = []
        data['Game'].append({
            'Nb_game':0,
            'Win':0,
            'Lose':0
        })
        data['Symboles'] = []
        data['Symboles'].append({
            "Pierre": 0,
            "Papier": 0,
            "Ciseaux": 0,
            "Lezard": 0,
            "Spock": 0
        })
        json.dumps(data, indent=4)
        with open('stats.json', 'w') as outfile:
            json.dump(data, outfile)
        return "Reset Successful"
@api.route('/JanKenPon')
class JanKenPon(Resource):
    def get(self):
        return redirect("/JanKenPon/choice")

@app.route('/JanKenPon/choice')
def choice():
    return render_template('choice.html')

@app.route('/JanKenPon/verify', methods = ['POST','GET'])
def verify():
    if request.method == 'POST':
        data = request.form['name']

        return redirect(url_for("game",x=data))

@app.route('/JanKenPon/fail')
def fail():
    return render_template('fail.html')

@app.route('/JanKenPon/Game?data=<x>')
def game(x):
    symboles = Symboles()
    combis = Combinaisons()
    # Définition des Choix
    J1 = Player1(symboles,x)
    if(J1 not in symboles):
        return redirect("/JanKenPon/fail")
    J2 = Player2(symboles,J1)
    # Récupération du résultat en fonction des choix
    J1_equiv = symboles.index(J1)
    J2_equiv = symboles.index(J2)
    result = combis[J1_equiv][J2_equiv]
    #Update du fichier stats.json
    with open('stats.json') as json_file:
        data = json.load(json_file)
        for i in data['Symboles']:
            i[J1] += 1

        #Affichage du résultat
        if(result == True):
            for i in data['Game']:
                i['Nb_game'] += 1
                i['Win'] += 1
            winner = "Le Joueur 1 a gagner"
        elif(result == False):
            for i in data['Game']:
                i['Nb_game'] += 1
                i['Lose'] += 1
            winner = "Le Joueur 2 a gagner"
        for i in data['Game']:
            i['Winrate'] = f"{( i['Win']*100 ) / (i['Nb_game'])}%"
        with open('stats.json', 'w') as outfile:
            json.dump(data, outfile)
        return {"Choix du Joueur1": J1, "Choix du Joueur2": J2,"Gagnant": winner }

if __name__ == '__main__':
    app.run(debug=True)