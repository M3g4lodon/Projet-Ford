#Paris WOEID code is 615702 (documentation de l'API: https://developer.yahoo.com/weather/documentation.html)

import requests

#temperature actuelle et visibilité
url="https://query.yahooapis.com/v1/public/yql"
param="q=select%20item.condition%20from%20weather.forecast%20where%20woeid%20%3D%20615702%20and%20u%3D'c'&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"


#5 days forecast incl. temperature, humidity...
#url="https://query.yahooapis.com/v1/public/yql"
#param="q=select%20*%20from%20weather.forecast%20where%20woeid%20%3D615702%20and%20u%3D'c'&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="

resp = requests.get(url,param)
r=resp.json()

code=r['query']['results']['channel']['item']['condition']['code']
temperature=r['query']['results']['channel']['item']['condition']['temp']
temps=r['query']['results']['channel']['item']['condition']['text']

if code not in [19-34,36]:
    print("temps pourri, utilisez les transports couverts")

print("il fait {}, et le temps est {}".format(temperature,temps))