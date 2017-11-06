#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase

from Itinerary import Itinerary
from Place import Place

class Test(TestCase):
    """Teste toutes les fonctions du projet Ford"""

    def test_place(self):
        somewhere=Place(adresse ="1 rue Joliot Curie, 91190 Gif-sur-Yvette")
        self.assertEqual(somewhere.address,"1 rue Joliot Curie, 91190 Gif-sur-Yvette")
        self.assertEqual(somewhere.lng,)
        self.

    def test_itinerary(self):
        itinerary = Itinerary()
        self.assertEqual()

    def test_Autolib(self):

    def test_Velib(self):

    def test_Transit(self):

    def test_Uber(self):

    def test_Velib(self):

    def test_Walking(self):

    def test_User(self):

    def test_Suggested_itineraries(self):

    def test_meteo(self):
