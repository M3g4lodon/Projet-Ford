from datetime import datetime as dt
import requests
import Leg
import Place

class Route:
    """Désigne un trajet entre deux points spécifiés dans l'itinéraire"""

    __TRANSPORT_MODES = ["walking", "driving", "velib", "autolib"]  # Liste des modes de transport possibles
    __route_id = 1
    URL_API_DIRECTION = 'https://maps.googleapis.com/maps/api/directions/json?&key=AIzaSyATrZmC9-XjaEAdwtPw6RG0QWV65dbywe0'



    def __init__(self, origin, destination, transport_mode, date=None, route_index=None):
        self._id = Route.__route_id
        Route.__route_id += 1

        self._origin = origin
        self._destination = destination
        self._transport_mode = transport_mode
        self._destination_intermediaire = []
        self._transport_mode_intermediaire=[]

        # Par défaut, la date prise pour la recherche d'itinéraire est "maintenant"
        if date is None:
            self._date = dt.now()
        else:
            self._date = date

        #Par défaut, la route sélectionnée est la première, sinon c'est celle spécifiée
        if route_index is None:
            self._route_index = 0
        else:
            self._route_index = route_index

        # On determine le nombre de routes de transit proposées par Google Maps

                if self._transport_mode in ["Transit","driving","walking","bicycling"]:
            liste = []
            url_request = Route.URL_API_DIRECTION + "&origin=" + str(self.origin) + "&destination=" + str(self.destination) + "&mode=" + str(self.transport_mode) +"&alternatives=True"
            print(url_request)
            raw_data = requests.get(url_request).json()
            etape = raw_data['routes'][self._route_index]['legs'][0]['steps'] #on récupère les informations concernant les différentes étapes
            print(etape)
            self._nombre_etape = len(etape)
            print(len(etape))

            for i in range(self._nombre_etape):
                liste.append({})
            for k in range(self._nombre_etape):
                    test = etape[k]
                    liste[k]['distance'] = test['distance']['text']
                    liste[k]['destination_intermediaire'] = test['end_location']
                    liste[k]['instructions'] = test['html_instructions']
                    liste[k]['mode de transport'] = test['travel_mode']
            self.information_legs = liste #cette liste contient toutes les étapes et les informations utiles (encore à définir)

        else:
            raise TypeError("transport mode not defined, no available routes were found")

       # for i in range(len(Route.dict)):
         #   self._destination_intermediaire.append(self,Route.dict[str(i)])
       # for valeur in Route.dict.keys():
          #  self._transport_mode_intermediaire.append(valeur)





    @property
    def id(self):
        return self._id

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = value

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, value):
        self._destination = value

    @property
    def transport_mode(self):
        return self._transport_mode

    @transport_mode.setter
    def transport_mode(self, value):
        if value in Route.__TRANSPORT_MODES:
            self._transport_mode = value
        elif not isinstance(value, str):
            raise TypeError("Est attendue une chaine de caractère pour le mode de transport.")
        else:
            raise ValueError("La valeur en entrée n'est pas un type de transport possible.")




if __name__ == "__main__":
    """Script de test"""

    # Test des Routes
    # To do