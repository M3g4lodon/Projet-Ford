#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Entry file to the server
# To start the server, run the program, then open on your browser: http://localhost:5000/

from flask import Flask, render_template, request, jsonify

from backend.Itinerary import Itinerary
from backend.Place import Place
from backend.User import User
from backend.WIP_Suggested_Itineraries import Suggested_Itineraries

app = Flask(__name__)


@app.route('/')
def function():
    return render_template('Home.html')


@app.route('/itineraire')
def itinerary_search():
    TypeUser = request.args.get('TypeUser', 'Défaut')
    P_Permis = request.args.get('P_Permis', False)
    if P_Permis == "true":
        P_Permis=True
    else:
        P_Permis=False
    P_Meteo = request.args.get('P_Meteo', True)
    if P_Meteo == "true":
        P_Meteo=True
    else:
        P_Meteo=False
    P_Charge = request.args.get('P_Charge', False)
    if P_Charge == "true":
        P_Charge=True
    else:
        P_Charge=False

    org = request.args.get('origine', "Champs de Mars")
    dest = request.args.get('destination', "Place de la Nation")

    print("type utilisateur:{}\npermis:{}\nmeteo:{}\nchargé:{}\norigine:{}\ndestination:{}\n".format(TypeUser, P_Permis,
                                                                                                     P_Meteo, P_Charge,
                                                                                                     org, dest))

    origin = Place(org)
    destination = Place(dest)
    iti = Itinerary(origin=origin, destination=destination)
    Utilisateur = User(TypeUser, driving_license=P_Permis, weather=P_Meteo, loaded=P_Charge)
    resultat=Suggested_Itineraries(Utilisateur, iti)

    print(resultat)

    return jsonify(resultat)


if __name__ == '__main__':
    app.run(debug=True)
