import requests

exemple_coordonnees=(48.8539837,2.2694961)

def station_depart(depart_GEO):
    hits=0
    i=1
    while hits == 0:
        distance=100*i
        depart="%2C".join([str(depart_GEO[0]),str(depart_GEO[1]),str(distance)])

        url="https://opendata.paris.fr/api/records/1.0/search/"
        param="dataset=stations-velib-disponibilites-en-temps-reel&q=status%3D%3D%22open%22+AND+available_bikes%3E0&geofilter.distance="+depart

        r = requests.get(url,param)
        results = r.json()

        hits=results['nhits']
        i+=1

    ad_station=results['records'][0]['fields']['address']
    nb_velo = results['records'][0]['fields']['available_bikes']
    distance=results['records'][0]['fields']['dist']
    print("la station la plus proche est {}, à {} mètres.\nIl y a {} vélos disponibles.".format(ad_station,distance,nb_velo))

    return ad_station,nb_velo

def station_arrivee(arrivee_GEO):
    hits = 0
    i = 1
    while hits == 0:
        distance = 100 * i
        depart = "%2C".join([str(arrivee_GEO[0]), str(arrivee_GEO[1]), str(distance)])

        url = "https://opendata.paris.fr/api/records/1.0/search/"
        param = "dataset=stations-velib-disponibilites-en-temps-reel&q=status%3D%3D%22open%22+AND+available_bike_stands%3E0&geofilter.distance=" + depart

        r = requests.get(url, param)
        results = r.json()

        hits = results['nhits']
        i += 1

    ad_station = results['records'][0]['fields']['address']
    nb_velo = results['records'][0]['fields']['available_bike_stands']
    distance = results['records'][0]['fields']['dist']
    print("la station la plus proche est {}, à {} mètres.\nIl y a {} ports disponibles.".format(ad_station, distance,
                                                                                                nb_velo))

    return ad_station, nb_velo