#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from datetime import datetime

from backend.Place import Place


class Itinerary:
    """Gives a route between two specified points in the itinerary search."""

    __TRANSPORT_MODES = ["walking", "driving", "velib", "autolib", "transit", "bicycling", "uber"]

    __TRANSIT_MODE_TYPES = ["bus", "subway", "train", "tram", "rail", "bus|rail"]
    # Liste des modes de transport possibles
    # bus       : bus
    # subway    : subway
    # train     : train
    # tram      : tramway and light subway
    # rail      : subway+train+tram (could be written as subway|train|tram)
    # bus|rail  : all transit mode types !


    __route_id = 1

    def __init__(self, origin, destination, date=None, transit_mode_type=None, itinerary_index=0):

        self._id = Itinerary.__route_id
        Itinerary.__route_id += 1

        # Vérification que les points de départ et d'arrivée sont des objets accetapbles.
        if isinstance(origin, Place):
            self._origin = origin
        else:
            raise TypeError("The origin variable should be an object from the class Place.")

        if isinstance(destination, Place):
            self._destination = destination
        else:
            raise TypeError("The destination variable should be an object from the class Place.")

        # Date: par défaut, la recherche d'itinéraire est "Maintenant"
        if date is None:
            self._date = datetime.now()
        elif isinstance(date, datetime):
            self._date = date
        else:
            raise TypeError("The variable should be the same type as datetime in order to define the search date.")

        # Vérification que le mode de transport est le bon
        if transit_mode_type in Itinerary.__TRANSIT_MODE_TYPES or transit_mode_type is None:
            self._transit_mode_type = transit_mode_type
        elif isinstance(transit_mode_type, str):
            raise ValueError(
                "The transit mode type should be part of the possible values available.")
        else:
            raise TypeError(
                "The transit mode type should be a chain of characters, part of the possible values available.")

        # Vérification du numéro de l'itinéraire
        if isinstance(itinerary_index, int):
            self._itinerary_index = itinerary_index
        else:
            raise TypeError("Expected an integer for the index itinerary.")

        # Valeur par défaut de différents attributs
        self._transport_mode = ""
        self._total_duration = 0
        self._walking_duration = 0
        self._walking_distance = 0
        self._bicycling_duration = 0
        self._bicycling_distance = 0
        self._driving_duration = 0
        self._driving_distance = 0
        self._transit_duration = 0
        self._information_legs = []
        self._total_polyline = []
        self._price = None

    #
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
            raise TypeError("The origin variable should be an object from the class Place.")

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, value):
        if isinstance(value, Place):
            self._destination = value
        else:
            raise TypeError("The destination variable should be an object from the class Place.")

    @property
    def transport_mode(self):
        return self._transport_mode

    @transport_mode.setter
    def transport_mode(self, value):
        if value in Itinerary.__TRANSPORT_MODES:
            self._transport_mode = value
        elif not isinstance(value, str):
            raise TypeError("Was expecting a chain of characters for the transport mode.")
        else:
            raise ValueError("The value entered is not an available transport mode.")

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if isinstance(value, datetime):
            self._date = value
        else:
            raise TypeError("The variable should be the same type as datetime in order to define the search date.")

    @property
    def transit_mode_type(self):
        return self._transit_mode_type

    @transit_mode_type.setter
    def transit_mode_type(self, value):
        if value in Itinerary.__TRANSIT_MODE_TYPES:
            self._transit_mode_type = value
        elif not isinstance(value, str):
            raise TypeError("Was expecting a chain of characters for the transport mode type.")
        else:
            raise ValueError("The value entered is not an available transport mode type.")

    @property
    def itinerary_index(self):
        return self._itinerary_index

    @itinerary_index.setter
    def itinerary_index(self, value):
        if isinstance(value, int):
            self._itinerary_index = value
        else:
            raise TypeError("L'indice de l'itinéraire est un entier.")

    @property
    def total_duration(self):
        return self._total_duration

    @total_duration.setter
    def total_duration(self, value):
        if isinstance(value, int):
            self._total_duration = value
        else:
            raise TypeError("A duration is an integer (in seconds).")

    @property
    def walking_duration(self):
        return self._walking_duration

    @walking_duration.setter
    def walking_duration(self, value):
        if isinstance(value, int):
            self._walking_duration = value
        else:
            raise TypeError("A duration is an integer (in seconds).")

    @property
    def walking_distance(self):
        return self._walking_distance

    @walking_distance.setter
    def walking_distance(self, value):
        if isinstance(value, int):
            self._walking_distance = value
        else:
            raise TypeError("A distance is an integer (in meters).")

    @property
    def bicycling_duration(self):
        return self._bicycling_duration

    @bicycling_duration.setter
    def bicycling_duration(self, value):
        if isinstance(value, int):
            self._bicycling_duration = value
        else:
            raise TypeError("A duration is an integer (in seconds).")

    @property
    def bicycling_distance(self):
        return self._bicycling_distance

    @bicycling_distance.setter
    def bicycling_distance(self, value):
        if isinstance(value, int):
            self._bicycling_distance = value
        else:
            raise TypeError("A distance is an integer (in meters).")

    @property
    def transit_duration(self):
        return self._transit_duration

    @transit_duration.setter
    def transit_duration(self, value):
        if isinstance(value, int):
            self._transit_duration = value
        else:
            raise TypeError("A duration is an integer (in seconds).")

    @property
    def driving_duration(self):
        return self._driving_duration

    @driving_duration.setter
    def driving_duration(self, value):
        if isinstance(value, int):
            self._driving_duration = value
        else:
            raise TypeError("A duration is an integer (in seconds).")

    @property
    def driving_distance(self):
        return self._driving_distance

    @driving_distance.setter
    def driving_distance(self, value):
        if isinstance(value, int):
            self._driving_distance = value
        else:
            raise TypeError("A distance is an integer (in meters).")

    @property
    def total_polyline(self):
        return self._total_polyline

    @total_polyline.setter
    def total_polyline(self, value):
        if isinstance(value, list):
            self._total_polyline = value
        else:
            raise TypeError("A polyline is a list of strings.")

    @property
    def information_legs(self):
        return self._information_legs

    @information_legs.setter
    def information_legs(self, value):
        if isinstance(value, list):
            self._information_legs = value
        else:
            raise TypeError("A distance is an integer (in meters).")

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    def __str__(self):
        '''Return an overview of your trip with must-know details.'''
        res = "Itinerary departs from {} and arrives at {}, ".format(self.origin, self.destination)
        res += " using the following transport mode : {}, on the {}.".format(self._transport_mode, self.date)
        return res

    def __repr__(self):
        '''Returns a detailed summary of your trip.'''
        res = ""
        res += "Your itinerary will take place in  {} step(s) :".format(len(self.information_legs))

        for leg_index, leg in enumerate(self.information_legs):
            res += "\n"
            res += "Portion " + str(leg_index+1)
            if leg['transport_mode'] != 'TRANSIT':
                res += ": You will be " + leg['transport_mode']
            else:
                res += ": You will be taking the " + leg['instructions'] + " on line " + leg['line']
            res += " for a duration of " + Itinerary.time_formatted(leg['duration'])
            if leg['transport_mode'] != 'TRANSIT':
                res += " - " + leg['instructions']
                res += " for a distance of " + Itinerary.dist_formatted(leg['distance'])
            if leg['transport_mode'] == 'TRANSIT':
                res += " - You will depart from " + leg['departure_stop'] + " and arrive at " + leg['arrival_stop']

        res += "\nIt will take " + Itinerary.time_formatted(self.total_duration) + ", "
        res += Itinerary.time_formatted(self.walking_duration) + " walking ("
        res += Itinerary.dist_formatted(self.walking_distance) + ")."
        res += "\n"

        return res

    @staticmethod
    def time_formatted(nb_second):
        """Convert a number of second in a formatted string"""
        if nb_second == 0:
            return "0 min"
        else:
            m, s = divmod(nb_second, 60)
            h, m = divmod(m, 60)
            if h == 0:
                return str(m + 1) + " min"
            else:
                return str(h) + " h " + str(m + 1) + " min"

    @staticmethod
    def dist_formatted(nb_meter):
        """Convert a number of meters in a formatted string"""
        if nb_meter == 0:
            return "0 km"
        else:
            return str(math.floor(nb_meter / 100 + 1) / 10) + " km"


class QueryLimit(Exception):
    """Error raised when the query limit is reached"""
    pass


class BadRequest(Exception):
    """The request is not working properly."""
    pass


if __name__ == "__main__":
    """Script de test"""

    # Test des itinéraires
    org = Place(address="Opéra,Paris")
    des = Place(address="Bastille,Paris")
    AtoB = Itinerary(org, des)
    print(repr(AtoB))
