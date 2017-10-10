from datetime import datetime as dt


# To do
# tests

class User:
    """Désigne un utilisateur du service, avec son type et son historique des recherches d'itinéraires"""

    user_id = 1
    TYPES = ["Défaut", "PMR", "Touriste", "Cadre"]  # Liste des types d'utilisateur possibles

    def __init__(self):
        self._id = User.user_id
        User.user_id += 1

        self._type = "Défaut"
        self._itineraries = []

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if value in User.TYPES:
            self._type = value
        else:
            ValueError("La valeur en entrée n'est pas définie comme type possible.")

    @property
    def itineraries(self):
        return self._itineraries

    @itineraries.setter
    def itineraries(self, value):
        self._itineraries = value

    def nouvel_itineraire(self, origin, destination, date=None):
        itineraire = Itineraire(origin, destination, date)
        self.itineraries.append(itineraire)


class Itineraire:
    """Désigne un ensemble de routes possibles entre deux points pour un utilisateur"""

    itineraire_id = 1

    def __init__(self, origin, destination, date=None):
        self._id = Itineraire.itineraire_id
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
        self._origin = value

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, value):
        self._destination = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def routes(self):
        return self._routes

    @routes.setter
    def routes(self, value):
        self._routes = value


class Route:
    """Désigne un trajet entre deux points spécifiés dans l'itinéraire"""

    TRANSPORT_MODES = ["walking", "driving"]  # Liste des modes de transport possibles
    route_id = 1

    def __init__(self, origin, destination, transport_mode, date=None):
        self._id = Route.route_id
        Route.route_id += 1

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
        if value in Route.TRANSPORT_MODES:
            self._transport_mode = value
        else:
            ValueError("La valeur en entrée n'est pas un type de transport possible.")


class Lieu:
    """Désigne un lieu géographique"""

    def __init__(self, adresse=None, lat=None, long=None):
        # Cas où le lieu est ma spécifié
        if adresse is None and (lat is None or long is None):
            pass
            # Exception à créer ici
        self._adresse = adresse
        self._lat = lat
        self._lont = long

    @property
    def adresse(self):
        return self._adresse

    @adresse.setter
    def adresse(self, value):
        self._adresse = value

    @property
    def lat(self):
        return self.lat

    @property
    def long(self):
        return self.long

    def lat_long_from_adresse(self):
        # to do
        print("à faire")


if __name__ == "__main__":
    """Script de test de la bonne construction des classes"""
    Mathieu = User()
    print("ID de Mathieu : " + str(Mathieu.id))
    Mathieu.type = "Touriste"
    print("Type de Mathieu : " + Mathieu.type)
