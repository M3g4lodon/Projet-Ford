#TODO Faire les exceptions et revoir la terminaison des attributs ?
#TODO Bien faire les distances pour l'affichage
#TODO Quid de simplifier le code = la distance et el temps devraient etre les memes pour chaque type d'uber
#TODO Faire des getter et des setters pour notamment: transit_mode_type (changer de type d'uber)

import requests
from Itinerary import Itinerary
from Place import Place
import math


class Uber(Itinerary):

    __UBER_API_PRICE = 'https://api.uber.com/v1.2/estimates/price?'
    __UBER_API_TIME = 'https://api.uber.com/v1.2/estimates/time?'

    def __init__(self, origin, destination, date=None, transit_mode_type=None, itinerary_index=0):
        Itinerary.__init__(self, origin, destination, date, transit_mode_type, itinerary_index)
        self.transit_mode = "uber"

        # j'avais très envie de mettre uberberline par défaut
        if self.transit_mode_type is None:
             self.transit_mode_type = "uberx"

        self.information_legs_uber = []
        self.uber_wait_duration = 0
        self.uber_travel_duration = 0
        available_options = []

        #Code Spécifique à l'API UBER

        headers = {'Authorization':'Token 1QTK0iskAoX7vFZ3Ir1j_NdqnADK7zXAF4GcaRLe','Accept-Language':'en_US',"Content-Type":"application/json"}
        url_request_price = Uber.__UBER_API_PRICE
        url_request_price += 'start_latitude=' + str(self.origin.lat) + '&start_longitude=' + str(self.origin.lng) + '&end_latitude=' + str(self.destination.lat) + '&end_longitude=' + str(self.destination.lng)
        url_request_time = Uber.__UBER_API_TIME
        url_request_time += 'start_latitude=' + str(self.origin.lat) + '&start_longitude=' + str(self.origin.lng) + '&end_latitude=' + str(self.destination.lat) + '&end_longitude=' + str(self.destination.lng)

        raw_data_price = requests.get(url = url_request_price, headers = headers).json()
        raw_data_time = requests.get(url = url_request_time, headers = headers).json()

        options_price = raw_data_price['prices']
        options_time = raw_data_time['times']
        print(len(options_price),len(options_time))

        #les estimations temps et prix ne sont pas toujours identiques. On veut prendre l'intersection des deux. D'où la disjonction de cas un peu moche...

        if len(options_price)<=len(options_time):

            for uber_option, option in enumerate(options_price):
                self.information_legs_uber.append({})
                self.information_legs_uber[-1]['uber_name'] = str(option['display_name']).lower()
                available_options += str(option['display_name']).lower()
                self.information_legs_uber[-1]['price'] = option['estimate']
                self.information_legs_uber[-1]['distance'] = option['distance']
                self.information_legs_uber[-1]['duration'] = option['duration']

                if options_time[uber_option]['display_name'] == option['display_name']:
                    self.information_legs_uber[-1]['wait_time'] = options_time[uber_option]['estimate']




                if self.information_legs_uber[-1]['uber_name'] == self.transit_mode_type:

                    self.price = self.information_legs_uber[uber_option]['price']
                    self.uber_wait_duration = self.information_legs_uber[uber_option]['wait_time']
                    self.uber_travel_duration = self.information_legs_uber[uber_option]['duration']
                    self.total_duration = self.uber_wait_duration + self.uber_travel_duration
                    self.driving_distance = int(self.information_legs_uber[uber_option]['distance']*1610) #l'appli renvoie des miles et non des km


        else:
            for uber_option, option in enumerate(options_time):
                self.information_legs_uber.append({})
                self.information_legs_uber[-1]['uber_name'] = str(option['display_name']).lower()
                available_options += str(option['display_name']).lower()
                self.information_legs_uber[-1]['wait_time'] = option['estimate']


                if options_price[uber_option]['display_name'] == option['display_name']:
                    self.information_legs_uber[-1]['price'] = options_price[uber_option]['estimate']
                    self.information_legs_uber[-1]['distance'] = options_price[uber_option]['distance']
                    self.information_legs_uber[-1]['duration'] = options_price[uber_option]['duration']

                if self.information_legs_uber[-1]['uber_name'] == self.transit_mode_type:
                    self.price = self.information_legs_uber[uber_option]['price']
                    self.uber_wait_duration = self.information_legs_uber[uber_option]['wait_time']
                    self.uber_travel_duration = self.information_legs_uber[uber_option]['duration']
                    self.total_duration = self.uber_wait_duration + self.uber_travel_duration
                    self.driving_distance = int(float(self.information_legs_uber[uber_option]['distance'])*1610) #l'appli renvoie des miles et non des km

        if self.transit_mode_type not in available_options:
            TypeError("The Uber option you selected isn't available. Please select another option or try again later.")

        print(self.information_legs_uber)

    #J'ai décidé d'override celle de la classe mère, plus facile (on n'utilise pas google maps ici...)
    def __repr__(self):

        res = ""
        res += "Here is the summary of your Uber Trip:"
        res += "\n"
        res += "Your uber will be arriving in " + str(math.floor(self.uber_wait_duration / 60 + 1)) + "min."
        res += "\n"
        res += "Your ride will take you " + str(math.floor(self.uber_travel_duration / 60 + 1)) + "min and " + str(self.driving_distance) + " meters to arrive at destination."
        res += "The fare estimate is " + str(self.price)

        return res

if __name__ == "__main__":
    """Script de test"""

    # Test des itinéraires
    org = Place(address="Porte de Passy")
    des = Place(address="Porte de la Villette")
    AtoB = Uber(org, des, transit_mode_type="uberx")
    print(repr(AtoB))



