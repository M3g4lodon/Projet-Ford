from unittest import TestCase
from random import uniform
from datetime import datetime

from Place import Place
from Itinerary import Itinerary
from Itinerary_Autolib import Autolib
from Itinerary_Bicycling import Bicycling



class Test(TestCase):
    """Teste toutes les fonction du projet Ford"""

    def test_place(self):
        somewhere = Place(address="1 rue Joliot Curie, 91190 Gif-sur-Yvette")
        self.assertEqual(somewhere.address, "1 rue Joliot Curie, 91190 Gif-sur-Yvette")
        self.assertEqual(somewhere.lng, 2.1632833)
        self.assertEqual(somewhere.lat, 48.7100841)

    @staticmethod
    def random_place_in_paris():
        """return a random location in Paris"""
        MAX_LAT = 48.90
        MIN_LAT = 48.80
        MAX_LNG = 2.41
        MIN_LNG = 2.22

        rand_lat=uniform(MIN_LAT,MAX_LAT)
        rand_lng=uniform(MIN_LNG,MAX_LNG)
        return Place(lat=rand_lat, lng=rand_lng)

    def test_itinerary_date(self):
        origin = random_place_in_paris()
        destination = random_place_in_paris()
        itinerary = Bicycling(origin=origin, destination=destination)
        self.assertEqual(itinerary.date.date(),datetime.now().date())
    def test_bicycling(self):
        origin=random_place_in_paris()
        destination=random_place_in_paris()
        itinerary=Bicycling(origin=origin, destination=destination)

if __name__ =="__main__":
    pass