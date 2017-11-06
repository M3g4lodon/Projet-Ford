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
    MAX_LAT = 48.90
    MIN_LAT = 48.80
    MAX_LNG = 2.41
    MIN_LNG = 2.22

    rand_lat = uniform(MIN_LAT, MAX_LAT)
    rand_lng = uniform(MIN_LNG, MAX_LNG)
    return Place(lat=rand_lat, lng=rand_lng)


class Test(TestCase):
    """Teste toutes les fonction du projet Ford"""

    def test_place(self):
        somewhere = Place(address="1 rue Joliot Curie, 91190 Gif-sur-Yvette")
        self.assertEqual(somewhere.address, "1 rue Joliot Curie, 91190 Gif-sur-Yvette")
        self.assertEqual(somewhere.lng, 2.1632833)
        self.assertEqual(somewhere.lat, 48.7100841)

    def test_itinerary_date(self):
        origin = random_place_in_paris()
        destination = random_place_in_paris()
        itinerary = Itinerary(origin=origin, destination=destination, date=datetime.now() + timedelta(days=1))
        self.assertEqual(itinerary.date.date(), datetime.now() + timedelta(days=1))
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
    pass
