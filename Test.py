from unittest import TestCase

from Itinerary import Itinerary
from Place import Place

class Test(TestCase):
    """Teste toutes les fonction du projet Ford"""

    def test_place(self):
        somewhere=Place(adresse ="1 rue Joliot Curie, 91190 Gif-sur-Yvette")
        self.assertEqual(somewhere.address,"1 rue Joliot Curie, 91190 Gif-sur-Yvette")
        self.assertEqual(somewhere.lng,)
        self.

    def test_itinerary(self):
        itinerary_0=Itinerary()
        self.assertEqual()