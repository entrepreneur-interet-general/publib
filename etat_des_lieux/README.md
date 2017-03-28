# Etat des lieux

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

## Quelques développements en passant
* jargon
* convertisseur
* schema du circuit de production des MD

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
