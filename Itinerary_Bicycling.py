import requests

from Itinerary import Itinerary
from Itinerary import QueryLimit
from Place import Place


class Bicycling(Itinerary):
    __URL_API_DIRECTION = 'https://maps.googleapis.com/maps/api/directions/json?&key=AIzaSyATrZmC9' \
                          '-XjaEAdwtPw6RG0QWV65dbywe0&mode=bicycling&alternatives=true '

    def __init__(self, origin, destination, date=None, transit_mode_type=None, itinerary_index=0):

        Itinerary.__init__(self, origin, destination, date, transit_mode_type, itinerary_index)
        self.transport_mode = "bicycling"

        url_request = Bicycling.__URL_API_DIRECTION
        url_request += "&origin=" + str(self.origin.lat) + "," + str(self.origin.lng)
        url_request += "&destination=" + str(self.destination.lat) + "," + str(self.destination.lng)

        raw_data = requests.get(url_request).json()
        if raw_data['status'] == "OVER_QUERY_LIMIT":
            raise QueryLimit("Can't retieve any data from API (Bicyling)")
        else:
            # on récupère les informations concernant les différentes étapes
            steps = raw_data['routes'][self.itinerary_index]['legs'][0]['steps']

            self.total_duration = raw_data['routes'][self.itinerary_index]['legs'][0]['duration']['value']
            self.total_polyline = raw_data['routes'][self.itinerary_index]['overview_polyline']['points']

            self.walking_distance = 0
            self.walking_duration = 0
            self.bicycling_distance = 0
            self.bicycling_duration = 0

            self.information_legs = []  # Notre liste stockant nos étapes de trajet

            # Parcours des étapes trouvées de notre trajet pour remplir notre liste de stockage information_legs
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

                if self.information_legs[step_number]['transport_mode'] == "BICYCLING":
                    self.bicycling_distance += step['distance']['value']
                    self.bicycling_duration += step['duration']['value']
                else:
                    self.walking_distance += step['distance']['value']
                    self.walking_duration += step['duration']['value']

        self.transit_duration = 0


if __name__ == "__main__":
    """Script de test de la bonne construction des classes"""

    # Test des différentes portions d'une voyage en vélo
    org = Place(address="10 rue oswaldo cruz paris 75016")
    des = Place(address="Favella Chic Paris")
    AtoB = Bicycling(org, des)
    print(repr(AtoB))

    org = Place(address="Montmartre, Paris")
    des = Place(address="Cité Universitaire, Paris")
    CtoD = Bicycling(org, des)
    print(repr(CtoD))
