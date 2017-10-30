
import math
from datetime import datetime

from Place import Place


# TODO Prise en compte de l'ordre de préférence sur Autolib/velib (itinerary_index)
# TODO Méthodes de conversion sec(int) --> h:m:s (str) et m(int) --> km (str)

class Itinerary:
    """Désigne un trajet entre deux points spécifiés dans la recherche d'itinéraires"""

    __TRANSPORT_MODES = ["walking", "driving", "velib", "autolib", "transit", "bicycling"]

    __TRANSIT_MODE_TYPES = ["bus", "subway", "train", "tram", "rail", "bus|rail"]
    # Liste des modes de transport possibles
    # bus       : bus
    # subway    : subway
    # train     : train
    # tram      : tramway and light subway
    # rail      : subway+train+tram (could be written as subway|train|tram)
    # bus|rail  : all transit mode types !

    __UBER_MODE_TYPES = ["uberx", "uberpool", "uberberline", "ubergreen", "ubervan", "access"]

    __route_id = 1

    def __init__(self, origin, destination, date=None, transit_mode_type=None, itinerary_index=0):

        self._id = Itinerary.__route_id
        Itinerary.__route_id += 1

        if isinstance(origin, Place):
            self._origin = origin
        else:
            raise TypeError("L'origine doit être un objet Place")

        if isinstance(destination, Place):
            self._destination = destination
        else:
            raise TypeError("La destination doit être un objet Place")

        # Par défaut, la date prise pour la recherche d'itinéraire est "Maintenant"
        if date is None:
            self._date = datetime.now()
        elif isinstance(date, datetime):
            self._date = date
        else:
            raise TypeError("La valeur attendue de la date doit être de type datetime.")

        if transit_mode_type in Itinerary.__TRANSIT_MODE_TYPES or transit_mode_type is None  or Itinerary.__UBER_MODE_TYPES:
            self._transit_mode_type = transit_mode_type
        elif isinstance(transit_mode_type, str):
            raise ValueError(
                "La valeur du type de transport en commun doit faire partie de la liste des valeurs possibles")
        else:
            raise TypeError(
                "La valeur d'un type de transport en commun doit être une chaine de caractères parmi la liste des "
                "valeurs possible.")

        if isinstance(itinerary_index, int):
            self._itinerary_index = itinerary_index
        else:
            raise TypeError("Un entier est attendu pour l'indice de l'itinéraire")

        # Valeur par défaut
        self._transport_mode = ""
        self._total_duration = 0
        self._walking_duration = 0
        self._walking_distance = 0
        self._bicycling_duration = 0
        self._bicycling_distance = 0
        self._driving_duration = 0
        self._driving_distance = 0
        self._transit_duration = 0
        self._information_legs = []
        self._total_polyline = ""
        self.price = 0 

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
            raise TypeError("Une variable de type Place est attendue pour désigner l'origine.")

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, value):
        if isinstance(value, Place):
            self._destination = value
        else:
            raise TypeError("Une variable de type Place est attendue pour désigner la destination.")

    @property
    def transport_mode(self):
        return self._transport_mode

    @transport_mode.setter
    def transport_mode(self, value):
        if value in Itinerary.__TRANSPORT_MODES:
            self._transport_mode = value
        elif not isinstance(value, str):
            raise TypeError("Est attendue une chaine de caractère pour le mode de transport.")
        else:
            raise ValueError("La valeur en entrée n'est pas un type de transport possible.")

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if isinstance(value, datetime):
            self._date = value
        else:
            raise TypeError("Une variable de type datetime est attendue pour désigner la date de la recherche.")

    @property
    def transit_mode_type(self):
        return self._transit_mode_type

    @transit_mode_type.setter
    def transit_mode_type(self, value):
        if value in Itinerary.__TRANSIT_MODE_TYPES or Itinerary.__UBER_MODE_TYPES:
            self._transit_mode_type = value
        elif not isinstance(value, str):
            raise TypeError("Est attendue une chaine de caractère pour le type de mode de transport en commun.")
        else:
            raise ValueError("La valeur en entrée n'est pas un type de transport en commun possible.")

    @property
    def itinerary_index(self):
        return self._itinerary_index

    @itinerary_index.setter
    def itinerary_index(self, value):
        if isinstance(value, int):
            self._itinerary_index = value
        else:
            raise TypeError("L'indice de l'itinéraire est un entier.")

    @property
    def total_duration(self):
        return self._total_duration

    @total_duration.setter
    def total_duration(self, value):
        if isinstance(value, int):
            self._total_duration = value
        else:
            raise TypeError("Une durée s'exprime en entier (Nombre de secondes)")

    @property
    def walking_duration(self):
        return self._walking_duration

    @walking_duration.setter
    def walking_duration(self, value):
        if isinstance(value, int):
            self._walking_duration = value
        else:
            raise TypeError("Une durée s'exprime en entier (Nombre de secondes)")

    @property
    def walking_distance(self):
        return self._walking_distance

    @walking_distance.setter
    def walking_distance(self, value):
        if isinstance(value, int):
            self._walking_distance = value
        else:
            raise TypeError("Une distance s'exprime en entier (Nombre de mètres)")

    @property
    def bicycling_duration(self):
        return self._bicycling_duration

    @bicycling_duration.setter
    def bicycling_duration(self, value):
        if isinstance(value, int):
            self._bicycling_duration = value
        else:
            raise TypeError("Une durée s'exprime en entier (Nombre de secondes)")

    @property
    def bicycling_distance(self):
        return self._bicycling_distance

    @bicycling_distance.setter
    def bicycling_distance(self, value):
        if isinstance(value, int):
            self._bicycling_distance = value
        else:
            raise TypeError("Une distance s'exprime en entier (Nombre de mètres)")

    @property
    def transit_duration(self):
        return self._transit_duration

    @transit_duration.setter
    def transit_duration(self, value):
        if isinstance(value, int):
            self._transit_duration = value
        else:
            raise TypeError("Une durée s'exprime en entier (Nombre de secondes)")

    @property
    def driving_duration(self):
        return self._driving_duration

    @driving_duration.setter
    def driving_duration(self, value):
        if isinstance(value, int):
            self._driving_duration = value
        else:
            raise TypeError("Une durée s'exprime en entier (Nombre de secondes)")

    @property
    def driving_distance(self):
        return self._driving_distance

    @driving_distance.setter
    def driving_distance(self, value):
        if isinstance(value, int):
            self._driving_distance = value
        else:
            raise TypeError("Une distance s'exprime en entier (Nombre de mètres)")

    @property
    def total_polyline(self):
        return self._total_polyline

    @total_polyline.setter
    def total_polyline(self, value):
        if isinstance(value, str):
            self._total_polyline = value
        else:
            raise TypeError("Une polyline est une chaine de caractère")

    @property
    def information_legs(self):
        return self._information_legs

    @information_legs.setter
    def information_legs(self, value):
        if isinstance(value, list):
            self._information_legs = value
        else:
            raise TypeError("Une distance s'exprime en entier (Nombre de mètres)")

    def __str__(self):
        res = "Itinéraire de {} à {}, ".format(self.origin, self.destination)
        res += " en utilisant le mode de transport suivant : {}, le{}.".format(self._transport_mode, self.date)
        return res

    # TODO indiquer le type de transit (bus, train, tram, subway) dans le repr
    def __repr__(self):
        res = ""
        res += "Your itinerary will take place in  {} step(s) :".format(len(self.information_legs))

        for leg_index, leg in enumerate(self.information_legs):
            res += "\n"
            res += "Portion " + str(leg_index)
            if leg['transport_mode'] != 'TRANSIT':
                res += ": You will be " + leg['transport_mode']
            else:
                res += ": You will be taking the " + leg['instructions'] + " on line " + leg['line']
            res += " for a duration of " + str(math.floor(leg['duration'] / 60 + 1)) + " min"
            if leg['transport_mode'] != 'TRANSIT':
                res += " - " + leg['instructions']
                res += " for a distance of " + str(math.floor(leg['distance'] / 100 + 1) / 10) + " km"
            if leg['transport_mode'] == 'TRANSIT':
                res += " - You will depart from " + leg['departure_stop'] + " and arrive at " + leg['arrival_stop']


        res += "\nIt will take " + str(math.floor(self.total_duration / 60 + 1))
        res += " min, " + str(math.floor(self.walking_duration / 60 + 1)) + " min walking ("
        res += str(math.floor(self.walking_distance / 100 + 1) / 10) + " km)."
        res += "\n"

        return res


class QueryLimit(Exception):
    """Error raised when the query limit is reached"""
    pass


class BadRequest(Exception):
    """The request is not working properly."""
    pass


if __name__ == "__main__":
    """Script de test"""

    # Test des itinéraires
    org = Place(address="Opéra,Paris")
    des = Place(address="Bastille,Paris")
    AtoB = Itinerary(org, des)
    print(repr(AtoB))
