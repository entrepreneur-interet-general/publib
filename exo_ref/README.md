# PISTE: Referentiels exogènes

## Objectifs
 1. Mise à jour de l'ensemble des référentiels externes
 2. En figeant les valeurs spécifiques liés au catalogage interne
 3. En proposant une interface pour gérer les conflits de merge
 4. En mettant à jour les notices BIB et AUT concernées


## Datasets

Nous disposons de plusieurs datasets:
* Un document **master** qui liste l'ensemble des référentiels externes pour chaque format(type de notice), zone, sous zone position et type de notice concernée ainsi que la date de dernière modification
* Un ensemble de document **spécifiques pour chaque référentiels**. Ils listent
le code attribué et la valeur correspondante. Selon le référentiel, on peut trouver des informations complémentaires telles que:
  * le détail de la  modification d'une valeur (date, remplacement)
  * la norme sur laquelle repose le référentiel
  * les valeurs locales (spécifique à la BNF) qui remplacent les valeurs globales

    ` A noter: les normes ISO sont disponibles en ligne et pourraient etre mise à jour automatiquement
    en respectant la priorité des données locales (soit les valeurs spécifiques figées par la BNF)
    `
* L'**ensemble des notices concernées** par ses référentiels exogènes: l'information est qualifiée par chaque zone,sous-zone, position et "type"  de notice et la valeur  peut être présente à plusieurs endroits.

## BackLog

* Création d'une base de connaissance qui croise chaque référentiel externe avec les valeurs du document master (format, zone, sous-zone, position)
`tag:master_ref`
* Création d'une API de requetage de ces données pour chaque valeur controlée `tag:requete`
* API de requetage des référentiels exogènes `tag:exo_api`
* Gestion des versions/modifications: stockage dans une BDD `tag:versionning`

### Master_ref

En v0.1 **création d'un fichier XLS à plat** caractérisé comme suit
pour chaque code son référentiel correspondant pour prise de connaissance
globale de la base

En v0.1.1 identifier les valeurs à mettre à jours depuis l'extérieur
accessible depuis une API en prenant un exemple: le code de langue
et en croisant le référentiel BNF avec le normalisateur officiel
dans `/api/lang`
Etapes:
1. Récupérer le dataset externe et interne via un script et stockage dans `/api_lang/data`
2. Comparer et fusionner avec le ref BNF: déterminer les valeurs locales et les valeurs prioritaires
3. Ouvrir une route api pour questionner le réf externe en temps réel?
4. Ouvrir une route api pour questionner la base fusionnée
5. Ouvrir une route api pour la MàJ en temps réel

Problème:
Le normalisateur officiel bLoque l'acces depuis une adresse virtuelle:
Unauthorized




#### code langue

Elle suit la norme ISO 639-2 Alpha 3 et est officiellement maintenue par la
Library of Congress


* Source officielle:
http://id.loc.gov/ Library of Congress
mais **bloqué depuis la VM**

* Sources alternatives:
http://www-01.sil.org/iso639-3/codes.asp?order=639_2&letter=a

* Anciennes versions officielles:
https://www.loc.gov/standards/iso639-2/php/code_list.php html [derniere MàJ 2012]
https://www.loc.gov/standards/iso639-2/ISO-639-2_utf-8.txt txt [dernière MàJ 2010]

* Evolution de la la norme
http://www.loc.gov/standards/iso639-2/php/code_changes.php

* Mise à jour d'un code de langue à la fois?
http://id.loc.gov/vocabulary/iso639-2/<code_lang>.skos.json

Bloqué depuis la VM
1. Création du dataset externe de base:
bloqué par la VM et le proxy
recours à la version alternative du SIL
dans build_lang_code.py

2. Création de l'api


####s code pays
* Norme
(https://restcountries.eu)









ou directement de http://www-01.sil.org/iso639-3/chg_detail.asp?id=2017-002

- code pays:
https://restcountries.eu/rest/v2/alpha/col
LANGUE => PAYS
https://restcountries.eu/rest/v2/lang/es
<!-- https://restcountries.eu -->
