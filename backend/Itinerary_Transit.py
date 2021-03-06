#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests

from backend.Itinerary import BadRequest
from backend.Itinerary import Itinerary
from backend.Itinerary import QueryLimit
from backend.Place import Place


class Transit(Itinerary):
    """Désigne un itinéraire utilisant les transports en commun"""

    __URL_API_DIRECTION_TRANSIT = 'https://maps.googleapis.com/maps/api/directions/json?&key=AIzaSyATrZmC9' \
                                  '-XjaEAdwtPw6RG0QWV65dbywe0&mode=transit&alternatives=true '

    def __init__(self, origin, destination, date=None, transit_mode_type=None, itinerary_index=0):
        Itinerary.__init__(self, origin, destination, date, transit_mode_type, itinerary_index)
        self.transport_mode = "transit"
        if self.transit_mode_type is None:
            self.transit_mode_type = "bus|rail"

        url_request = Transit.__URL_API_DIRECTION_TRANSIT
        url_request += "&origin=" + str(self.origin.lat) + "," + str(self.origin.lng)
        url_request += "&destination=" + str(self.destination.lat) + "," + str(self.destination.lng)
        url_request += "&transit_mode=" + str(self.transit_mode_type)

        r = requests.get(url_request)
        if r.status_code != 200:
            raise BadRequest(r.status_code)
        else:
            raw_data = r.json()
            if raw_data['status'] == "OVER_QUERY_LIMIT":
                raise QueryLimit("Can't retieve any data from API (Transit)")
            else:
                steps = raw_data['routes'][self.itinerary_index]['legs'][0]['steps']

                self.total_duration = raw_data['routes'][self.itinerary_index]['legs'][0]['duration']['value']
                self.total_polyline = [raw_data['routes'][self.itinerary_index]['overview_polyline']['points']]

                self.walking_distance = 0
                self.walking_duration = 0
                self.transit_duration = 0

                self.information_legs = []
                # Parcours des étapes trouvées de notre trajet
                # pour remplir notre liste de stockage self.information_legs
                for step_number, step in enumerate(steps):
                    self.information_legs.append({})
                    self.information_legs[step_number]['transport_mode'] = step['travel_mode']
                    self.information_legs[step_number]['distance'] = step['distance']['value']
                    self.information_legs[step_number]['interim_destination'] = Place(lat=step['end_location']['lat'],
                                                                                      lng=step['end_location']['lng'])
                    self.information_legs[step_number]['duration'] = step['duration']['value']
                    self.information_legs[step_number]['interim_start'] = Place(lat=step['start_location']['lat'],
                                                                                lng=step['start_location']['lng'])
                    self.information_legs[step_number]['instructions'] = step['html_instructions']
                    if self.information_legs[step_number]['transport_mode'] == "TRANSIT":
                        self.information_legs[step_number]['arrival_stop'] = step['transit_details']['arrival_stop'][
                            'name']
                        self.information_legs[step_number]['departure_stop'] = \
                            step['transit_details']['departure_stop']['name']
                        self.information_legs[step_number]['transit_mode'] = step['transit_details']['line']['vehicle'][
                            'type']
                        if 'short_name' in step['transit_details']['line'].keys():
                            self.information_legs[step_number]['line'] = step['transit_details']['line']['short_name']
                        else:
                            self.information_legs[step_number]['line'] = step['transit_details']['line']['name']
                        self.information_legs[step_number]['number_stops'] = step['transit_details']['num_stops']
                        self.information_legs[step_number]['duration'] = step['duration']['value']
                        self.transit_duration += step['duration']['value']
                    if self.information_legs[step_number]['transport_mode'] == "WALKING":
                        self.walking_distance += step['distance']['value']
                        self.walking_duration += step['duration']['value']


if __name__ == "__main__":
    """Script de test de la bonne construction des classes"""

    # Test des différentes portions d'une voyage en transport de commun
    org = Place(address="79 Avenue de la république 75011, Paris")
    des = Place(address="La Muette, Paris")
    AtoB = Transit(org, des, transit_mode_type="bus")
    print(repr(AtoB))

    org = Place(address="Montmartre, Paris")
    des = Place(address="Cité Universitaire, Paris")
    CtoD = Transit(org, des, transit_mode_type="bus")
    print(repr(CtoD))

    org = Place(address="10 rue oswaldo cruz paris 75016")
    des = Place(address="2 Avenue Mozart 75016 Paris")
    EtoF = Transit(org, des, transit_mode_type="bus|rail")
    print(repr(EtoF))
