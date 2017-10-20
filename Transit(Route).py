import Route
import requests


class Transit(Route):


    URL_API_DIRECTION_Transit = 'https://maps.googleapis.com/maps/api/directions/json?&key=AIzaSyATrZmC9-XjaEAdwtPw6RG0QWV65dbywe0&mode=transit&alternatives=true'

    def __init__(self, origin, destination, transport_mode, transit_mode="", date=None):

        Route.__init__(self, origin, destination, transport_mode, date)
        self._transport_mode = transport_mode
        self._transit_mode = transit_mode


        if self._transport_mode == "transit":
            information_legs = []


            url_request = Transport.URL_API_DIRECTION_Transit + "&origin=" + str(self._origin) + "&destination=" + str(self._destination) + "&transit_mode=" + str(self._transit_mode)
            raw_data = requests.get(url_request).json()
            etapes = raw_data['routes'][self._route_index]['legs'][0]['steps'] #on récupère les informations concernant les différentes étapes du premier voyage proposé (celui qui correpond au plus rapide d'ailleurs...)

            self._steps_number = len(etapes)


         
                
            for step_number in range(self._steps_number):
                    information_legs.append({})
                    etape = etapes[step_number]
                    information_legs[step_number]['mode_de_transport'] = etape['travel_mode']
                    information_legs[step_number]['distance'] = etape['distance']['text']
                    #a = Place(lat = etape['end_location']['lat']), lng = etape['end_location']['lng']))
                    information_legs[step_number]['destination_intermediaire'] = etape['end_location'] #j'essaie de transformer les positions Long,Lat en adresse ! A FAIRE
                    information_legs[step_number]['time'] = etape['duration']['text']
                    b = Place(lat = etape['start_location']['lat'], lng = etape['start_location']['lng'])
                    information_legs[step_number]['depart_intermediaire'] = etape['start_location'] # lat,long en adresse

                    if information_legs[step_number]['mode_de_transport']=="TRANSIT":
                        information_legs[step_number]['arrival_stop'] = etape['transit_details']['arrival_stop']['name']
                        information_legs[step_number]['departure_stop']  = etape['transit_details']['departure_stop']['name']
                        information_legs[step_number]['transit_mode'] = etape['transit_details']['line']['vehicle']['type']
                        information_legs[step_number]['line'] = etape['transit_details']['line']['short_name']
                        information_legs[step_number]['number_stops'] = etape['transit_details']['num_stops']

                    else:
                        information_legs[k]['instructions'] = etape['html_instructions']
            self._information_legs = information_legs #cette liste contient toutes les étapes et les informations utiles (encore à définir)

        else:
            raise TypeError("transport mode not defined, no available routes were found")

    # transit_routing_preference — Specifies preferences for transit routes. Using this parameter,
    # you can bias the options returned, rather than accepting the default best route chosen by the API.
    # This parameter may only be specified for transit directions, and only if the request includes an API
    # key or a Google Maps APIs Premium Plan client ID. The parameter supports the following arguments:
    # less_walking indicates that the calculated route should prefer limited amounts of walking.
    # fewer_transfers indicates that the calculated route should prefer a limited number of transfers.

    def get_legs(self):

        '''On va avoir accès à toutes les informations '''

        k = 0
        print("Your itinerary will take place in  {} step(s) :".format(len(self._information_legs)))

        #use enumerate
        for leg_index, leg  in enumerate(self._information_legs):
            
            if leg['mode_de_transport'] == "TRANSIT" :
                print("Portion number {} : You will be taking the {} line number {} at station {} and arriving at {} after a duration of {} and {} stops.".format(leg_index, leg[
                    'transit_mode'], leg['line'], leg['departure_stop'], leg['arrival_stop'], leg['time'], leg['number_stops']))
            else:

                print("Portion number {} : You will be {} for a duration of {} and a distance of {}; Please {}.".format(leg_index, leg['mode_de_transport'], leg['time'], leg['distance'], leg['instructions']))



if __name__ == "__main__":
    """Script de test de la bonne construction des classes"""

    #Test des différentes portions d'une voyage en transport de commun
    voyage = Transport("10 rue oswaldo cruz paris 75016", "Favella Chic Paris","Transit","bus")

    voyage.get_legs()
