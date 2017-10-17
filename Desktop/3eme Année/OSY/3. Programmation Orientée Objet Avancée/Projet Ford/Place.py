import requests

class Place:
    """Désigne un lieu géographique"""

    __URL_API_GEOCODE = "https://maps.googleapis.com/maps/api/geocode/json?&key=AIzaSyDpVNzFcwgFfPJOK25P9NlMBL-YEe8bSow"

    def __init__(self, address=None, lat=None, long=None):
        # Cas où le lieu est ma spécifié
        if address is None and (lat is None or long is None):
            pass
            # Exception à créer ici
        self._address = address
        self._lat = lat
        self._long = long

    @property
    def address(self):
        if self._address is None:
            self.address_from_lat_long()
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def lat(self):
        if self._lat is None:
            self.lat_long_from_address()
        return self._lat

    @lat.setter
    def lat(self, value):
        if isinstance(value, float):
            self._lat = value
        else:
            raise TypeError("Un flottant est attendu pour la latitude")

    @property
    def long(self):
        if self._long is None:
            self.lat_long_from_address()
        return self._long

    @long.setter
    def long(self, value):
        if isinstance(value, float):
            self._long = value
        else:
            raise TypeError("Un flottant est attendu pour la longitude")

    def lat_long_from_address(self):
        """Calcule la latitude et la longitude de l'adresse d'origine"""
        url_request = Place.__URL_API_GEOCODE + "&address=" + self.address
        raw_data = requests.get(url_request).json()
        self.lat = raw_data['results'][0]['geometry']['location']['lat']
        self.long = raw_data['results'][0]['geometry']['location']['lng']

    def address_from_lat_long(self):
        """calcule l'adresse associé à une latitude et une longitude"""
        url_request = Place.__URL_API_GEOCODE + "&latlng=" + str(self.lat) + "," + str(self.long)
        raw_data = requests.get(url_request).json()
        self.address = raw_data['results'][0]['formatted_address']

    def __repr__(self):
        res = ""
        if self.address is not None:
            res += "[Place] Address : " + self.address + "\n"
        if not (self.lat is None or self.long is None):
            res += "[Place] Latitude : " + str(self.lat) + "\n" + "[Place] Longitude : " + str(self.long)
        return res


if __name__ == "__main__":
    """Script de test de la bonne construction des classes"""

    # Test des lieux
    paris = Place(address="Paris")
    print(paris)
    print("Pré-demande de coordonnées : " + str(paris))
    paris.lat_long_from_address()
    print("Post-demande de coordonnées : " + str(paris))
    poissonnier = Place(lat=48.896614, long=2.3522219)
    print(poissonnier)
    poissonnier.address_from_lat_long()
    print(poissonnier)