#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Entry file to the server
# To start the server, run the program, then open on your browser: http://localhost:5000/

from flask import Flask, render_template, request, Response
from backend.Place import Place
from backend.User import User
from backend.WIP_Suggested_Itineraries import Suggested_Itineraries
from backend.Itinerary import Itinerary

app = Flask(__name__)


@app.route('/')
def function():
    return render_template('Home.html')


@app.route('/itineraire')
def itinerary_search():
    TypeUser = request.args.get('TypeUser', 'Défaut')
    P_Permis = request.args.get('P_Permis', "false")
    P_Meteo = request.args.get('P_Meteo', "true")
    P_Charge = request.args.get('P_Charge', "false")

    org = request.args.get('origine', "Champs de Mars")
    dest = request.args.get('destination', "Place de la Nation")

    print("type utilisateur:{}\npermis:{}\nmeteo:{}\nchargé:{}\norigine:{}\ndestination:{}\n".format(TypeUser, P_Permis,
                                                                                                     P_Meteo, P_Charge,
                                                                                                     org, dest))

    origin = Place(org)
    destination = Place(dest)
    iti = Itinerary(origin=origin, destination=destination)
    Utilisateur = User(TypeUser, driving_license=P_Permis, weather=P_Meteo, loaded=P_Charge)
    Suggested_Itineraries(Utilisateur, iti)

    return Response(status=200)


if __name__ == '__main__':
    app.run(debug=True)
