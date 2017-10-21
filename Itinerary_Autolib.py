from Itinerary import Itinerary
import Place


class Autolib(Itinerary):
    __URL_API_DIRECTION = 'https://maps.googleapis.com/maps/api/directions/json?&key=AIzaSyATrZmC9-XjaEAdwtPw6RG0QWV65dbywe0&mode=transit&alternatives=true'
    __URL_AUTOLIB = 'https://opendata.paris.fr/api/records/1.0/search/'

    def __init__(self, origin, destination, transport_mode, date=None, transit_mode_type=None, itinerary_index=0):
        super().__init__(self, origin, destination, transport_mode, date, transit_mode_type, itinerary_index)

        if self.transit_mode_type not "autolib":
            ValueError("cette classe ne prend en compte que les trajets en autolib")

        if isinstance(origin, Place):
            self._origin_lng = self._origin.lng()
            self._origin_lat = self._origin.lat()
        else:
            TypeError("L'origine doit être un objet Place")

        if isinstance(destination, Place):
            self._destination_lat = self.destination.lat()
            self._destination_lng = self.desination.lng()
        else:
            TypeError("La destination doit être un objet Place")

        number_hits = 0

        # Station autolib d'origine

        while number_hits == 0:
            stations_origin = []
            parameters = "dataset=autolib-disponibilite-temps-reel&q=status%3Dok+AND+cars%3E0&geofilter.distance=" + "%2C".join(
                self._origin_lat, self._origin_lng, 1000)
            r = requests.get(Autolib.__URL_AUTOLIB, parameters)
            results = r.json()
            number_hits = results['nhits']

            for number_station in range(number_hits):
                if results['records'][number_station]['fields']['cars'] == 0:
                    pass
                else:
                    self._address_station_origin = results['records'][number_station]['fields'][
                                                       'address'] + "Paris"  # Je me limite au cas où la station autolib se trouve à Paris et on sélectionne la première uniquement
                    self._nb_auto_origin = results['records'][number_station]['fields']['cars']
                    break
            for number_station in range(number_hits):

                if results['records'][number_station]['fields']['cars'] == 0:
                    pass
                else:
                    stations_origin.append({})
                    stations_origin[number_station]['Station Number'] = number_station
                    stations_origin[number_station]['adress_station'] = results['records'][number_station]['fields'][
                                                                            'address'] + "Paris"
                    stations_origin[number_station]['nb_auto'] = results['records'][number_station]['fields']['cars']

            self._stations_origin = stations_origin

        '''Attributs Distance - à pied - en voiture - et au total'''

        self._distance_driving = Driving(origin=self._address_station_origin,
                                         destination=self._address_station_destination).distance(self)

        self._distance_walking = Walking(origin=self._origin, destination=self._address_station_origin).distance(
            self) + Walking(origin=self._destination, destination=self._address_station_destination).distance(self)

        self._distance = self._distance_walking + self._distance_driving

        '''Attributs Temps - à pied - en voiture - et au total'''        

        self._time_driving = Driving(origin=self._origin, destination=self._address_station_origin).duration(
            self)
        self._time_walking = Walking(origin=self._origin, destination=self._address_station_origin).duration(
            self)
        self._time = self._time_driving + self._time_walking

        #station autolib à l'arrivée

        while number_hits == 0:
            stations_destination = []
            parameters = "dataset=autolib-disponibilite-temps-reel&q=status%3Dok+AND+cars%3E0&geofilter.distance=" + "%2C".join(
                self._destination_lat, self._destination_lng, 1000)
            r = requests.get(Autolib.__URL_AUTOLIB, parameters)
            results = r.json()
            number_hits = results['nhits']

            for number_station in range(number_hits):
                if results['records'][number_station]['fields']['cars'] == 0:
                    pass
                else:
                    self._address_station_destination = results['records'][number_station]['fields'][
                                                            'address'] + "Paris"  # Je me limite au cas où la station autolib se trouve à Paris et on sélectionne la première uniquement
                    self._nb_auto_destination = results['records'][number_station]['fields']['cars']
                    break
            for number_station in range(number_hits):

                if results['records'][number_station]['fields']['cars'] == 0: #faut changer ce paramètre, il faudrait voir si on a accès au nombre de bornes libres
                    pass
                else:
                    stations_destination.append({})
                    stations_destination[number_station]['Station Number'] = number_station
                    stations_destination[number_station]['adress_station'] = \
                    results['records'][number_station]['fields']['address'] + "Paris"
                    stations_destination[number_station]['nb_auto'] = results['records'][number_station]['fields'][
                        'cars']

            self._stations_destination = stations_destination

        @property
        def address_station_origin(self):
            return self._address_station_origin

        @property
        def nb_auto_origin(self):
            return self._nb_auto_origin

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
