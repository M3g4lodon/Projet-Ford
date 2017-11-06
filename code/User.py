#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
import requests


class User:
    """Specifies a user, his type and his itinerary search history."""

    __user_id = 1
    __TYPES = {"Default": ["transit", "walking", "velib", "autolib", "driving", "uber"],
               "HANDI": ["bus", "walking", "autolib", "driving", "uber"],
               "Tourist": ["bus", "velib", "transit", "walking", "uber"],
               "Business": ["driving", "walking", "uber"],
               "Customized ": []}  # Liste des types d'utilisateur possibles

    def __init__(self, user_type="Default", driving_license=False):
        self._id = User.__user_id
        User.__user_id += 1

        self._type = user_type
        self._driving_license = driving_license
        self._weather = False
        self._loaded = False
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
            raise TypeError("Was excpeted a chain of characters for the type.")
        else:
            raise ValueError("The given value is not a known possible type.")

    @property
    def driving_license(self):
        return self._driving_license

    @driving_license.setter
    def driving_license(self, value):
        if isinstance(value, bool):
            self._driving_license = value
        else:
            raise TypeError("Was expecting a boolean for the Driver License.")

    @property
    def weather(self):
        return self._weather

    @weather.setter
    def weather(self, value):
        if isinstance(value, bool):
            self._weather = value
        else:
            raise TypeError("Was expecting a boolean for the weather.")

    @property
    def loaded(self):
        return self._loaded

    @loaded.setter
    def loaded(self, value):
        if isinstance(value, bool):
            self._loaded = value
        else:
            raise TypeError("Was expecting a boolean to know if the person is loaded or not.")

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
        if self.type == "Customized":
            print("Class by choice preference transport modes you wish to use among the following options :\ntransit, walking, velib, autolib, driving")
            i = 0
            while i < 5:
                choix = str(input('Choice Number [{}]: '.format(i + 1))).lower()
                while choix not in User.__TYPES['Default'] or choix in liste_base:
                    print(
                        "Sorry, the asked transport mode isn't referenced or has already been selected. \nYou can select "
                        "between: transit, walking, velib, autolib, driving")
                    choix = str(input('choix [{}]: '.format(i + 1))).lower()
                liste_base.append(choix)
                i += 1

        if self.driving_license:
            if 'autolib' in liste_base:
                liste_base.remove('autolib')

        return liste_base

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
                info = "The weather will be: {}, with a high of {}°C and a low of {}°C.".format(texte, max_temp, min_temp)

                if 19 <= code <= 34 or code == 36:
                    resultat = "All available transport modes are good! " + info
                else:
                    resultat = "\nUse rain-free transport modes. " + info
                    pref = list(self.preferences)
                    if 'velib' in pref:
                        pref.remove('velib')
                    if 'walking' in pref:
                        pref.remove('walking')
                    self.preferences = pref

                return resultat

    def preferencse_if_loaded(self):
        pref = list(self.preferences)
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

        self.preferences = pref

    # manque une fonction pour faire une recherche

    def __str__(self):
        return "\nUser Nb {}, type {}. His search history is comprised of {} search(s).\n".format(self.id, self.type,len(self.search_history))


if __name__ == "__main__":
    """Script de test de la bonne construction des classes"""

    # Test des utilisateurs
    charles = User("Tourist", False)
    print(charles)

    mathieu = User("Customized", True)
    print(mathieu.preferences)
    print(mathieu)
