from datetime import datetime as dt
import requests


# To do
# Préférence à rajouter
# Prise en compte des erreurs dans les requêtes rest


class User:
    """Désigne un utilisateur du service, avec son type et son historique des recherches d'itinéraires"""

    user_id = 1
    __TYPES = ["Défaut", "PMR", "Touriste", "Cadre", "Personnalisé"]  # Liste des types d'utilisateur possibles

    def __init__(self):
        self._id = User.user_id
        User.user_id += 1

        self._type = "Défaut"
        self._search_history = []

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if value in User.__TYPES:
            self._type = value
        elif isinstance(value, str):
            raise TypeError("Est attendue une chaine de caractère pour le type.")
        else:
            raise ValueError("La valeur en entrée n'est pas définie comme type possible.")

    @property
    def search_history(self):
        return self._search_history

    @search_history.setter
    def search_history(self, value):
        self._search_history = value

    def new_itinerary(self, origin, destination, date=None):
        itinerary = ItinerarySearch(origin, destination, date)
        self.search_history.append(itinerary)


class ItinerarySearch:
    """Désigne un ensemble de routes possibles entre deux points pour un utilisateur"""

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


class Leg:
    pass


class Place:
    """Désigne un lieu géographique"""

    __URL_API_GEOCODE = "https://maps.googleapis.com/maps/api/geocode/json?&key=AIzaSyDpVNzFcwgFfPJOK25P9NlMBL-YEe8bSow"

    def __init__(self, address=None, lat=None, long=None):
        # Cas où le lieu est ma spécifié
        if address is None and (lat is None or long is None):
            pass
            # Exception à créer ici
        self._address = address
        self._lat = lat
        self._long = long

    @property
    def address(self):
        if self._address is None:
            self.address_from_lat_long()
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def lat(self):
        if self._lat is None:
            self.lat_long_from_address()
        return self._lat

    @lat.setter
    def lat(self, value):
        if isinstance(value, float):
            self._lat = value
        else:
            raise TypeError("Un flottant est attendu pour la latitude")

    @property
    def long(self):
        if self._long is None:
            self.lat_long_from_address()
        return self._long

    @long.setter
    def long(self, value):
        if isinstance(value, float):
            self._long = value
        else:
            raise TypeError("Un flottant est attendu pour la longitude")

    def lat_long_from_address(self):
        """Calcule la latitude et la longitude de l'adresse d'origine"""
        url_request = Place.__URL_API_GEOCODE + "&address=" + self.address
        raw_data = requests.get(url_request).json()
        self.lat = raw_data['results'][0]['geometry']['location']['lat']
        self.long = raw_data['results'][0]['geometry']['location']['lng']

    def address_from_lat_long(self):
        """calcule l'adresse associé à une latitude et une longitude"""
        url_request = Place.__URL_API_GEOCODE + "&latlng=" + str(self.lat) + "," + str(self.long)
        raw_data = requests.get(url_request).json()
        self.address = raw_data['results'][0]['formatted_address']

    def __repr__(self):
        res = ""
        if self.address is not None:
            res += "[Place] Address : " + self.address + "\n"
        if not (self.lat is None or self.long is None):
            res += "[Place] Latitude : " + str(self.lat) + "\n" + "[Place] Longitude : " + str(self.long)
        return res


if __name__ == "__main__":
    """Script de test de la bonne construction des classes"""

    # Test des utilisateurs
    mathieu = User()
    print("ID de Mathieu : " + str(mathieu.id))
    mathieu.type = "Touriste"
    print("Type de Mathieu : " + mathieu.type)
    charles = User()
    # charles.type = "ESCP"
    print("Type de Charles : " + charles.type)
    paris = Place(address="Paris")
    gif = Place(address="Gif")
    mathieu.new_itinerary(paris, gif)

    # Test de la recherche
    # To do

    # Test des Routes
    # To do

    # Test des Legs
    # To do

    # Test des lieux
    paris = Place(address="Paris")
    print(paris)
    print("Pré-demande de coordonnées : " + str(paris))
    paris.lat_long_from_address()
    print("Post-demande de coordonnées : " + str(paris))
    poissonnier = Place(lat=48.896614, long=2.3522219)
    print(poissonnier)
    poissonnier.address_from_lat_long()
    print(poissonnier)
