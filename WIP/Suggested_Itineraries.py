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
            raise TypeError("L'itinéraire doit être un objet Itinerary")

        self._suggested_options = []
        self._suggested_itineraries = []



        for itinerary_options, option in enumerate(self._user.preferences):

            #dans nos autres codes, on se limite à 3 propositions de trajet... Je prends tout ici, mettre un while <3 si besoin
            if option == 'transit':
                transit_option = Transit(origin= self._itinerary.origin, destination = self._itinerary.destination)
                self._suggested_options.append(transit_option)
            if option == 'uber':
                uber_option = Uber(origin = self._itinerary.origin, destination = self._itinerary.destination, date=None, uber_type=None, transit_mode_type=None, itinerary_index=0)
                self._suggested_options.append(uber_option)
            if option == 'bus':
                bus_option = Transit(origin= self._itinerary.origin, destination = self._itinerary.destination, transit_mode_type='bus')
                self._suggested_options.append(bus_option)
            if option == 'walking':
                walking_option = Walking(origin= self._itinerary.origin, destination = self._itinerary.destination)
                self._suggested_options.append(walking_option)
            if option == 'driving':
                driving_option = Driving(origin= self._itinerary.origin, destination = self._itinerary.destination)
                self._suggested_options.append(driving_option)
            if option == 'autolib':
                autolib_option = Autolib(origin= self._itinerary.origin, destination = self._itinerary.destination)
                self._suggested_options.append(autolib_option)
            if option == 'velib':
                velib_option = Velib(origin= self._itinerary.origin, destination = self._itinerary.destination)
                self._suggested_options.append(velib_option)
            if option == 'bicycling':
                bicycling_option = Bicycling(origin= self._itinerary.origin, destination = self._itinerary.destination)
                self._suggested_options.append(bicycling_option)






if __name__ == "__main__":
    """Script de test"""
    origin = Place("10 rue oswaldo cruz paris")
    destination = Place("La villette paris")
    iti = Itinerary(origin=origin, destination= destination)
    pierre = User()
    Suggested_Itineraries(pierre, iti)






