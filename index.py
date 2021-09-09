from flask import Flask, redirect, request, render_template
from flask.helpers import url_for
from flask_restx import Resource, Api
import random

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
    #Affichage du résultat
    if(result == True): 
        winner = "Le Joueur 1 a gagner"
    elif(result == False): 
        winner = "Le Joueur 2 a gagner"
    return {"Choix du Joueur1": J1, "Choix du Joueur2": J2,"Gagnant": winner }

if __name__ == '__main__':
    app.run(debug=True)