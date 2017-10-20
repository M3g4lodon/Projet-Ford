import Itinerary
import Place


class Autolib(Itinerary):
    _URL_API_DIRECTION = 'https://maps.googleapis.com/maps/api/directions/json?&key=AIzaSyATrZmC9-XjaEAdwtPw6RG0QWV65dbywe0&mode=transit&alternatives=true'
    _URL_AUTOLIB = 'https://opendata.paris.fr/api/records/1.0/search/'

    def __init__(self, origin, destination, transit_mode, date=None):
        super().__init__(origin, destination, transit_mode, date)

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

        while number_hits == 0:
            stations_origin = []
            parameters = "dataset=autolib-disponibilite-temps-reel&q=status%3Dok+AND+cars%3E0&geofilter.distance=" + "%2C".join(self._origin_lat, self._origin_lng, 1000)
            r = requests.get(Autolib._URL_AUTOLIB, parameters)
            results = r.json()
            number_hits = results['nhits']

            for number_station in range(number_hits):
                if results['records'][number_station]['fields']['cars'] == 0:
                    pass
                else:
                    self._address_station_depart = results['records'][number_station]['fields']['address'] + "Paris"  # Je me limite au cas où la station autolib se trouve à Paris et on sélectionne la première uniquement
                    self._nb_auto = results['records'][number_station]['fields']['cars']
                    break
            for number_station in range(number_hits):

                if results['records'][number_station]['fields']['cars'] == 0:
                    pass
                else:
                    stations_origin.append({})
                    stations_origin[number_station]['adress_station'] = results['records'][number_station]['fields']['address'] + "Paris"
                    stations_origin[number_station]['nb_auto'] = results['records'][number_station]['fields']['cars']
            self._stations_origin = stations_origin
        @property
        def address_station(self):
            return self._address_station

        @property
        def nb_auto(self):
            return self._nb_auto

        def change_origin_autolib_station(self):
            print("These are the next closest station with available cars by proximity:")
            print(self._stations_origin)




