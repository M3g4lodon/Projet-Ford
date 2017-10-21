from datetime import datetime
from Place import Place


class Itinerary:
    """Désigne un trajet entre deux points spécifiés dans la recherche d'itinéraires"""

    __TRANSPORT_MODES = ["walking", "driving", "velib", "autolib", "transit","bicycling"]
    __TRANSIT_MODE_TYPES = ["rail", "bus", "tramway"]  # Liste des modes de transport possibles
    __route_id = 1

    def __init__(self, origin, destination, transport_mode, date=None, transit_mode_type=None, itinerary_index=0):

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

        if transport_mode in Itinerary.__TRANSPORT_MODES:
            self._tranport_mode = transport_mode
        elif isinstance(transport_mode, str):
            raise ValueError("La valeur du mode de transport doit faire partie de la liste des valeurs possibles")
        else:
            raise TypeError("La valeur d'un mode de transport doit être une chaine de caractères parmi la liste des "
                            "modes de transport possible.")

            # Par défaut, la date prise pour la recherche d'itinéraire est "Maintenant"
        if date is None:
            self._date = datetime.now()
        elif isinstance(date, datetime):
            self._date = date
        else:
            raise TypeError("La valeur attendue de la date doit être de type datetime.")

        if transit_mode_type in Itinerary.__TRANSIT_MODE_TYPES or transit_mode_type is None:
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
        return self._tranport_mode

    @transport_mode.setter
    def transport_mode(self, value):
        if value in Itinerary.__TRANSPORT_MODES:
            self._tranport_mode = value
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
        if value in Itinerary.__TRANSIT_MODE_TYPES:
            self.transit_mode_type = value
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

    def __str__(self):
        res = "Itinéraire de {} à {}, ".format(self.origin, self.destination)
        res += " en utilisant le mode de transport suivant {}, le{}.".format(self.transport_mode, self.date)
        return res


if __name__ == "__main__":
    """Script de test"""

    # Test des itinéraires
    org = Place(address="Opéra,Paris")
    des = Place(address="Bastille,Paris")
    AtoB = Itinerary(org, des, "walking")
    print(AtoB)
