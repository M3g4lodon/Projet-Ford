import Place


class Leg:
    """Portion d'un itinéraire"""

    def __init__(self, leg_origin, leg_destination, transport_mode, duration=None, distance=None, steps=list(),
                 polyline=None):
        if isinstance(leg_origin, Place.Place) and isinstance(leg_destination, Place.Place):
            self._origin = leg_origin
            self._destination = leg_destination
        else:
            raise TypeError("Est attendu pour un leg un départ/arrivée défini comme lieu.")

        self._transport_mode = transport_mode

        self._duration = duration
        self._distance = distance
        self._steps = steps
        self._polyline = polyline

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, value):
        self._distance = value

    @property
    def steps(self):
        return self._steps

    @steps.setter
    def steps(self, value):
        self._steps = value

    @property
    def polyline(self):
        return self._polyline

    @polyline.setter
    def polyline(self, value):
        self._polyline = value


if __name__ == "__main__":
    """Script de test"""
    portion_d_itineraire = Leg()
