import json
from threading import Thread

import requests as re
from flask import Flask, request, jsonify

"""
@app.route('/articles')
def api_articles():
    return 'List of ' + url_for('api_articles')

@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid
"""

Users=[]

app = Flask(__name__)

@app.route('/auth', methods=['POST'])
def api_authentification():
    print(json.dumps(request.json))
    # user=User()
    user_id = 17  # à changer
    return jsonify({"id": user_id})


@app.route('/itinerary', methods=['GET'])
def api_itinerary_search():
    if all([x in request.args for x in ['user_id', 'origin', 'destination', 'luggage']]):
        for user in Users:
            raw_data = request.json
            if user.id == raw_data['user_id']:
                origin = Place(raw_data['origin'])
                destination = Place(raw_data['destination'])
                user.newItinerarySearch

class Server(Thread):
    """Notre serveur où s'éxécute notre service "comment y aller ?" """

    def run(self):
        app.run()


class Tester(Thread):
    """Classe de test """

    def run(self):
        # Test de notre API
        raw_data = re.post("http://127.0.0.1:5000/auth",json={"permis":False})
        print(raw_data.json())


if __name__ == '__main__':
    server = Server()
    test = Tester()

    server.start()
    test.start()
