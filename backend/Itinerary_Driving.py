#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests

from backend.Itinerary import BadRequest
from backend.Itinerary import Itinerary
from backend.Itinerary import QueryLimit
from backend.Place import Place


class Driving(Itinerary):
    __URL_API_DIRECTION = 'https://maps.googleapis.com/maps/api/directions/json?&key=AIzaSyATrZmC9' \
                          '-XjaEAdwtPw6RG0QWV65dbywe0&mode=driving&alternatives=true '

    def __init__(self, origin, destination, date=None, transit_mode_type=None, itinerary_index=0):
        Itinerary.__init__(self, origin, destination, date, transit_mode_type, itinerary_index)
        self.transport_mode = "driving"

        url_request = Driving.__URL_API_DIRECTION
        url_request += "&origin=" + str(self.origin.lat) + "," + str(self.origin.lng)
        url_request += "&destination=" + str(self.destination.lat) + "," + str(self.destination.lng)
        r = requests.get(url_request)

        if r.status_code != 200:
            raise BadRequest(r.status_code)
        else:
            raw_data = r.json()
            if raw_data['status'] == "OVER_QUERY_LIMIT":
                raise QueryLimit("Can't retieve any data from API (Driving)")
            else:
                # on récupère les informations concernant les différentes étapes
                steps = raw_data['routes'][self.itinerary_index]['legs'][0]['steps']

                self.total_duration = raw_data['routes'][self.itinerary_index]['legs'][0]['duration']['value']
                self.total_polyline = [raw_data['routes'][self.itinerary_index]['overview_polyline']['points']]

                self.walking_distance = 0
                self.walking_duration = 0
                self.driving_distance = 0
                self.driving_duration = 0

                self.information_legs = []  # Notre liste stockant nos étapes de trajet

                # Parcours des étapes trouvées de notre trajet pour remplir notre liste de stockage self.information_legs
                for step_number, step in enumerate(steps):
                    self.information_legs.append({})
                    self.information_legs[step_number]['transport_mode'] = step['travel_mode']
                    self.information_legs[step_number]['interim_start'] = Place(lat=step['start_location']['lat'],
                                                                                lng=step['start_location']['lng'])
                    self.information_legs[step_number]['interim_destination'] = Place(lat=step['end_location']['lat'],
                                                                                      lng=step['end_location']['lng'])
                    self.information_legs[step_number]['distance'] = step['distance']['value']
                    self.information_legs[step_number]['duration'] = step['duration']['value']
                    self.information_legs[step_number]['instructions'] = step['html_instructions']

                    if self.information_legs[step_number]['transport_mode'] == "DRIVING":
                        self.driving_distance += step['distance']['value']
                        self.driving_duration += step['duration']['value']
                    else:
                        self.walking_distance += step['distance']['value']
                        self.walking_duration += step['duration']['value']


if __name__ == "__main__":
    """Script de test de la bonne construction des classes"""

    # Test des différentes portions d'une voyage en voiture
    org = Place(address="10 rue oswaldo cruz paris 75016")
    des = Place(address="Favella Chic Paris")
    AtoB = Driving(org, des)
    print(repr(AtoB))

    org = Place(address="Montmartre, Paris")
    des = Place(address="Cité Universitaire, Paris")
    CtoD = Driving(org, des)
    print(repr(CtoD))
