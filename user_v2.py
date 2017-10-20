class User:
    """Désigne un utilisateur du service, avec son type et son historique des recherches d'itinéraires"""

    user_id = 1
    __TYPES = {"Défaut": ["transit", "walking", "velib", "autolib", "driving"],
               "PMR": ["'transit'&transit_mode='bus'", "walking", "autolib", "driving"],
               "Touriste": ["'transit'&transit_mode='bus'", "velib", "transit", "walking"],
               "Cadre": ["driving", "walking"],
               "Personnalisé": []}  # Liste des types d'utilisateur possibles

    def __init__(self, type="Défaut", permis="non"):
        self._id = User.user_id
        User.user_id += 1

        self._type = type
        self._permis = permis
        self._meteo = "non"
        self._charge = "non"
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
        elif not isinstance(value, str):
            raise TypeError("Est attendue une chaine de caractère pour le type.")
        else:
            raise ValueError("La valeur entrée n'est pas définie comme type possible.")


    @property
    def search_history(self):
        return self._search_history

    @search_history.setter
    def search_history(self, value):
        self._search_history = value


    @property
    def preferences(self):
        return self._preferences

    @preferences.setter
    def preferences(self, value):
        self._preferences = value

    def set_preferences(self):
        liste_base = list(User.__TYPES[self._type])
        if self._type == "Personnalisé":
            print("Classez par ordre de préférence les modes de transport que vous souhaitez utiliser parmi les suivants:\ntransit, walking, velib, autolib, driving")
            i=0
            while i<5:
                choix=str(input('choix [{}]: '.format(i+1))).lower()
                while choix not in User.__TYPES['Défaut'] or choix in liste_base:
                    print("Désolé le mode de transport demandé n'est pas référencé ou a déjà été choisi. \nVous pouvez choisir entre:transit, walking, velib, autolib, driving")
                    choix=str(input('choix [{}]: '.format(i+1))).lower()
                liste_base.append(choix)
                i+=1

        if self._permis == "non":
            if 'autolib' in liste_base:
                liste_base.remove('autolib')

        return liste_base

    def __str__(self):
        return "\nUtilisateur n°{}, de type {}. Son historique comporte {} recherche(s).\n".format(self._id,self._type,len(self._search_history))

if __name__ == "__main__":
    """Script de test de la bonne construction des classes"""

    # Test des utilisateurs
    charles = User("Touriste","non")
    print(charles)

    mathieu = User("Personnalisé", "oui")
    print(mathieu.preferences)

