from Itinerary import Itinerary
from Place import Place
import requests
import math


class Driving(Itinerary):
    __URL_API_DIRECTION = 'https://maps.googleapis.com/maps/api/directions/json?&key=AIzaSyATrZmC9' \
                          '-XjaEAdwtPw6RG0QWV65dbywe0&mode=driving&alternatives=true '

    def __init__(self, origin, destination, transport_mode, date=None, transit_mode_type=None, itinerary_index=0):
        Itinerary.__init__(self, origin, destination, transport_mode, date, transit_mode_type, itinerary_index)

        if self.transport_mode == "driving":

            url_request = Driving.__URL_API_DIRECTION \
                          + "&origin=" \
                          + str(self._origin) \
                          + "&destination=" \
                          + str(self._destination)

            raw_data = requests.get(url_request).json()
            # on récupère les informations concernant les différentes étapes
            steps = raw_data['routes'][self.itinerary_index]['legs'][0]['steps']

            self._total_duration = raw_data['routes'][self.itinerary_index]['legs'][0]['duration']['value']
            self._total_polyline = raw_data['routes'][self.itinerary_index]['overview_polyline']['points']

            self._walking_distance = 0
            self._walking_duration = 0
            self._driving_distance = 0
            self._driving_duration = 0

            information_legs = []  # Notre liste stockant nos étapes de trajet

            # Parcours des étapes trouvées de notre trajet pour remplir notre liste de stockage information_legs
            for step_number, step in enumerate(steps):
                information_legs.append({})
                information_legs[step_number]['transport_mode'] = step['travel_mode']
                information_legs[step_number]['interim_start'] = Place(lat=step['start_location']['lat'],
                                                                       lng=step['start_location']['lng'])
                information_legs[step_number]['interim_destination'] = Place(lat=step['end_location']['lat'],
                                                                             lng=step['end_location']['lng'])
                information_legs[step_number]['distance'] = step['distance']['value']
                information_legs[step_number]['duration'] = step['duration']['value']
                information_legs[step_number]['instructions'] = step['html_instructions']

                if information_legs[step_number]['transport_mode'] == "DRIVING":
                    self._driving_distance += step['distance']['value']
                    self._driving_duration += step['duration']['value']
                else:
                    self._walking_distance += step['distance']['value']
                    self._walking_duration += step['duration']['value']

            self._information_legs = information_legs

        else:
            raise TypeError("transport mode not defined, no available routes were found")

    @property
    def total_duration(self):
        return self._total_duration

    @property
    def walking_duration(self):
        return self._walking_duration

    @property
    def walking_distance(self):
        return self._walking_distance

    @property
    def driving_duration(self):
        return self._driving_duration

    @property
    def driving_distance(self):
        return self._driving_distance

    @property
    def total_polyline(self):
        return self._total_polyline

    @property
    def information_legs(self):
        return self._information_legs

    def __repr__(self):
        res = ""
        res += "Your itinerary will take place in  {} step(s) :".format(len(self.information_legs))

        for leg_index, leg in enumerate(self.information_legs):
            res += "\n"
            res += "Portion " + str(leg_index)
            res += ": You will be " + leg['transport_mode']
            res += " for a duration of " + str(math.floor(leg['duration'] / 60 + 1)) + " min"
            res += " and a distance of " + str(math.floor(leg['distance'] / 100 + 1) / 10) + " km"
            res += " ; Please " + leg['instructions']

        res += "\nIt will take " + str(math.floor(self.total_duration / 60 + 1))
        res += " min, " + str(math.floor(self.walking_duration / 60 + 1)) + " min walking ("
        res += str(math.floor(self.walking_distance / 100 + 1) / 10) + " km)."
        res += "\n"

        return res


if __name__ == "__main__":
    """Script de test de la bonne construction des classes"""

    # Test des différentes portions d'une voyage en voiture
    org = Place(address="10 rue oswaldo cruz paris 75016")
    des = Place(address="Favella Chic Paris")
    AtoB = Driving(org, des, "driving")
    print(repr(AtoB))

    org = Place(address="Montmartre, Paris")
    des = Place(address="Cité Universitaire, Paris")
    CtoD = Driving(org, des, "driving")
    print(repr(CtoD))
