#!/usr/bin/env python
# -*- coding: utf-8 -*-


import math

import requests

from backend.Itinerary import BadRequest
from backend.Itinerary import Itinerary
from backend.Itinerary_Driving import Driving
from backend.Place import Place


class Uber(Itinerary):
    __URL_UBER_PRICE = 'https://api.uber.com/v1.2/estimates/price?'
    __URL_UBER_TIME = 'https://api.uber.com/v1.2/estimates/time?'
    __UBER_MODE_TYPES = ["uberx", "uberpool", "uberberline", "ubergreen", "ubervan", "access"]

    def __init__(self, origin, destination, date=None, uber_type=None, transit_mode_type=None, itinerary_index=0):
        Itinerary.__init__(self, origin, destination, date, transit_mode_type, itinerary_index)
        self.transport_mode = "uber"

        if uber_type in Uber.__UBER_MODE_TYPES:
            self._uber_type = uber_type
        elif isinstance(uber_type, str):
            raise ValueError(
                "The uber type must be a part of the possible uber vehicle options")
        elif uber_type is None:
            self._uber_type = "uberx"
        else:
            raise TypeError(
                "The uber type must be a chain of characters among the possible uber vehicle options available.")

        self._options_uber = []
        self._uber_wait_duration = 0
        self._uber_travel_duration = 0
        self._available_options = []

        # Code Spécifique à l'API UBER
        headers = {'Authorization': 'Token 1QTK0iskAoX7vFZ3Ir1j_NdqnADK7zXAF4GcaRLe', 'Accept-Language': 'en_US',
                   "Content-Type": "application/json"}
        #PRICE API from Uber to get Price information
        url_request_price = Uber.__URL_UBER_PRICE
        url_request_price += 'start_latitude=' + str(self.origin.lat) + '&start_longitude=' + str(
            self.origin.lng) + '&end_latitude=' + str(self.destination.lat) + '&end_longitude=' + str(
            self.destination.lng)
        r_price = requests.get(url=url_request_price, headers=headers)
        
        #TIME API from Uber to get Time information
        url_request_time = Uber.__URL_UBER_TIME
        url_request_time += 'start_latitude=' + str(self.origin.lat) + '&start_longitude=' + str(
            self.origin.lng) + '&end_latitude=' + str(self.destination.lat) + '&end_longitude=' + str(
            self.destination.lng)
        r_time = requests.get(url=url_request_time, headers=headers)

        if r_price.status_code != 200 or r_time.status_code != 200:
            raise BadRequest()
        else:
            raw_data_price = r_price.json()
            raw_data_time = r_time.json()

            options_price = raw_data_price['prices']
            options_time = raw_data_time['times']

            # les estimations temps et prix ne sont pas toujours identiques.
            # On veut prendre l'intersection des deux.
            # D'où la disjonction de cas ...

            if len(options_price) <= len(options_time):

                for uber_option, option in enumerate(options_price):
                    self._options_uber.append({})
                    self._options_uber[-1]['uber_name'] = str(option['display_name']).lower()
                    self._available_options.append(str(option['display_name']).lower())
                    self._options_uber[-1]['price'] = option['estimate']
                    self._options_uber[-1]['distance'] = option['distance']
                    self._options_uber[-1]['duration'] = option['duration']

                    if options_time[uber_option]['display_name'] == option['display_name']:
                        self._options_uber[-1]['wait_time'] = options_time[uber_option]['estimate']

                    if self._options_uber[-1]['uber_name'] == self._uber_type:
                        self.price = self._options_uber[uber_option]['price']
                        self._uber_wait_duration = self._options_uber[uber_option]['wait_time']
                        self._uber_travel_duration = self._options_uber[uber_option]['duration']
                        self.total_duration = self._uber_wait_duration + self._uber_travel_duration
                        self.driving_distance = int(self._options_uber[uber_option][
                                                        'distance'] * 1610)  # l'API renvoie des miles et non des km

            else:
                for uber_option, option in enumerate(options_time):
                    self._options_uber.append({})
                    self._options_uber[-1]['uber_name'] = str(option['display_name']).lower()
                    self._available_options.append(str(option['display_name']).lower())
                    self._options_uber[-1]['wait_time'] = option['estimate']

                    if options_price[uber_option]['display_name'] == option['display_name']:
                        self._options_uber[-1]['price'] = options_price[uber_option]['estimate']
                        self._options_uber[-1]['distance'] = options_price[uber_option]['distance']
                        self._options_uber[-1]['duration'] = options_price[uber_option]['duration']

                    if self._options_uber[-1]['uber_name'] == self._uber_type:
                        self.price = self._options_uber[uber_option]['price']
                        self._uber_wait_duration = self._options_uber[uber_option]['wait_time']
                        self._uber_travel_duration = self._options_uber[uber_option]['duration']
                        self.total_duration = self._uber_wait_duration + self._uber_travel_duration
                        self.driving_distance = int(float(self._options_uber[uber_option][
                                                              'distance']) * 1610)
                        # l'API renvoie des miles et non des km
                self.total_polyline = Driving(origin, destination, date, transit_mode_type,
                                              itinerary_index).total_polyline
            if self._uber_type not in self._available_options:
                TypeError(
                    "The Uber option you selected isn't available. Please select another option or try again later.")

    @property
    def uber_travel_duration(self):
        return self._uber_travel_duration

    @property
    def uber_wait_duration(self):
        return self._uber_wait_duration

    @property
    def available_options(self):
        return self._available_options

    @property
    def uber_type(self):
        return self._uber_type

    @uber_type.setter
    def uber_type(self, value):
        if value in Uber.__UBER_MODE_TYPES:
            self._uber_type = value
        elif not isinstance(value, str):
            raise TypeError("Est attendue une chaine de caractère pour le type d'uber.")
        else:
            raise ValueError("La valeur en entrée n'est pas un type d'uber.")

    @property
    def options_uber(self):
        return self._options_uber

    # J'ai décidé d'override celle de la classe mère, plus facile (on n'utilise pas google maps ici...)
    def __repr__(self):

        res = ""
        res += "Here is the summary of your Uber Trip:"
        res += "\n"
        res += "Your uber will be arriving in " + str(math.floor(self._uber_wait_duration / 60 + 1)) + " min."
        res += "\n"
        res += "Your ride will take you " + str(math.floor(self._uber_travel_duration / 60 + 1)) + " min and " + str(
            self.driving_distance // 1000) + " km " + str(
            self.driving_distance % 1000) + "m to arrive at destination."
        res += "The fare estimate is " + str(self.price) + "."

        return res


if __name__ == "__main__":
    """Script de test"""

    # Test des itinéraires
    org = Place(address="Porte de Passy")
    des = Place(address="Porte de la Villette")
    AtoB = Uber(org, des, uber_type="uberberline")

    print(repr(AtoB))
