#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import requests


class User:
    """Désigne un utilisateur du service, avec son type et son historique des recherches d'itinéraires"""

    __user_id = 1
    __TYPES = {"Défaut": ["transit", "walking", "velib", "autolib", "driving", "uber"],
               "PMR": ["bus", "walking", "autolib", "driving", "uber"],
               "Touriste": ["bus", "velib", "transit", "walking", "uber"],
               "Cadre": ["driving", "walking", "uber"],
               "Personnalisé": []}  # Liste des types d'utilisateur possibles

    def __init__(self, user_type="Défaut", driving_license=False, weather=True, loaded=False):
        self._id = User.__user_id
        User.__user_id += 1

        self._type = user_type
        self._driving_license = driving_license
        self._weather = weather
        self._loaded = loaded
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
    def driving_license(self):
        return self._driving_license

    @driving_license.setter
    def driving_license(self, value):
        if isinstance(value, bool):
            self._driving_license = value
            if self._driving_license == False :
                if 'autolib' in self._preferences:
                    self._preferences.remove('autolib')
                if 'driving' in self._preferences:
                    self._preferences.remove('driving')
        else:
            raise TypeError("Est attendu un booléen pour la détente ou non du permis.")


    @property
    def weather(self):
        return self._weather

    @weather.setter
    def weather(self, value):
        if isinstance(value, bool):
            self._weather = value
            if self._weather == True:
                resultat=self.preferences_with_weather(datetime.date.today())
                if resultat[1]== False:
                    if 'velib' in self._preferences:
                        self._preferences.remove('velib')
                    if 'walking' in self._preferences:
                        self._preferences.remove('walking')
        else:
            raise TypeError("Est attendu un booléen pour la météo.")

    @property
    def loaded(self):
        return self._loaded

    @loaded.setter
    def loaded(self, value):
        if isinstance(value, bool):
            self._loaded = value
            if self._loaded == True:
                self.preferences_if_loaded()

        else:
            raise TypeError("Est attendu un booléen pour savoir si la personne est chargé ou non.")

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
        preferences = list(User.__TYPES[self._type])
        if self.type == "Personnalisé":
            print("Classez par ordre de préférence les modes de transport que vous souhaitez utiliser parmi les "
                  "suivants:\ntransit, walking, velib, autolib, driving")
            i = 0
            while i < 5:
                choix = str(input('choix [{}]: '.format(i + 1))).lower()
                while choix not in User.__TYPES['Défaut'] or choix in preferences:
                    print(
                        "Désolé le mode de transport demandé n'est pas référencé ou a déjà été choisi. \nVous pouvez "
                        "choisir entre:transit, walking, velib, autolib, driving")
                    choix = str(input('choix [{}]: '.format(i + 1))).lower()
                preferences.append(choix)
                i += 1

        if self.driving_license == False:
            if 'autolib' in preferences:
                preferences.remove('autolib')
            if 'driving' in preferences:
                preferences.remove('driving')

        return preferences

    def preferences_with_weather(self, date):
        # 5 days forecast incl. temperature, weather,...
        url = "https://query.yahooapis.com/v1/public/yql"
        param = "q=select%20*%20from%20weather.forecast%20where%20woeid%20%3D615702%20and%20u%3D'c'&format=json" \
                "&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback= "

        resp = requests.get(url, param)
        r = resp.json()

        for i in range(0, 4):
            if date == datetime.date.today() + datetime.timedelta(days=i):
                forecast = r['query']['results']['channel']['item']['forecast'][i]
                # print(forecast)

                code = int(forecast['code'])
                texte = forecast['text']
                max_temp = forecast['high']
                min_temp = forecast['low']
                info = "Le temps sera: {}, la température comprise entre {} et {}°C.".format(texte, min_temp, max_temp)

                if 19 <= code <= 34 or code == 36:
                    description = "Tous les moyens de transport sont disponibles ! " + info
                    beau_temps=True
                else:
                    description = "\nUtilisez les moyens de transport couverts. " + info
                    beau_temps =False

                return description, beau_temps

    def preferences_if_loaded(self):
        pref = list(self._preferences)
        if 'velib' in pref:
            pref.remove('velib')
        if 'walking' in pref:
            pref.remove('walking')
        if 'driving' in pref:
            pref.remove('driving')
            pref.insert(0, 'driving')
        if 'autolib' in pref:
            pref.remove('autolib')
            pref.insert(1, 'autolib')
        if 'bus' in pref:
            pref.remove('bus')
        pref.insert(2, 'bus')

        self._preferences = pref

    # manque une fonction pour faire une recherche

    def __str__(self):
        return "\nUtilisateur n°{}, de type {}. Son historique comporte {} recherche(s).\n".format(self.id, self.type,len(self.search_history))


if __name__ == "__main__":
    """Script de test de la bonne construction des classes"""

    # Test des utilisateurs
    charles = User("Touriste", False)
    print(charles)

    mathieu = User("Personnalisé", True)
    print(mathieu.preferences)
    print(mathieu)

