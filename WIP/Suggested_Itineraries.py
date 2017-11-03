#TODO setters et getters
#TODO rajouter des info comme le prix
#TODO faire plus de tests pour voir si tout fonctionne 

from Itinerary import Itinerary
from Itinerary_Uber import Uber
from Itinerary_Autolib import Autolib
from User import User
from Itinerary_Driving import Driving
from Itinerary_Bicycling import Bicycling
from Itinerary_Velib import Velib
from Itinerary_Walking import Walking
from Itinerary_Transit import Transit
from Place import Place


class Suggested_Itineraries:

    def __init__(self, user, itinerary):

        if isinstance(user, User):
            self._user = user
        else:
            raise TypeError("L'utilisateur doit être un objet User")

        if isinstance(itinerary, Itinerary):
            self._itinerary = itinerary
        else:
            raise TypeError("L'origine doit être un objet Place")

        self._suggested_options = []
        self._suggested_itineraries = []
        self._number_of_option = 0



        for itinerary_options, option in enumerate(self._user.preferences):

            #dans nos autres codes, on se limite à 3 propositions de trajet... Je prends tout ici, mettre un while <3 si besoin
            if option == 'transit':
                transit_option = Transit(origin= self._itinerary.origin, destination = self._itinerary.destination)
                self._suggested_options.append(['transit',transit_option])
            if option == 'uber':
                uber_option = Uber(origin = self._itinerary.origin, destination = self._itinerary.destination, date=None, uber_type=None, transit_mode_type=None, itinerary_index=0)
                self._suggested_options.append(['uber',uber_option])
            if option == 'bus':
                bus_option = Transit(origin= self._itinerary.origin, destination = self._itinerary.destination, transit_mode_type='bus')
                self._suggested_options.append(['bus',bus_option])
            if option == 'walking':
                walking_option = Walking(origin= self._itinerary.origin, destination = self._itinerary.destination)
                self._suggested_options.append(['walking',walking_option])
            if option == 'driving':
                driving_option = Driving(origin= self._itinerary.origin, destination = self._itinerary.destination)
                self._suggested_options.append(['driving',driving_option])
            if option == 'autolib':
                autolib_option = Autolib(origin= self._itinerary.origin, destination = self._itinerary.destination)
                self._suggested_options.append(['autolib', autolib_option])
            if option == 'velib':
                velib_option = Velib(origin= self._itinerary.origin, destination = self._itinerary.destination)
                self._suggested_options.append(['velib',velib_option])
            if option == 'bicycling':
                bicycling_option = Bicycling(origin= self._itinerary.origin, destination = self._itinerary.destination)
                self._suggested_options.append(['bicycling', bicycling_option])


        for option, transport_option_info in enumerate(self._suggested_options):
            transport_nom = transport_option_info[0]
            transport_option = transport_option_info[1]
            self._suggested_itineraries.append({})
            self._suggested_itineraries[option]['transport_type'] = transport_nom
            self._suggested_itineraries[option]['origin']={'address': self._itinerary.origin.address, 'lat': self._itinerary.origin.lat, 'lng': self._itinerary.origin.lng}
            self._suggested_itineraries[option]['destination'] = {'address': self._itinerary.destination.address,
                                                             'lat': self._itinerary.destination.lat,
                                                             'lng': self._itinerary.destination.lng}
            self._suggested_itineraries[option]['duration'] = transport_option.total_duration
            self._suggested_itineraries[option]['polyline'] = transport_option.total_polyline
            self._suggested_itineraries[option]['instructions'] = repr(transport_option)

            if transport_option is 'driving':
                self._suggested_itineraries[option]['distance'] = transport_option.driving_distance
            if transport_option is 'walking':
                self._suggested_itineraries[option]['distance'] = transport_option.walking_distance
            if transit_option is 'bicycling':
                self._suggested_itineraries[option]['distance'] = transport_option.bicycling_distance

            if transport_option is 'uber':
                self._suggested_itineraries[option]['wait_time'] = transport_option.uber_wait_duration
                #on utilise le polyline driving ici pour uber
                self._suggested_itineraries[option]['polyline'] = driving_option.total_polyline
        

if __name__ == "__main__":
    """Script de test"""
    origin = Place("10 rue oswaldo cruz paris")
    destination = Place("La villette paris")
    iti = Itinerary(origin=origin, destination= destination)
    pierre = User()
    Suggested_Itineraries(pierre, iti)






