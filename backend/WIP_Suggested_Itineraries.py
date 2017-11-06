#!/usr/bin/env python
# -*- coding: utf-8 -*-


# TODO setters et getters
# TODO rajouter des info comme le prix
# TODO faire plus de tests pour voir si tout fonctionne

from Itinerary import Itinerary
from Itinerary_Autolib import Autolib
from Itinerary_Bicycling import Bicycling
from Itinerary_Driving import Driving
from Itinerary_Transit import Transit
from Itinerary_Uber import Uber
from Itinerary_Velib import Velib
from Itinerary_Walking import Walking
from Place import Place
from User import User
from WIP_meteo_yahoo import meteo_jour
import datetime



def Suggested_Itineraries(user, itinerary):

    if isinstance(user, User):
        pass
    else:
        raise TypeError("The destination variable should be an object from the class Place.")

    if isinstance(itinerary, Itinerary):
        pass
    else:
        raise TypeError("The origin variable should be an object from the class Place.")

    suggested_options = []
    suggested_itineraries = []
    number_of_option = 0

    for option in user.preferences:


        if option == 'transit':
            transit_option = Transit(origin=itinerary.origin, destination=itinerary.destination)
            suggested_options.append(['transit', transit_option])
        if option == 'uber':
            uber_option = Uber(origin=itinerary.origin, destination=itinerary.destination, date=None,
                               uber_type=None, transit_mode_type=None, itinerary_index=0)
            suggested_options.append(['uber', uber_option])
        if option == 'bus':
            bus_option = Transit(origin=itinerary.origin, destination=itinerary.destination,
                                 transit_mode_type='bus')
            suggested_options.append(['bus', bus_option])
        if option == 'walking':
            walking_option = Walking(origin=itinerary.origin, destination=itinerary.destination)
            suggested_options.append(['walking', walking_option])
        if option == 'driving':
            driving_option = Driving(origin=itinerary.origin, destination=itinerary.destination)
            suggested_options.append(['driving', driving_option])
        if option == 'autolib':
            autolib_option = Autolib(origin=itinerary.origin, destination=itinerary.destination)
            suggested_options.append(['autolib', autolib_option])
        if option == 'velib':
            velib_option = Velib(origin=itinerary.origin, destination=itinerary.destination)
            suggested_options.append(['velib', velib_option])
        if option == 'bicycling':
            bicycling_option = Bicycling(origin=itinerary.origin, destination=itinerary.destination)
            suggested_options.append(['bicycling', bicycling_option])

    for option_nb, transport_option_info in enumerate(suggested_options):
        transport_nom = transport_option_info[0]
        transport_option = transport_option_info[1]
        suggested_itineraries.append({})
        suggested_itineraries[option_nb]['transport_type'] = transport_nom
        suggested_itineraries[option_nb]['origin'] = {'address': itinerary.origin.address,
                                                      'lat': itinerary.origin.lat,
                                                      'lng': itinerary.origin.lng}
        suggested_itineraries[option_nb]['destination'] = {'address': itinerary.destination.address,
                                                           'lat': itinerary.destination.lat,
                                                           'lng': itinerary.destination.lng}
        suggested_itineraries[option_nb]['duration'] = transport_option.total_duration
        suggested_itineraries[option_nb]['polyline'] = transport_option.total_polyline
        suggested_itineraries[option_nb]['instructions'] = repr(transport_option)

        if transport_option is 'driving':
            suggested_itineraries[option]['distance'] = transport_option.driving_distance
        if transport_option is 'walking':
            suggested_itineraries[option]['distance'] = transport_option.walking_distance
        if transit_option is 'bicycling':
            suggested_itineraries[option]['distance'] = transport_option.bicycling_distance

        if transport_option is 'uber':
            suggested_itineraries[option]['wait_time'] = transport_option.uber_wait_duration
            # on utilise le polyline driving ici pour uber
            suggested_itineraries[option]['polyline'] = driving_option.total_polyline


    weather = preferences_with_weather(datetime.date.today())
    suggested_itineraries.append({'weather': weather})

    return suggested_itineraries


if __name__ == "__main__":
    """Script de test"""
    origin = Place("10 rue oswaldo cruz paris")
    destination = Place("La villette paris")
    iti = Itinerary(origin=origin, destination=destination)
    pierre = User()
    Suggested_Itineraries(pierre, iti)
