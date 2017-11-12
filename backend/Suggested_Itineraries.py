#!/usr/bin/env python
# -*- coding: utf-8 -*-


# TODO setters et getters
# TODO rajouter des info comme le prix
# TODO faire plus de tests pour voir si tout fonctionne

import datetime

from backend.Itinerary import Itinerary
from backend.Itinerary_Autolib import Autolib
from backend.Itinerary_Bicycling import Bicycling
from backend.Itinerary_Driving import Driving
from backend.Itinerary_Transit import Transit
from backend.Itinerary_Uber import Uber
from backend.Itinerary_Velib import Velib
from backend.Itinerary_Walking import Walking
from backend.Place import Place
from backend.User import User


def Suggested_Itineraries(user, itinerary):
    # We want a maximum of 3 itineraries shown
    OPTIONS_NB_MAX = 3

    if isinstance(user, User):
        pass
    else:
        raise TypeError("The destination variable should be an object from the class Place.")

    if isinstance(itinerary, Itinerary):
        pass
    else:
        raise TypeError("The origin variable should be an object from the class Place.")

    suggested_options = []

    for option in user.preferences:
        if len(suggested_options) < OPTIONS_NB_MAX:
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

    suggested_itineraries = dict()
    suggested_itineraries['origin'] = {'address': itinerary.origin.address,
                                       'lat': itinerary.origin.lat,
                                       'lng': itinerary.origin.lng}
    suggested_itineraries['destination'] = {'address': itinerary.destination.address,
                                            'lat': itinerary.destination.lat,
                                            'lng': itinerary.destination.lng}
    weather = user.preferences_with_weather(datetime.date.today())
    suggested_itineraries['weather'] = weather[0]

    suggested_itineraries['results'] = []

    for option_nb, transport_option_info in enumerate(suggested_options):
        transport_nom = transport_option_info[0]
        transport_option = transport_option_info[1]
        suggested_itineraries['results'].append({})
        suggested_itineraries['results'][option_nb]['transport_type'] = transport_nom
        suggested_itineraries['results'][option_nb]['duration'] = transport_option.total_duration
        suggested_itineraries['results'][option_nb]['polyline_encoded'] = transport_option.total_polyline
        suggested_itineraries['results'][option_nb]['instructions'] = repr(transport_option).replace("\n", "<br />")

        if transport_option is 'driving':
            suggested_itineraries['results'][option]['distance'] = transport_option.driving_distance
        if transport_option is 'walking':
            suggested_itineraries['results'][option]['distance'] = transport_option.walking_distance
        if transport_option is 'bicycling':
            suggested_itineraries['results'][option]['distance'] = transport_option.bicycling_distance
        if transport_option is 'uber':
            suggested_itineraries['results'][option]['wait_time'] = transport_option.uber_wait_duration

    return suggested_itineraries


if __name__ == "__main__":
    """Script de test"""
    origin = Place("10 rue oswaldo cruz paris")
    destination = Place("La villette paris")
    iti = Itinerary(origin=origin, destination=destination)
    pierre = User('Touriste', True, True, True)
    print(Suggested_Itineraries(pierre, iti))
