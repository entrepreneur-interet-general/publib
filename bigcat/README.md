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

- Des silos différents: 100.000 par 100.000
- Sampling de 1% représentatifs
- Atomiser les notices?


Autres reflexions:
- Mettre les pex avec le numero de notices dans une autre collection NON
- Recréer la logique de mise à jour ou création de notices d'autorité immédiate
- Indexer les champs les plus usités


Quelques explications

## 1. Modèle de données pour Mongo ##

Mongo est un SGBD orienté document, j'ai donc fait le choix de faire un test:
mettre toutes les notices interXmarc disponibles dans un seule base de données
et dans une seule table (appelée collection) `catalogue.notices` via le script: exploration.py

* en *applatissant* la structure XML  de la notice  du format [Intermarc](http://www.bnf.fr/fr/professionnels/f_intermarc/s.format_intermarc_biblio.html)

le champ des notices est donc composé et stocké ainsi:
` { <zone>$<sous_zone>P<position>: valeur} `

* en permettant pour **certaines zones** les valeurs multiples en **liste** et parfois en liste de dictionnaires:
  * les pex
  * les données de gestion

* en transformant des valeurs textuelles en types de données informatiques (cast)
  * les dates seront au format date (datetime.date)
  * les nombres (integer, float, long)
  * les textes (string) avec controle automatique de taille autorisé


Pour valider la faisabilité de plusieurs pistes:

* permettre les controles de validations ultérieurs date, range, taille de texte autorisé [RIM NG]
* tester le *report de forme* [API FNE]
* tester le traitement massif multidocument et l'idnexation [TAM]
* tester la mise à jour automatique des referentiels exogènes [REF EXO]



## 2. Mise à l'échelle verticale

Après quelques tests, et quelques pertes de données de la BDD,
la première solution a été de transférer la bse sur un serveur de développement plus puissant.
C'est une opération de **mise à l'échelle verticale** qui implique deux opérations:
- la réinsertion des  données de catalogue qui ont survécu au crash du système (Notices d'autorité).
- la réindexation des données de catalogue depuis les notices
Pour des tests de performances plus avancé

* Dump des notices d'autorité depuis la base préexistante:
 ```
$ mongo catalogue
> db.aut.count()
> 5428385
 ```
par export et non par dump (plus verbeux):

 ```
 mongoexport -d catalogue -c aut -o notices_aut.json
 ```

* Retraitement dans la BDD mongo de reception:


**IDentifiant de notices**

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

** Type de notice **
On distingue deux grand type de notices:
* Autorité
* Bibliographique
<record Numero="42008009" format="InterXMarc_Complet" type="Bibliographic">

## 3. Mise à l'échelle horizontale

La particularité du NoSQl base de données orientée documents est de permetre la mise à l'échelle horizontale
en répartissant une seule collection sur plusieurs *shards* en cluster
pour permettre de répartir l'espace de stockage et la capacité de calcul.
Sur le concept du sharding https://docs.mongodb.com/v3.0/core/sharding-introduction/


*Les SGBD avec de gros datasets  et de nombreuses applications (modifications multiples en concurrences) peuvent
mettre à l'épreuve les capacité d'un serveur unique*
