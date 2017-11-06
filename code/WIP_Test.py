from unittest import TestCase

from Place import Place


class Test(TestCase):
    """Teste toutes les fonction du projet Ford"""

    def test_place(self):
        somewhere = Place(address="1 rue Joliot Curie, 91190 Gif-sur-Yvette")
        self.assertEqual(somewhere.address, "1 rue Joliot Curie, 91190 Gif-sur-Yvette")
        self.assertEqual(somewhere.lng, 2.1632833)
        self.assertEqual(somewhere.lat, 48.7100841)
