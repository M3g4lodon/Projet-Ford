import requests

exemple_coordonnees=(48.8539837,2.2694961)

def station_depart(depart_GEO):
    hits=0
    i=1
    while hits == 0:
        distance=100*i
        localisation="%2C".join([str(depart_GEO[0]),str(depart_GEO[1]),str(distance)])

        url="https://opendata.paris.fr/api/records/1.0/search/"
        param="dataset=autolib-disponibilite-temps-reel&q=status%3Dok+AND+cars%3E0&geofilter.distance="+localisation

        r = requests.get(url,param)
        results = r.json()

        hits=results['nhits']
        i+=1

    ad_station=results['records'][0]['fields']['address']
    nb_auto = results['records'][0]['fields']['cars']
    distance=results['records'][0]['fields']['dist']
    print("la station la plus proche est {}, à {} mètres.\nIl y a {} autolib disponibles.".format(ad_station,distance,nb_auto))

    return ad_station,nb_auto

def station_arrivee(arrivee_GEO):
    hits = 0
    i = 1
    while hits == 0:
        distance = 100 * i
        localisation = "%2C".join([str(arrivee_GEO[0]), str(arrivee_GEO[1]), str(distance)])

        url="https://opendata.paris.fr/api/records/1.0/search/"
        param="dataset=autolib-disponibilite-temps-reel&q=status%3Dok+AND+charge_slots%3E0&geofilter.distance="+localisation

        r = requests.get(url, param)
        results = r.json()

        hits = results['nhits']
        i += 1

    ad_station=results['records'][0]['fields']['address']
    nb_auto = results['records'][0]['fields']['cars']
    distance=results['records'][0]['fields']['dist']
    print("la station la plus proche est {}, à {} mètres.\nIl y a {} places disponibles.".format(ad_station, distance,
                                                                                                nb_auto))

    return ad_station, nb_auto

station_depart(exemple_coordonnees)
station_arrivee(exemple_coordonnees)