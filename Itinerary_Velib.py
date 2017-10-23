from Itinerary import Itinerary
from Itinerary import QueryLimit
from Place import Place
import requests

class Velib(Itinerary):
    __URL_API_DIRECTION = 'https://maps.googleapis.com/maps/api/directions/json?&key=AIzaSyATrZmC9-XjaEAdwtPw6RG0QWV65dbywe0&mode=transit&alternatives=true'
    __URL_VELIB = 'https://opendata.paris.fr/api/records/1.0/search/'

    def __init__(self, origin, destination, date=None, transit_mode_type=None, itinerary_index=0):
        Itinerary.__init__(self, origin, destination, date, transit_mode_type, itinerary_index)
        self.transport_mode = "velib"

        number_hits = 0

        # Station velib d'origine

        while number_hits == 0:
            stations_origin = []
            parameters = "dataset=stations-velib-disponibilites-en-temps-reel&q=status%3D%3D%22open%22+AND+available_bikes%3E0&geofilter.distance=" + "%2C".join(
                self.origin_lat, self.origin_lng, 1000)
            r = requests.get(Velib.__URL_VELIB, parameters)
            results = r.json()
            number_hits = results['nhits']

            for number_station in range(number_hits):
                if results['records'][number_station]['fields']['cars'] == 0:
                    pass
                else:
                    self.address_station_origin = results['records'][number_station]['fields'][
                                                       'address'] + "Paris"  # Je me limite au cas où la station velib se trouve à Paris et on sélectionne la première uniquement
                    self.nb_auto_origin = results['records'][number_station]['fields']['available_bike']
                    self.distance_origin_station_origin = results['records'][number_station]['fields']['dist']
                    break
            for number_station in range(number_hits):

                if results['records'][number_station]['fields']['available_bike'] == 0:
                    pass
                else:
                    stations_origin.append({})
                    stations_origin[number_station]['Station Number'] = number_station
                    stations_origin[number_station]['adress_station'] = results['records'][number_station]['fields'][
                                                                            'address'] + "Paris"
                    stations_origin[number_station]['nb_bike'] = results['records'][number_station]['fields']['cars']

            self.stations_origin = stations_origin

        '''Attributs Distance - à pied - en voiture - et au total'''

        self.distance_bicycling = Bicycling(origin=self.address_station_origin,
                                            destination=self.address_station_destination).distance(self)

        self.distance_walking = Walking(origin=self.origin, destination=self.address_station_origin).distance(
            self) + Walking(origin=self.destination, destination=self.address_station_destination).distance(self)

        self.distance = self.distance_walking + self.distance_bicycling

        '''Attributs Temps - à pied - en voiture - et au total'''

        self.time_bicycling = Bicycling(origin=self.origin, destination=self.address_station_origin).duration(
            self)
        self.time_walking = Walking(origin=self.origin, destination=self.address_station_origin).duration(
            self)
        self.time = self.time_bicycling + self.time_walking

        #station velib à l'arrivée

        while number_hits == 0:
            stations_destination = []
            parameters = "dataset=velib-disponibilite-temps-reel&q=status%3Dok+AND+cars%3E0&geofilter.distance=" + "%2C".join(
                self.destination_lat, self.destination_lng, 1000)
            r = requests.get(Velib.__URL_VELIB, parameters)
            results = r.json()
            number_hits = results['nhits']

            for number_station in range(number_hits):
                if results['records'][number_station]['fields']['cars'] == 0:
                    pass
                else:
                    self.address_station_destination = results['records'][number_station]['fields'][
                                                            'address'] + "Paris"  # Je me limite au cas où la station velib se trouve à Paris et on sélectionne la première uniquement
                    self.nb_auto_destination = results['records'][number_station]['fields']['cars']
                    break
            for number_station in range(number_hits):

                if results['records'][number_station]['fields']['available_bike_stands'] == 0: #on souhaite arriver à une station avec des places libres
                    pass
                else:
                    stations_destination.append({})
                    stations_destination[number_station]['Station Number'] = number_station
                    stations_destination[number_station]['adress_station'] = \
                    results['records'][number_station]['fields']['address'] + "Paris"
                    stations_destination[number_station]['nb_available_bike_stands'] = results['records'][number_station]['fields'][
                        'available_bike_stands']

            self.stations_destination = stations_destination

        @property
        def address_station_origin(self):
            return self.address_station_origin

        @property
        def nb_auto_origin(self):
            return self.nb_auto_origin

        @property
        def address_station_destination(self):
            return self.address_station_destination

        @property
        def nb_auto_destination(self):
            return self.nb_auto_destination

        def time(self):
            return self.time

        def distance(self):
            return self.distance    





        def get_all_other_origin_velib_station(self):
            '''Afficher toutes les stations velib de départ'''
            print("These are the next closest station with available cars by proximity:")
            print(self.stations_origin)

        def get_all_other_destination_velib_station(self):
            '''Afficher toutes les stations velib d'arrivée'''
            print("These are the next closest station with available cars by proximity:")
            print(self.stations_destination)

        def change_station_velib_origin(self, value):
            '''On décide de prendre une autre station de départ au choix'''
            if isinstance(int, value) and value < len(self.stations_origin):
                self.address_station_origin = self.station_origin[value]['address_station']
            else:
                TypeError("Please enter the Station Number associated to a Velib Station")

        def change_station_velib_destination(self, value):
            '''On décide de prendre une autre station d'arrivée au choix'''
            if isinstance(int, value) and value < len(self.stations_origin):
                self.address_station_destination = self.station_destination[value]['address_station']
            else:
                TypeError("Please enter the Station Number associated to a Velib Station")


if __name__"__main__":

    # Test des différentes portions d'une voyage en Velib
    org = Place(address="10 rue oswaldo cruz paris 75016")
    des = Place(address="Favella Chic Paris")
    AtoB = Velib(org, des)
    print(repr(AtoB))

    org = Place(address="Montmartre, Paris")
    des = Place(address="Cité Universitaire, Paris")
    CtoD = Velib(org, des)
    print(repr(CtoD))