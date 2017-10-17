from datetime import datetime as dt
import ItinerarySearch


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