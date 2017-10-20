import Route
import requests


class Transport(Route):


    URL_API_DIRECTION_Transit = 'https://maps.googleapis.com/maps/api/directions/json?&key=AIzaSyATrZmC9-XjaEAdwtPw6RG0QWV65dbywe0&mode=transit&alternatives=true'

    def __init__(self, origin, destination, transport_mode, transit_mode=None, date=None):

        Route.__init__(self, origin, destination, transport_mode, date)
        self._transport_mode = transport_mode


        if transit_mode is None:
            self._transit_mode = ''
        else:
            self._transit_mode = transit_mode


        if self._transport_mode in ["transit","Transit"]:
            liste = []


            url_request = Transport.URL_API_DIRECTION_Transit + "&origin=" + str(self._origin) + "&destination=" + str(self._destination) + "&transit_mode=" + str(self._transit_mode)
            print(url_request)
            raw_data = requests.get(url_request).json()
            etape = raw_data['routes'][self._route_index]['legs'][0]['steps'] #on récupère les informations concernant les différentes étapes du premier voyage proposé (celui qui correpond au plus rapide d'ailleurs...)

            self._nombre_etape = len(etape)


            for i in range(self._nombre_etape):
                liste.append({})
            for k in range(self._nombre_etape):
                    test = etape[k]
                    liste[k]['mode_de_transport'] = test['travel_mode']
                    liste[k]['distance'] = test['distance']['text']
                    # a = Place(float(test['end_location']['lat']), float(test['end_location']['lng']))
                    #print(test['end_location']['lat'])
                    liste[k]['destination_intermediaire'] = test['end_location'] #j'essaie de transformer les positions Long,Lat en adresse ! A FAIRE
                    liste[k]['time'] = test['duration']['text']
                    #b = Place(test['start_location']['lat'], test['start_location']['lng'])
                    liste[k]['depart_intermediaire'] = test['start_location'] # lat,long en adresse

                    if liste[k]['mode_de_transport']=="TRANSIT":
                        liste[k]['arrival_stop'] = test['transit_details']['arrival_stop']['name']
                        liste[k]['departure_stop']  = test['transit_details']['departure_stop']['name']
                        liste[k]['transit_mode'] = test['transit_details']['line']['vehicle']['type']
                        liste[k]['line'] = test['transit_details']['line']['short_name']
                        liste[k]['number_stops'] = test['transit_details']['num_stops']

                    else:
                        liste[k]['instructions'] = test['html_instructions']
            self._information_legs = liste #cette liste contient toutes les étapes et les informations utiles (encore à définir)

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

        for i in range(len(self._information_legs)):
            k +=1
            tampon = self._information_legs[i]
            if tampon['mode_de_transport'] == "TRANSIT" :
                print("Portion number {} : You will be taking the {} line number {} at station {} and arriving at {} after a duration of {} and {} stops.".format(k, tampon[
                    'transit_mode'], tampon['line'], tampon['departure_stop'], tampon['arrival_stop'], tampon['time'], tampon['number_stops']))
            else:

                print("Portion number {} : You will be {} for a duration of {} and a distance of {}; Please {}.".format(k, tampon['mode_de_transport'], tampon['time'], tampon['distance'], tampon['instructions']))



if __name__ == "__main__":
    """Script de test de la bonne construction des classes"""

#Test des différentes portions d'une voyage en transport de commun
voyage = Transport("10 rue oswaldo cruz paris 75016", "Favella Chic Paris","Transit","bus")

voyage.get_legs()
