import Itinerary
import requests


class Bicycling(Itinerary):

    __URL_API_DIRECTION_Transit = 'https://maps.googleapis.com/maps/api/directions/json?&key=AIzaSyATrZmC9-XjaEAdwtPw6RG0QWV65dbywe0&mode=bicycling&alternatives=true'

    def __init__(self, origin, destination, transit_mode, date=None, route_index=None):

        Itinerary.__init__(self, origin, destination, transit_mode, date, route_index)
        
        


        if self._transit_mode == "bicycling":

            url_request = Transport.__URL_API_DIRECTION_Transit + "&origin=" + str(self._origin) + "&destination=" + str(
                self._destination)
        
            raw_data = requests.get(url_request).json()
            etapes = raw_data['routes'][self.route_index]['legs'][0][
                'steps']  # on récupère les informations concernant les différentes étapes du premier voyage proposé (celui qui correpond au plus rapide d'ailleurs...)

            self._distance = etapes['distance']
            self._duration = etapes['duration']
            self._polyline = raw_data['routes']['overview_polyline']['points']


        else:
            raise TypeError("This class only takes walking as transit mode option")



        @property
        def distance(self):
            return self._distance

        @property
        def duration(self):
            return self._duration

        @property
        def polyline(self):
            return self._polyline


if __name__ == "__main__":
    """Script de test de la bonne construction des classes"""

    # Test des différentes portions d'une voyage en transport de commun
    voyage = Bicycling("10 rue oswaldo cruz paris 75016", "Favella Chic Paris", "walking")


