from datetime import datetime as dt
import requests
import Leg
import Place

class Route:
    """Désigne un trajet entre deux points spécifiés dans l'itinéraire"""

    __TRANSPORT_MODES = ["walking", "driving", "velib", "autolib"]  # Liste des modes de transport possibles
    __route_id = 1

    def __init__(self, origin, destination, transport_mode, date=None):
        self._id = Route.__route_id
        Route.__route_id += 1

        self._origin = origin
        self._destination = destination
        self._transport_mode = transport_mode

        # Par défaut, la date prise pour la recherche d'itinéraire est "Maintenant"
        if date is None:
            self._date = dt.now()
        else:
            self._date = date

    @property
    def id(self):
        return self._id

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = value

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, value):
        self._destination = value

    @property
    def transport_mode(self):
        return self._transport_mode

    @transport_mode.setter
    def transport_mode(self, value):
        if value in Route.__TRANSPORT_MODES:
            self._transport_mode = value
        elif not isinstance(value, str):
            raise TypeError("Est attendue une chaine de caractère pour le mode de transport.")
        else:
            raise ValueError("La valeur en entrée n'est pas un type de transport possible.")

if __name__ == "__main__":
    """Script de test"""

    # Test des Routes
    # To do

