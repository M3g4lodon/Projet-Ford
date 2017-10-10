import requests
import json


# créer un dictionnaire avec les valeurs correspondantes
# mode -> driving walking bicycling transit (departure_time or arrival_time possible) ; possibilite d'utiliser transit_mode ou transit_troute_preference
# JSON: acceder legs in routes
# avoid -> eviter un certain mode de transport/deplacement
# alternatives -> choisir entre plusieurs possibilites
# language -> in which language do you want your result
# departure_time : set to default if not included
# waypoints ...
# avoid = tolls, highways, ferries
# units = metric, imperial


class Itineraire():

    URL_API_DIRECTION = 'https://maps.googleapis.com/maps/api/directions/json?&key=AIzaSyATrZmC9-XjaEAdwtPw6RG0QWV65dbywe0'
    URL_API_GEOCODE = 'https://maps.googleapis.com/maps/api/geocode/json?&key=AIzaSyDpVNzFcwgFfPJOK25P9NlMBL-YEe8bSow'
    KEY_DIRECTION = '&key=AIzaSyATrZmC9-XjaEAdwtPw6RG0QWV65dbywe0'
    KEY_GEOCODE = 'AIzaSyDpVNzFcwgFfPJOK25P9NlMBL-YEe8bSow'

    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination
        self.url_full_direction = Itineraire.URL_API_DIRECTION
        self.url_full_direction = self.url_full_direction + "&origin=" + str(self.origin) + "&destination=" + str(self.destination)
        self.url_content_direction = requests.get(self.url_full_direction).text
        self.url_full_geocode = Itineraire.URL_API_GEOCODE

    def get_distance(self):
        '''Obtenir la distance en km entre le point A et le point B'''
        self.url_full_direction = self.url_full_direction + "&origin=" + str(self.origin) + "&destination=" + str(self.destination)
        self.url_content_direction = requests.get(self.url_full_direction).text
        self.distance = json.loads(self.url_content_direction)['routes'][0]['legs'][0]['distance']['text']
        return self.distance

    def get_time(self):
        '''Obtenir le temps entre le point A et le point B'''
        self.url_full_direction = self.url_full_direction + "&origin=" + str(self.origin) + "&destination=" + str(self.destination)
        self.url_content_direction = requests.get(self.url_full_direction).text
        self.time = json.loads(self.url_content_direction)['routes'][0]['legs'][0]['duration']['text']
        return self.time

    def transit_mode_options(self, mode):
        '''permet a l'utilisateur de choisir son mode de transport (voiture, velo, etc.)'''
        self.url_full_direction = self.url_full_direction + "&mode=" + str(mode)


    def polyline(self):
        a = json.loads(self.url_content_direction)['routes'][0]['overview_polyline']['points']
        return a

    def position_lat_long_origin(self):
        '''calcul la latitude et la longitude de l'adresse d'origine'''
        self.url_full_geocode_origin = self.url_full_geocode + '&address=' + str(self.origin)
        self.url_content_geocode_origin = requests.get(self.url_full_geocode_origin).text
        lat = json.loads(self.url_content_geocode_origin)['results'][0]['geometry']['location']['lat']
        lng = json.loads(self.url_content_geocode_origin)['results'][0]['geometry']['location']['lng']
        # print("latitutde {} ; longitude {}".format(lat,lng))
        return [lat,lng]


    def position_lat_long_destination(self):
        '''calcul la latitude et la longitude de l'adresse d'arrivée'''
        self.url_full_geocode_destination = self.url_full_geocode + '&address=' + str(self.destination)
        self.url_content_geocode_destination = requests.get(self.url_full_geocode_destination).text
        lat = json.loads(self.url_content_geocode_destination)['results'][0]['geometry']['location']['lat']
        lng = json.loads(self.url_content_geocode_destination)['results'][0]['geometry']['location']['lng']
        # print("latitutde {} ; longitude {}".format(lat,lng))
        return [lat,lng]


    def addresse_station_velib_depart(self):
        '''On souhaite ici obtenir l'adresse de la station velib la plus proche de notre point de depart'''

        hits = 0
        i = 1
        depart_geo = Itineraire.position_lat_long_origin(self)
        while hits == 0:
            distance = 100 * i
            depart = "%2C".join([str(depart_geo[0]), str(depart_geo[1]), str(distance)])

            url = "https://opendata.paris.fr/api/records/1.0/search/"
            param = "dataset=stations-velib-disponibilites-en-temps-reel&q=status%3D%3D%22open%22+AND+available_bikes%3E0&geofilter.distance=" + depart

            r = requests.get(url, param)
            results = r.json()

            hits = results['nhits']
            i += 1

        ad_station = results['records'][0]['fields']['address']
        # nb_velo = results['records'][0]['fields']['available_bikes']
        # distance = results['records'][0]['fields']['dist']
        return ad_station


    def addresse_station_velib_arrivee(self):
        '''On souhaite ici obtenir l'adresse de la station velib la plus proche de notre point d'arrivee'''
        hits = 0
        i = 1
        arrivee_geo = Itineraire.position_lat_long_destination(self)
        while hits == 0:
            distance = 100 * i
            depart = "%2C".join([str(arrivee_geo[0]), str(arrivee_geo[1]), str(distance)])

            url = "https://opendata.paris.fr/api/records/1.0/search/"
            param = "dataset=stations-velib-disponibilites-en-temps-reel&q=status%3D%3D%22open%22+AND+available_bikes%3E0&geofilter.distance=" + depart

            r = requests.get(url, param)
            results = r.json()

            hits = results['nhits']
            i += 1

        ad_station = results['records'][0]['fields']['address']
       # nb_velo = results['records'][0]['fields']['available_bikes']
       # distance = results['records'][0]['fields']['dist']
        return ad_station



    def addresse_station_autolib_depart(self):
        '''On souhaite ici obtenir l'adresse de la station autolib la plus proche de notre point de depart'''
        hits = 0
        i = 1
        depart_geo = Itineraire.position_lat_long_origin(self)
        while hits == 0:
            distance = 100 * i
            localisation = "%2C".join([str(depart_geo[0]), str(depart_geo[1]), str(distance)])

            url = "https://opendata.paris.fr/api/records/1.0/search/"
            param = "dataset=autolib-disponibilite-temps-reel&q=status%3Dok+AND+cars%3E0&geofilter.distance=" + localisation

            r = requests.get(url, param)
            results = r.json()

            hits = results['nhits']
            i += 1

        ad_station = results['records'][0]['fields']['address']
        # nb_auto = results['records'][0]['fields']['cars']
        # distance = results['records'][0]['fields']['dist']
        # print("la station la plus proche est {}, à {} mètres.\nIl y a {} autolib disponibles.".format(ad_station, distance, nb_auto))

        return ad_station


    def addresse_station_autolib_arrivee(self):
        '''On souhaite ici obtenir l'adresse de la station autolib la plus proche de notre arrivee'''
        hits = 0
        i = 1
        arrivee_geo = Itineraire.position_lat_long_destination(self)
        while hits == 0:
            distance = 100 * i
            localisation = "%2C".join([str(arrivee_geo[0]), str(arrivee_geo[1]), str(distance)])

            url = "https://opendata.paris.fr/api/records/1.0/search/"
            param = "dataset=autolib-disponibilite-temps-reel&q=status%3Dok+AND+charge_slots%3E0&geofilter.distance=" + localisation

            r = requests.get(url, param)
            results = r.json()

            hits = results['nhits']
            i += 1

        ad_station = results['records'][0]['fields']['address']
        # nb_auto = results['records'][0]['fields']['cars']
        # distance = results['records'][0]['fields']['dist']
        #print(
         #   "la station la plus proche est {}, à {} mètres.\nIl y a {} places disponibles.".format(ad_station, distance, nb_auto))

        return ad_station


if __name__ == "__main__" :

    #Creation d'un objet Trajet

    Trajet=Itineraire("10 rue saint-didier paris 75116","10 rue oswaldo cruz paris 75016")

    #On verifie le temps entre le point A et le point B

    print(Trajet.get_time())

    # On verifie la distance entre le point A et le point B

    print(Trajet.get_distance())

    # On verifie que l'on peut bien choisir son mode de transport (walking)et obtenir des chiffres (distance/temps) différents que ceux ci-dessus

    Trajet.transit_mode_options("walking")
    print(Trajet.get_distance())
    print(Trajet.get_time())

    #On verifie la latitude et la longitude de notre point de depart/d'arrivee

    print(Trajet.position_lat_long_origin())
    print(Trajet.position_lat_long_destination())

    # On verifie l'adresse de la station autolib la plus proche de notre point de depart

    print(Trajet.addresse_station_autolib_depart())

    # On verifie l'dresse de la station autolib la plus proche de notre destination

    print(Trajet.addresse_station_autolib_arrivee())

    # On verifie l'adresse de la station velib la plus proche de notre point de depart

    print(Trajet.addresse_station_velib_depart())

    # On verifie l'adresse de la station velib la plus proche de notre destination

    print(Trajet.addresse_station_velib_arrivee())







