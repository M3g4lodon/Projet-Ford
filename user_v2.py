from datetime import datetime as dt


# import ItinerarySearch


class User:
    """Désigne un utilisateur du service, avec son type et son historique des recherches d'itinéraires"""

    user_id = 1
    __TYPES = {"Défaut": ["transit", "walking", "velib", "autolib", "driving"],
               "PMR": ["'transit'&transit_mode='bus'", "walking", "autolib", "driving"],
               "Touriste": ["'transit'&transit_mode='bus'", "velib", "transit", "walking"],
               "Cadre": ["driving", "walking"],
               "Personnalisé": []}  # Liste des types d'utilisateur possibles

    def __init__(self, type="Défaut", permis="non", meteo="oui", charge="non"):
        self._id = User.user_id
        User.user_id += 1

        self._type = type
        self._permis = permis
        self._meteo = meteo
        self._charge = charge
        self._search_history = []
        self._preferences = self.set_preferences()

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if value in User.__TYPES.keys():
            self._type = value.keys()
        elif isinstance(value, str):
            raise TypeError("Est attendue une chaine de caractère pour le type.")
        else:
            raise ValueError("La valeur en entrée n'est pas définie comme type possible.")

    @property
    def preferences(self):
        return self._preferences

    @preferences.setter
    def preferences(self, value):
        self._preferences = value

    @property
    def search_history(self):
        return self._search_history

    @search_history.setter
    def search_history(self, value):
        self._search_history = value

    def new_itinerary(self, origin, destination, date=None):
        itinerary = ItinerarySearch(origin, destination, date)
        self.search_history.append(itinerary)

    def set_preferences(self):
        liste_base = User.__TYPES[self.type]
        if self._permis == "non":
            liste_base.remove('autolib')
        if self._meteo == "oui":
            pass  # besoin de définir l'action s'il fait moche
        if (self._charge == "oui") and ("'transit'&transit_mode='bus'" not in liste_base) and (self.type != "cadre"):
            liste_base.insert(0, "'transit'&transit_mode='bus'")
        return liste_base


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
    # paris = Place(address="Paris")
    # gif = Place(address="Gif")
    # mathieu.new_itinerary(paris, gif)
