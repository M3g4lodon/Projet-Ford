# Projet-Ford (S3): Comment y aller?

## Installation
Version Python 3.+

Importer la bibliothèque Flask sous Python `pip install Flask`

Navigateur sur lequel le travail a été testé: Mozilla Firefox 56

## Démarrage
Lancer app.py 

Puis rendez vous sur http://127.0.0.1:5000/ avec votre navigateur préféré

## Présentation et Vision du Projet

Groupe: Python 05
Membres: Charles Jacquet, Pierre Monsel et Mathieu Seris. 

Notre projet répond à la problématique posée par l'énoncé S3. Nous calculons et affichons des itinéraires pour des utilisateurs. Chaque utilisateur peut définir ses propres préférences et les trajets proposés seront mis à jour. Nous souhaitions une interface pratique, lisible et fonctionnelle qui puissent au mieux traduire le travail effectué en backend.
L'utilisateur peut choisir d'obtenir des trajets pour des transports en commun (bus et métro), la marche, la conduite, le vélib' ou l'autolib',le vélo ou un taxi. Les préférences utilisateurs (prédéfinies ou personnalisées) permettent d'affiner ce choix de trajet et afficher les itinéraires pertinents. 


## Partie "Back-end" de recherche d'itinéraires

Dans le dossier Backend :
- **Place.py**, contient la classe Place, qui définit un endroit à Paris (par l'adresse ou la longitude/latitude)
- **Itinerary.py** contient la classe Itinerary, notre classe itinéraire de base.
- les fichiers de la forme **Itinerary\_xxx.py** contiennent les sous-classes xxx d'Itinerary
- **User.py** contient la classe User, qui définit un utilisateur, et enregistre ses préférences
- **Suggested\_Itinerary.py** contient la classe éponyme pour proposer à un _utilisateur_ donné, pour un _itineraire_ choisi, des intéraires pertinents pour sa requête.
- **Test.py** contient des tests unitaires sur l'ensemble des fichiers de backend.

### API utilisé
Pour la recherche d'itinéraires, en voiture, à pied, ou à vélo : Google Directions
Pour la recherche d'itineraires en autolib, et vélib : API open Data + Google Directions


## Partie "Front-end"
Partie contenue dans les dossiers Static (**style.css** et **script.js** en javascript) et Template (**Home.html**).

Nous avons utilisé la bibliothèque javascript de génération de cartes de Google Maps.

## Partie Serveur, le lien entre le "Back-end" et le "Front-end"

**app.py** permet l'affichage de la page à partir du template fourni, et la transmission d'informations entre utilisateur final et notre backend, grâce à des appels API (bibliothèque Flask).
