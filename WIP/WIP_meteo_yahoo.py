#Paris WOEID code is 615702 (documentation de l'API: https://developer.yahoo.com/weather/documentation.html)

import requests
import datetime
from user_v2 import User

def meteo_jour(utilisateur):
    #5 days forecast incl. temperature, weather,...
    url="https://query.yahooapis.com/v1/public/yql"
    param="q=select%20*%20from%20weather.forecast%20where%20woeid%20%3D615702%20and%20u%3D'c'&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="

    resp = requests.get(url,param)
    r=resp.json()

    for i in range (0,4):
        if date == datetime.date.today() + datetime.timedelta(days=i):
            forecast=r['query']['results']['channel']['item']['forecast'][i]
            #print(forecast)

            code=int(forecast['code'])
            texte=forecast['text']
            max=forecast['high']
            min=forecast['low']
            info="Le temps sera: {}, la température comprise entre {} et {}°C.".format(texte,min, max)

            if 19 <= code<= 34 or code==36:
                resultat="Tous les moyens sont bons ! "+info
            else:
                resultat="\nUtilisez les moyens de transport couverts. "+info
                pref=list(utilisateur.preferences) # preferences de l'objet de classe utilisateur -> a modifier par rapport a la fct
                if 'velib' in pref:
                    pref.remove('velib')
                if 'walking' in pref:
                    pref.remove('walking')
                utilisateur.preferences=pref

            return print(resultat)

if __name__=="__main__":

    date = datetime.date.today()+ datetime.timedelta(days=3)
    charles = User("Touriste", "non")
    meteo_jour(charles)
    print(charles.preferences)
