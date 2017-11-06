#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests


class Place:
    """Specifies a geographical location"""

    __URL_API_GEOCODE = "https://maps.googleapis.com/maps/api/geocode/json?&key=AIzaSyDpVNzFcwgFfPJOK25P9NlMBL-YEe8bSow"

    def __init__(self, address=None, lat=None, lng=None):
        # Cas où le lieu est ma spécifié
        if address is None and (lat is None or lng is None):
            self._address = "Paris, France"
        self._address = address
        self._lat = lat
        self._lng = lng

    @property
    def address(self):
        if self._address is None:
            self.address_from_lat_lng()
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def lat(self):
        if self._lat is None:
            self.lat_lng_from_address()
        return self._lat

    @lat.setter
    def lat(self, value):
        if isinstance(value, float):
            self._lat = value
        else:
            raise TypeError("Expected a float for latitude.")

    @property
    def lng(self):
        if self._lng is None:
            self.lat_lng_from_address()
        return self._lng

    @lng.setter
    def lng(self, value):
        if isinstance(value, float):
            self._lng = value
        else:
            raise TypeError("Expected a float for longitude.")

    def lat_lng_from_address(self):
        """Computes the latitude and the longitude of the address' origin."""
        url_request = Place.__URL_API_GEOCODE + "&address=" + self.address
        raw_data = requests.get(url_request).json()
        self.lat = raw_data['results'][0]['geometry']['location']['lat']
        self.lng = raw_data['results'][0]['geometry']['location']['lng']

    def address_from_lat_lng(self):
        """Computes the address associated with the latitude and longitude."""
        url_request = Place.__URL_API_GEOCODE + "&latlng=" + str(self.lat) + "," + str(self.lng)
        raw_data = requests.get(url_request).json()
        self.address = raw_data['results'][0]['formatted_address']

    def __repr__(self):
        res = ""
        if self.address is not None:
            res += "[Place] Address : " + self.address + "\n"
        if not (self.lat is None or self.lng is None):
            res += "[Place] Latitude : " + str(self.lat) + "\n" + "[Place] Longitude : " + str(self.lng)
        return res

    def __str__(self):
        return self.address


if __name__ == "__main__":
    """Script de test de la bonne construction des classes"""

    # Test des lieux
    paris = Place(address="Paris")
    print(paris)
    print("Pré-demande de coordonnées : " + str(paris))
    paris.lat_lng_from_address()
    print("Post-demande de coordonnées : " + str(paris))
    poissonnier = Place(lat=48.896614, lng=2.3522219)
    print(poissonnier)
    poissonnier.address_from_lat_lng()
    print(poissonnier)
