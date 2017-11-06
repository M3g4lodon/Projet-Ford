#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import timedelta

import requests

from Itinerary import BadRequest
from Itinerary import Itinerary
from Itinerary_Bicycling import Bicycling
from Itinerary_Walking import Walking
from Place import Place


class Velib(Itinerary):
    __URL_VELIB = 'https://opendata.paris.fr/api/records/1.0/search/'
    __PARAMETERS = "dataset=stations-velib-disponibilites-en-temps-reel&q=status%3D%3D%22open%22+AND+available_bikes" \
                   "%3E0 "
    __COMMUTING_DURATION = 60  # La durée de correspondance

    def __init__(self, origin, destination, date=None, transit_mode_type=None, itinerary_index=0):

        Itinerary.__init__(self, origin, destination, date, transit_mode_type, itinerary_index)
        self.transport_mode = "velib"
        #prix velib de base - beaucoup de segmentation clients pour les tarifs...
        self.price = "For 1,70€, the 1 day ticket gives you access to Velib' for 24h with the first 30min free of charge. Additional fares apply afterwards."
        # Station velib d'origine
        stop = True
        search_size = 1
        while stop:
            parameters = Velib.__PARAMETERS + "&geofilter.distance=" + "%2C".join(
                [str(self.origin.lat), str(self.origin.lng), str(search_size * 100)])
            r = requests.get(Velib.__URL_VELIB, parameters)
            if r.status_code != 200:
                raise BadRequest(r.status_code)
            else:
                raw_data = r.json()
                search_size += 1
                stations_origin = []
                possible_stations = raw_data['records']
                for possible_station in possible_stations:
                    available_bike = possible_station['fields']['available_bikes']
                    if available_bike == 0:
                        pass
                    else:
                        stop = False
                        stations_origin.append({})
                        stations_origin[-1]['station_address'] = Place(address=possible_station['fields']['address'],
                                                                       lat=possible_station['fields']['position'][0],
                                                                       lng=possible_station['fields']['position'][1])
                        stations_origin[-1]['nb_bike'] = available_bike

        fastest_path_origin = Walking(origin, stations_origin[0]['station_address'], date=self.date)
        for station in stations_origin:
            walk = Walking(origin, station['station_address'], date=self.date)
            if walk.total_duration < fastest_path_origin.total_duration:
                fastest_path_origin = walk

        # station velib à l'arrivée
        stop = True
        search_size = 1
        while stop:
            parameters = Velib.__PARAMETERS + "&geofilter.distance=" + "%2C".join(
                [str(self.destination.lat), str(self.destination.lng), str(search_size * 1000)])
            r = requests.get(Velib.__URL_VELIB, parameters)
            if r.status_code != 200:
                raise BadRequest(r.status_code)
            else:
                raw_data = r.json()
                search_size += 1
                stations_destination = []
                possible_stations = raw_data['records']
                for possible_station in possible_stations:
                    empty_slots = possible_station['fields']['available_bike_stands']
                    if empty_slots == 0:
                        pass
                    else:
                        stop = False
                        stations_destination.append({})
                        stations_destination[-1]['station_address'] = Place(
                            address=possible_station['fields']['address'],
                            lat=possible_station['fields']['position'][0],
                            lng=possible_station['fields']['position'][1])

                        stations_destination[-1]['empty_slots'] = empty_slots

        fastest_path_destination = Walking(stations_destination[0]['station_address'], destination)
        for station in stations_destination:
            walk = Walking(station['station_address'], destination)
            if walk.total_duration < fastest_path_destination.total_duration:
                fastest_path_destination = walk

        # trajet en velib

        start_date_velib = self.date + timedelta(0, fastest_path_origin.total_duration + Velib.__COMMUTING_DURATION)
        velib = Bicycling(fastest_path_origin.destination, fastest_path_destination.origin, date=start_date_velib)

        # Prise en compte du temps pour la dernière étape (station d'arrivée velib à destination)
        start_date_last_leg = start_date_velib + timedelta(0, velib.total_duration + Velib.__COMMUTING_DURATION)
        fastest_path_destination = Walking(fastest_path_destination.origin, self.destination, date=start_date_last_leg)

        # Itineraire total = fastest_path_origin + velib + fastest_path_destination

        self.total_duration = fastest_path_origin.total_duration \
                              + velib.total_duration \
                              + fastest_path_destination.total_duration
        self.walking_duration = fastest_path_origin.walking_duration \
                                + velib.walking_duration \
                                + fastest_path_destination.walking_duration
        self.walking_distance = fastest_path_origin.walking_distance \
                                + velib.walking_distance \
                                + fastest_path_destination.walking_distance
        self.transit_duration = fastest_path_origin.transit_duration \
                                + velib.transit_duration \
                                + fastest_path_destination.transit_duration
        self.velib_duration = velib.bicycling_duration
        self.velib_distance = velib.bicycling_distance
        self.total_polyline = fastest_path_origin.total_polyline \
                              + "\\" + velib.total_polyline \
                              + "\\" + fastest_path_destination.total_polyline
        self.information_legs = fastest_path_origin.information_legs \
                                + velib.information_legs \
                                + fastest_path_destination.information_legs


if __name__ == "__main__":
    # Test des différentes portions d'une voyage en velib

    org = Place(address="Montmartre, Paris")
    des = Place(address="Cité Universitaire, Paris")
    CtoD = Velib(org, des)
    print(repr(CtoD))
