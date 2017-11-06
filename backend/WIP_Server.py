from threading import Thread

import requests as re
from flask import Flask, request

app = Flask(__name__)


@app.route('/itinerary', methods=['POST'])
def api_itinerary_search():
    if set(request.args) == set(['origin', 'destination']):
        raw_data = request.json
        origin = Place(raw_data['origin'])
        destination = Place(raw_data['destination'])
        results = Itinerary.ItinerarySearch(origin, destination, preferences)


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
