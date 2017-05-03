### RIM NG
Un outil statistique sur les données existantes qui s'affranchisse des indexations de la BDD existante.
Soit en utilisant les notices InterXMARC
1. Détecter:
- les clés obligatoires,
- les interdépendances de zones
Pour identifier des 'types' ou famille de métadonnées:
quels règles spécifiques?
quels champs spécifiques?
quels évolutions dans le temps?
par une approche par l'usage et reboucler sur les Ateliers INterXMARC et les traitements de conformité faits au BEA (Contact Sylvie Florès)

Pour cela un proto d'exploration et d'indexation dans MONGO
cf ./exploration.py



1. Analyse fréquentielle simple:
permet de définir les champs obligatoires des notices
et les champs les plus / moins utilisés
A plusieurs niveaux:
zones
sous zones...
position

2. Analyse factorielle de correspondances
définir les interdépendances de champs

3. Modelisation du shema de dépendances créé par le format
Cartographier la norme par type de données et chaine d'entrée....
