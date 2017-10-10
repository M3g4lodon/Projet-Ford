from datetime import datetime as dt


class Utilisateur:
    """Désigne un utilisateur du service"""

    user_id = 1

    def __init__(self):
        self._id = Utilisateur.user_id
        Utilisateur.user_id += 1

        self._type = "Défaut"
        self._itineraires = []


class Itineraire(Utilisateur):
    """Désigne un ensemble de routes possibles entre deux points pour un utilisateur donné"""
    itineraire_id = 1

    def __init__(self, origin, destination, date=None):
        self._id = Itineraire.itineraire_id
        self._origin = origin
        self._destination = destination

        # Par défaut, la date prise pour la recherche d'itinéraire est "Maintenant"
        if date == None:
            self._date = dt.now()
        else:
            self._date = date

        self._routes = []


class Route(Itineraire):
    """Désigne un trajet entre deux points spécifiés dans l'itinéraire père"""

    def __init__(self,transport_mode):
        self._transport_mode=transport_mode


if __name__ == "__main__":
    print ("blublu")
