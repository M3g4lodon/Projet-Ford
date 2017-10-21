from datetime import datetime as dt
import requests
import Place

class Itinerary:
    """Désigne un trajet entre deux points spécifiés dans la recherche d'itinéraires"""

    __TRANSIT_MODES = ["walking", "driving", "velib", "autolib","transit"]
    __TRANSIT_MODE_TYPES = ["rail", "bus", "tramway"]  # Liste des modes de transport possibles
    __route_id = 1

    def __init__(self, origin, destination, transit_mode, transit_mode_type, date=None):

        self._id = Itinerary.__route_id
        Itinerary.__route_id += 1

        if isinstance(origin, Place):
            self._origin = origin
        else:
            TypeError("L'origine doit être un objet Place")

        if isinstance(destination, Place):
            self._destination = destination
        else:
            TypeError("La destination doit être un objet Place")

        self._transit_mode = transit_mode
        self._transit_mode_type = transit_mode_type

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
    def transit_mode(self):
        return self._transit_mode

    @property
    def transit_mode_type(self):
        return self._transit_mode_type

    @transit_mode_type.setter
    def transit_mode_type(self,value):
        if value in Itinerary.__TRANSIT_MODE_TYPES:
            self.transit_mode_type = value
        elif not isinstance(value, str):    
            raise TypeError("Est attendue une chaine de caractère pour le type de mode de transport en commun.")
        else:
            raise ValueError("La valeur en entrée n'est pas un type de transport en commun possible.")


    @transit_mode.setter
    def transit_mode(self, value):
        if value in Itinerary.__TRANSIT_MODES:
            self._transit_mode = value
        elif not isinstance(value, str):
            raise TypeError("Est attendue une chaine de caractère pour le mode de transport.")
        else:
            raise ValueError("La valeur en entrée n'est pas un type de transport possible.")

if __name__ == "__main__":
    """Script de test"""

    # Test des Routes
    # To do

