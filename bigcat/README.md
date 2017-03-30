# Modele BDD: Big CAT

Test initial avec Mongo DB.
### Intro
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

- Des silos différents: 100.000 par 100.000? => sharding une fois l'échantillon fait?
- Sampling de 1% représentatifs
- Atomiser les notices?


Autres reflexions:
- Mettre les pex avec le numero de notices dans une autre collection NON
- Recréer la logique de mise à jour ou création de notices d'autorité immédiate OUI après
- Indexer les champs les plus usités OUI ensuite
- Créer un service de mise à jour à partir des referentiels externes


Quelques explications

## 1. Modèle de données pour Mongo ##

Mongo est un SGBD orienté document, j'ai donc fait le choix de faire un test:
mettre toutes les notices interXmarc disponibles dans un seule base de données
et dans une seule table (appelée collection) `catalogue.notices` via le script: exploration.py

* en *applatissant* la structure XML  de la notice  du format [Intermarc](http://www.bnf.fr/fr/professionnels/f_intermarc/s.format_intermarc_biblio.html)
voir un exemple de notices bibliographique au format interXmarc: [./exampleB.xml]
voir un exemple de notices d'autorité au format interXmarc:  [./exampleA.xml]



* en permettant pour **certaines zones** les valeurs multiples en **liste** et parfois en liste de dictionnaires:
  * les pex
  * les données de gestion

* en transformant des valeurs textuelles en types de données informatiques (cast)
  * les dates seront au format date (datetime.date)
  * les nombres (integer, float, long)
  * les textes (string) avec controle automatique de taille autorisé

  le champ des notices est donc converti et transposé en json et stocké ainsi:
  ` { <zone>$<sous_zone>P<position>: valeur} `
  y sont ajouté au meme niveau les données de gestion
  ainsi que les parties d'exemplaires sous forme de liste de dictionnaires
  un exemple de notice d'autorité (certains champs ont été offusqués pour des raisons de confidentialité)

L'objectif est de valider la faisabilité de plusieurs pistes:

* permettre les controles de validations ultérieurs date, range, taille de texte autorisé [RIM NG]
* tester le *report de forme* [API FNE]
* tester le traitement automatisé massif/multidocument et l'indexation [TAM]
* tester la mise à jour automatique des referentiels exogènes [REF EXO] selon un même réferentiel




## 2. Mise à l'échelle verticale

Après quelques tests, et quelques pertes de données de la BDD,
la première solution implique de transférer la base sur un serveur de développement plus puissant.
C'est une opération de **mise à l'échelle verticale** qui implique de traiter les notices interxmarc:
- leur retraitements:
    - cast de type
    - indexation des pexs
    - vérification des notices

- l'ajout de valeurs multiples aggrégées après insertion dans la base

```
#historique des modifications
"history":[{"user":<user>, "date":<dt>, "action":<action_type:signalement|edition|validation|import>, "type": <action_type>]}, ...},
#status de la notice
"status": "<validé|confirmé|en attente>"
#on distingue la source de l'origine
#la source marque l'institution initiale de provenance du document
"source": {"org": "", "country":"", "lang": }
#l'origine indique le point d'entrée dans la chaine de traitements qui ont permis le versement de la notice
"origin": {"org": "", "channel":"", "action":"<manual|import|update>"}
"doc_type":""

```

Pour des tests de performances plus avancé

#Insertion initiale en base
* Dump des notices depuis la base préexistante:
 ```
$ mongo catalogue
> db.notices.count()
> 18 360 944
> db.logs.count()
> 29
```
par export c'est plus verbeux et complet car les index seront sauvegardés

 ```
 mongoexport -d catalogue -c aut -o notices_aut.json
 ```
trop lourd donc à découper selon une logique soit volumétrique soit par paramêtre

Choix de réinsérer les notices
#Deuxième insertion en Base
Les données vont etre versées depuis le puis des notices dans une BDD Mongo
- parser le xml
- applatir l'arborescence des zones sous zones et positions
- transformation des valeurs en nombre et en dates en fonction de leur nom
- insertion

Une fois la base constituée: de multiples corrections sont à prévoir et au cas par cas

Quelques indications sur les clés des documents

* **IDentifiant de notices**

Pour le moment, l'**id** unique de la notice correspond au numéro de notices
 (non perenne) il sera à terme remplacé par le nom [ark](http://www.bnf.fr/fr/professionnels/issn_isbn_autres_numeros/a.ark.html)

Dans notre premier [exemple](./exempleB.xml) cet identifiant corresond à la fois
au numéro présent dans la notice :

 `<record Numero="42008009" format="InterXMarc_Complet" type="Bibliographic"> `

et au nom du fichier xml  `42008009.xml`


Pour rappel l'ARK est utilisé pour deux types de ressources à la BnF :

     * Les documents numériques (préfixe "b"), cf. par exemple
     http://gallica.bnf.fr/ark:/12148/bpt6k107371t

     * Les notices bibliographiques (préfixe « c »), cf. par exemple
     http://catalogue.bnf.fr/ark:/12148/cb31009475p

Dans notre cas, seules les notices bibliographiques nous intéressent pour la partie identififiant de la notice. Des id ark pourront être rattachés au PEX (Partie d'Exemplaire)

* ** Type de notice **
On distingue deux grand type de notices:
  * Autorité
  * Bibliographique
<record Numero="42008009" format="InterXMarc_Complet" type="Bibliographic">

* Les autres informations liées aux notices seront mappées a partir des code de zones une fois l'insertion faite

## 3. Mise à l'échelle horizontale

La particularité du NoSQl base de données orientée documents est de permetre la mise à l'échelle horizontale
en répartissant une seule collection sur plusieurs *shards* en cluster
pour permettre de répartir l'espace de stockage et la capacité de calcul.
Sur le concept du sharding https://docs.mongodb.com/v3.0/core/sharding-introduction/


*Les SGBD avec de gros datasets  et de nombreuses applications (modifications multiples en concurrences) peuvent
mettre à l'épreuve les capacité d'un serveur unique*
