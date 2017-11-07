#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from random import uniform
from unittest import TestCase

from backend.Itinerary import Itinerary
from backend.Itinerary_Autolib import Autolib
from backend.Itinerary_Bicycling import Bicycling
from backend.Itinerary_Driving import Driving
from backend.Itinerary_Transit import Transit
from backend.Itinerary_Uber import Uber
from backend.Itinerary_Velib import Velib
from backend.Itinerary_Walking import Walking
from backend.Place import Place


def random_place_in_paris():
    """return a random location in Paris"""
    MAX_LAT = 48.87
    MIN_LAT = 48.84
    MAX_LNG = 2.295
    MIN_LNG = 2.285

    rand_lat = uniform(MIN_LAT, MAX_LAT)
    rand_lng = uniform(MIN_LNG, MAX_LNG)
    return Place(lat=rand_lat, lng=rand_lng)


class Test(TestCase):
    """Teste toutes les fonction du projet Ford"""

    def test_place(self):
        somewhere = Place(address="3 rue Rivoli")
        self.assertEqual(somewhere.address, "3 rue Rivoli Paris")
        self.assertAlmostEqual(somewhere.lat, 48.8555654)
        self.assertAlmostEqual(somewhere.lng, 2.3589835)


    def test_itinerary_date(self):
        origin = random_place_in_paris()
        destination = random_place_in_paris()
        itinerary = Itinerary(origin=origin, destination=destination, date=datetime.now() + timedelta(days=1))
        self.assertAlmostEqual(itinerary.date, datetime.now() + timedelta(days=1))
        itinerary1 = Itinerary(origin=origin, destination=destination)
        self.assertAlmostEqual(itinerary1.date, datetime.now())

    def test_bicycling(self):
        origin = random_place_in_paris()
        destination = random_place_in_paris()
        itinerary = Bicycling(origin=origin, destination=destination)

    def test_walking(self):
        origin = random_place_in_paris()
        destination = random_place_in_paris()
        itinerary = Walking(origin=origin, destination=destination)

    def test_driving(self):
        origin = random_place_in_paris()
        destination = random_place_in_paris()
        itinerary = Driving(origin=origin, destination=destination)

    def test_Uber(self):
        origin = random_place_in_paris()
        destination = random_place_in_paris()
        itinerary = Uber(origin=origin, destination=destination)

    def test_Autolib(self):
        origin = random_place_in_paris()
        destination = random_place_in_paris()
        itinerary = Autolib(origin=origin, destination=destination)

    def test_Transit(self):
        origin = random_place_in_paris()
        destination = random_place_in_paris()
        itinerary = Transit(origin=origin, destination=destination)

    def test_Velib(self):
        origin = random_place_in_paris()
        destination = random_place_in_paris()
        itinerary = Velib(origin=origin, destination=destination)


if __name__ == "__main__":
    unittest.main()
