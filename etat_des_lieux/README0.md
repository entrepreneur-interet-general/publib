# Pilote MD

Dans une logique d'état des lieux et d'étude de faisabilité  avec POC
un double travail est en cours:
* Etude de la chaine de production des métadonnées dans le périmêtre couvert par ADCAT02
(Demande MET: ajout des flux externes types OniX et autres fonds (optique FNE))
Au programme:
  * analyse des flux d'entrée (filière et chaine d'acquisition) auprès des experts métiers et DSI
  * règles de validation et Conversion
  * insertion en base et modèle logique de données
  * Enrichissement par saisie et par flux (ADCAT 02 ADCAT06)
  * Diffusion
* Développement exploratoire avec deux autres systèmes de SGBD:
découverte de InterXmarc et de la diversité des métadonnées
analyse de l'impact du changement de SGBD sur:
- l'insertion des données (unique + multiples)
- la validation des données (RIM + règles logiques)
- l'ajout de clés descriptives supplémentaires des données (cadre du chantier sur l'évolution vers InterMarc NG) dans le temps:
rétrocompatibilité et  cohérence du modèle de données avec usages. (ajout par exemple de la provenance et de l'info de stockage)
- la recherche et la sélection des données
- la modification, l'enrichissement et la correction d'une ou plusieurs notices


## Défi BNF:
Pistes d'intervention en 8 mois
* PISTE 1 :ETL
 ETL unifié pour les différentes chaines d'entrée des métadonnées
Une même logique d'acquisition pour chaque chaine, des règles spécifiques pour chaque type, source, filière et besoin métier ( a identifier de manière exhaustive)
Des convertisseurs  et adaptateurs génériques pour les différents flux.
En simple Un mode d'insertion unique des md dans pilote MD
Et un mode de sortie unique des md dans pilote MD?
> Mise de coté pour question d'intégration SI

* PISTE 2 : API FNE
Décorreler les notices bibliographiques des notices d'autorité et voir comment synchroniser et éditer les notices
* PISTE 3: TAM Prototype d'accès et de modification des données en paquets + versionning des modifications
* PISTE 4 : RIM NG
Outil de visualisation des évolutions et usage du Référentiel InterMarc + ajout/suppression de règles
* PISTE 5:  EXO REF
Enrichissement semi-automatique de notices pour suggestions dans ProdMD (la production des MD du catalogue)
suggestions issues de 2 endroits: interne (notices existantes), externes (API pour des zones spécifiques: exemple lieux, PEP)

## PISTE 1
Cette piste de développement est partie d'un constat: la diversité des flux et circuits d'entrée dans la production du catalogue
qui fait l'objet d'un travail d'état des lieux exhaustif en terme fonctionnels et techniques à travers la discussion et la rencontre des personnes impliquées.

Une autre manière de faire un état des lieux est de se pencher sur l'existant et de voir ce que cela produit,
en terme de modèle logique de données (déjà disponible et documenté à travers 2 choses:
  * le RIM (et le manuel KITKAT))
 * les champs de la Base de données deprodMD)

Cela permet aussi de se familiariser avec la syntaxe et le vocabulaire InterMarc.
Et peut être d'ajouter aux Ateliers de reflexion sur InterMarc NG, une vision de l'usage effectif qui en est fait.

Pour cette pise, je souhaiterais explorer un autre Système de Gestion de Base de données:
- NoSQL (Mongo ou ElascticSearch)
ou évaluer l'opportunité d'un système mixte PostgresQL (JSONB Nodes)
Exploration BIG  CAT

### Premier développement liminaire envisagé: EXPLORATION BIG CAT
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


##### Remarques
Format Intermarc complexe:
- Zones et sous Zones à position ou avec des champs
La parti-pris pour le moment est d'applatir la hiérarchie de l'Intermarc et de se passer de conversion pour le moment.

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

##### Autres developpements envisagés

- Des silos différents: 100.000 par 100.000
- Sampling de 1% représentatifs
- Atomiser les notices?


Autres reflexions:
- Mettre les pex avec le numero de notices dans une autre collection NON
- Recréer la logique de mise à jour ou création de notices d'autorité immédiate
- Indexer les champs les plus usités
