from Itinerary import Itinerary
from Place import Place
import requests
import math


class Transit(Itinerary):
    """Désigne un itinéraire utilisant les transports en commun"""

    __URL_API_DIRECTION_TRANSIT = 'https://maps.googleapis.com/maps/api/directions/json?&key=AIzaSyATrZmC9' \
                                  '-XjaEAdwtPw6RG0QWV65dbywe0&mode=transit&alternatives=true '

    def __init__(self, origin, destination, transport_mode, date=None, transit_mode_type=None, itinerary_index=0):
        Itinerary.__init__(self, origin, destination, transport_mode, date, transit_mode_type,
                           itinerary_index)

        if self.transport_mode == "transit":
            information_legs = []  # Notre liste stockant nos étapes de trajet

            url_request = Transit.__URL_API_DIRECTION_TRANSIT + "&origin=" + str(self._origin) + "&destination=" + str(
                self._destination) + "&transit_mode=" + str(self._transit_mode_type)
            raw_data = requests.get(url_request).json()
            # on récupère les informations concernant les différentes étapes du premier voyage proposé
            # (celui qui correpond au plus rapide d'ailleurs...)
            steps = raw_data['routes'][self.itinerary_index]['legs'][0]['steps']

            self._total_duration = raw_data['routes'][self.itinerary_index]['legs'][0]['duration']['value']
            self._total_polyline = raw_data['routes'][self.itinerary_index]['overview_polyline']['points']

            self._walking_distance = 0
            self._walking_duration = 0
            self._transit_duration = 0

            # Parcours des étapes trouvées de notre trajet pour remplir notre liste de stockage information_legs
            for step_number, step in enumerate(steps):
                information_legs.append({})
                information_legs[step_number]['transport_mode'] = step['travel_mode']
                information_legs[step_number]['distance'] = step['distance']['value']
                self._walking_distance += step['distance']['value']
                information_legs[step_number]['interim_destination'] = Place(lat=step['end_location']['lat'],
                                                                             lng=step['end_location']['lng'])
                information_legs[step_number]['duration'] = step['duration']['value']
                self._walking_duration += step['duration']['value']
                information_legs[step_number]['interim_start'] = Place(lat=step['start_location']['lat'],
                                                                       lng=step['start_location']['lng'])
                if information_legs[step_number]['transport_mode'] == "TRANSIT":
                    information_legs[step_number]['arrival_stop'] = step['transit_details']['arrival_stop']['name']
                    information_legs[step_number]['departure_stop'] = step['transit_details']['departure_stop']['name']
                    information_legs[step_number]['transit_mode'] = step['transit_details']['line']['vehicle']['type']
                    if 'short_name' in step['transit_details']['line'].keys():
                        information_legs[step_number]['line'] = step['transit_details']['line']['short_name']
                    else:
                        information_legs[step_number]['line'] = step['transit_details']['line']['name']
                    information_legs[step_number]['number_stops'] = step['transit_details']['num_stops']
                    information_legs[step_number]['duration'] = step['duration']['value']
                    self._transit_duration += step['duration']['value']

                else:
                    information_legs[step_number]['instructions'] = step['html_instructions']

            self._information_legs = information_legs

        else:
            raise TypeError("transport mode not defined, no available routes were found")

    # transit_routing_preference — Specifies preferences for transit routes. Using this parameter,
    # you can bias the options returned, rather than accepting the default best route chosen by the API.
    # This parameter may only be specified for transit directions, and only if the request includes an API
    # key or a Google Maps APIs Premium Plan client ID. The parameter supports the following arguments:
    # less_walking indicates that the calculated route should prefer limited amounts of walking.
    # fewer_transfers indicates that the calculated route should prefer a limited number of transfers.

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
    def transit_duration(self):
        return self._transit_duration

    @property
    def total_polyline(self):
        return self._total_polyline

    @property
    def information_legs(self):
        return self._information_legs

    def __repr__(self):
        res = ""
        res += "Your itinerary will take place in  {} step(s) :".format(len(self._information_legs))

        for leg_index, leg in enumerate(self.information_legs):
            if leg['transport_mode'] == "TRANSIT":
                res += "\n"
                res += "Portion " + str(leg_index)
                res += ": You will be taking the " + leg['transit_mode']
                res += " line number " + leg['line']
                res += " at station " + str(leg['departure_stop'])
                res += " and arriving at " + str(leg['arrival_stop'])
                res += " after a duration of " + str(math.floor(leg['duration'] / 60 + 1)) + " min"
                res += " and " + str(leg['number_stops'])
                res += " stops."
            else:
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

    # Test des différentes portions d'une voyage en transport de commun
    org = Place(address="79 Avenue de la république 75011, Paris")
    des = Place(address="La Muette, Paris")
    AtoB = Transit(org, des, "transit", transit_mode_type="bus")
    print(repr(AtoB))

    org = Place(address="Montmartre, Paris")
    des = Place(address="Cité Universitaire, Paris")
    CtoD = Transit(org, des, "transit", transit_mode_type="bus")
    print(repr(CtoD))
