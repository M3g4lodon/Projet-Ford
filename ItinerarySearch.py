from datetime import datetime as dt
import requests
import Place
import Itinerary

class ItinerarySearch:
    """Choisit les différentes options d'itinéraires à partir des préférences Utilisateurs"""

    __itinerary_id = 1

    def __init__(self, origin, destination, date=None):
        self._id = ItinerarySearch.__itinerary_id
        self._origin = origin
        self._destination = destination

        # Par défaut, la date prise pour la recherche d'itinéraire est "Maintenant"
        if date is None:
            self._date = dt.now()
        else:
            self._date = date

        self._routes = []

    @property
    def id(self):
        return self._id

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        if isinstance(value, Place):
            self._origin = value
        else:
            raise TypeError("La valeur en entrée n'est pas un lieu !")

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, value):
        if isinstance(value, Place):
            self._destination = value
        else:
            raise TypeError("La valeur en entrée n'est pas un lieu !")

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if isinstance(value, dt):
            self._date = value
        else:
            raise TypeError("La valeur en entrée doit être une date.")

    @property
    def routes(self):
        return self._routes

    @routes.setter
    def routes(self, value):
        if isinstance(value, Route):
            self._routes = value
        else:
            raise TypeError("La valeur en entrée doit être un trajet (Route).")

if __name__ == "__main__":
    """Script de test"""
