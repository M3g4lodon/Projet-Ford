from Itinerary import Itinerary
from Itinerary_Walking import Walking
from Itinerary_Driving import Driving
from Itinerary_Transit import Transit
from Place import Place
import requests
import math


class Autolib(Itinerary):
    __URL_API_DIRECTION = 'https://maps.googleapis.com/maps/api/directions/json?&key=AIzaSyATrZmC9' \
                          '-XjaEAdwtPw6RG0QWV65dbywe0&mode=transit&alternatives=true '
    __URL_AUTOLIB = 'https://opendata.paris.fr/api/records/1.0/search/'

    def __init__(self, origin, destination, transport_mode, date=None, transit_mode_type=None, itinerary_index=0):
        Itinerary.__init__(self, origin, destination, transport_mode, date, transit_mode_type, itinerary_index)

        # Station autolib d'origine
        stop = True
        search_size = 1
        while stop:
            parameters = "dataset=autolib-disponibilite-temps-reel&q=status%3Dok+AND+cars%3E0&geofilter.distance=" \
                         + "%2C".join([str(origin.lat), str(origin.lng), str(search_size * 1000)])
            r = requests.get(Autolib.__URL_AUTOLIB, parameters)
            raw_data = r.json()
            search_size += 1
            stations_origin = []
            possible_stations = raw_data['records']
            for possible_station in possible_stations:
                if possible_station['fields']['cars'] == 0:
                    pass
                else:
                    stop = False
                    stations_origin.append({})
                    stations_origin[-1]['station_address'] = Place(address=(possible_station['fields']['address']
                                                                            + " "
                                                                            + possible_station['fields']['postal_code']
                                                                            + " Paris"))
                    stations_origin[-1]['nb_auto'] = possible_station['fields']['cars']

        fastest_path_origin = Walking(origin, stations_origin[0]['station_address'], "walking")
        for station in stations_origin:
            walk = Walking(origin, station['station_address'], "walking")
            if walk.total_duration < fastest_path_origin.total_duration:
                fastest_path_origin = walk
            transit = Transit(origin, station['station_address'], "transit",transit_mode_type="bus|rail")

            if transit.total_duration < fastest_path_origin.total_duration:
                fastest_path_origin = transit
        print(fastest_path_origin)

        # station autolib à l'arrivée
        stop = True
        search_size = 1
        while stop:

            parameters = "dataset=autolib-disponibilite-temps-reel&q=status%3Dok+AND+cars%3E0&geofilter.distance=" \
                         + "%2C".join([destination.lat, destination.lng, str(search_size * 1000)])
            r = requests.get(Autolib.__URL_AUTOLIB, parameters)
            raw_data = r.json()
            number_hits = raw_data['nhits']

            stations_destination = []
            for station_index in range(number_hits):
                if raw_data['records'][station_index]['fields']['cars'] == 0:
                    pass
                else:
                    self._address_station_destination = raw_data['records'][station_index]['fields'][
                                                            'address'] + " Paris"  # Je me limite au cas où la station autolib se trouve à Paris et on sélectionne la première uniquement
                    self._nb_auto_destination = raw_data['records'][station_index]['fields']['cars']
                    break
            for station_index in range(number_hits):

                if raw_data['records'][station_index]['fields'][
                    'cars'] == 0:  # faut changer ce paramètre, il faudrait voir si on a accès au nombre de bornes libres
                    pass
                else:
                    stations_destination.append({})
                    stations_destination[station_index]['Station Number'] = station_index
                    stations_destination[station_index]['adress_station'] = \
                        raw_data['records'][station_index]['fields']['address'] + "Paris"
                    stations_destination[station_index]['nb_auto'] = raw_data['records'][station_index]['fields'][
                        'cars']

            self._stations_destination = stations_destination

        @property
        def address_station_origin(self):
            return self._address_station_origin

        @property
        def nb_auto_origin(self):
            return self._nb_cars_origin

        @property
        def address_station_destination(self):
            return self._address_station_destination

        @property
        def nb_auto_destination(self):
            return self._nb_auto_destination

        def time(self):
            return self._time

        def distance(self):
            return self._distance

        def get_all_other_origin_autolib_station(self):
            '''Afficher toutes les stations autolib de départ'''
            print("These are the next closest station with available cars by proximity:")
            print(self._stations_origin)

        def get_all_other_destination_autolib_station(self):
            '''Afficher toutes les stations autolib d'arrivée'''
            print("These are the next closest station with available cars by proximity:")
            print(self._stations_destination)

        def change_station_autolib_origin(self, value):
            '''On décide de prendre une autre station de départ au choix'''
            if isinstance(int, value) and value < len(self._stations_origin):
                self._address_station_origin = self._station_origin[value]['address_station']
            else:
                TypeError("Please enter the Station Number associated to a Autolib Station")

        def change_station_autolib_destination(self, value):
            '''On décide de prendre une autre station d'arrivée au choix'''
            if isinstance(int, value) and value < len(self._stations_origin):
                self._address_station_destination = self._station_destination[value]['address_station']
            else:
                TypeError("Please enter the Station Number associated to a Autolib Station")


if __name__ == "__main__":
    # Test des différentes portions d'une voyage en Autolib
    org = Place(address="10 rue oswaldo cruz paris 75016")
    des = Place(address="Favella Chic Paris")
    AtoB = Autolib(org, des, "autolib")
    print(repr(AtoB))

    org = Place(address="Montmartre, Paris")
    des = Place(address="Cité Universitaire, Paris")
    CtoD = Autolib(org, des, "autolib")
    print(repr(CtoD))
