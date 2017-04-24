# PISTE: Referentiels exogènes

## Contexte
La BNF est un organisme qui produit un ensemble de notices bibliographiques issus
du dépot légal et des commandes émises par la direction des collections.
Chaque notice est codée dans un format interne à la BNF Intermarc: un format xml structuré par zone et sous zone qui décrivent pour l'humain et la machine les informations nécessaires à l'identification **en interne** d'un ouvrage ou d'une autorité (vedette matière, auteur, sujet, etc..)
et **en externe** par les organismes partenaires.
Ces informations bibliographiques suivent donc un ensemble de règles de classement
qui s'alignent avec les standards internationaux.

### Etat de l'art
Ce développement a pour but de faciliter le travail des normalisateurs, catalogueurs
qui gèrent ces référentiels. Ces référentiels externes sont aujourd'hui mis à jour à la main par le chargé du référentiel qui envoie ensuite une DPI au service de la DSI CED (Cellule des données) qui modifie les valeurs dans le modèle logique de données ainsi que dans le système de gestion des règles de catalogage.

Ces référentiels impactent les valeurs contenues dans les notices pour certains codes de zones au moment de leur mise à jour. Les valeurs qui décrivent une notice contenue dans le catalogue reflète le référentiel à la date de modification sans qu'il y ait 'conversion rétrospective', c'est à dire mise à jour des valeurs du référentiel dans tous le catalogue au moment de la modification.

### Spécifications fonctionnelles

L'objectif de ce développement pilote est de permettre aux normalisateurs, correcteurs et catalogueurs:
* d'avoir une **vision d'ensemble des référentiels** et une vue détaillée du référentiel qu'ils gèrent au travers d'un tableau de bord.

Deux vues doivent être disponibles à la consultation, la modification et la mise à jour par les utilisateurs habilités:

* La vue **globale** appelée ici `référentiel master` (tous les référentiels confondus)
qui contienne la liste exhaustive des référentiels externes

* La vue **spécifique** pour un référentiel donné appelée ici referentiel spécifique

Aujourd'hui cette gestion se fait par transfert, modification, conversion et de fichiers pdf qui reproduisent des exports d'une table de la Base de données Catalogue (PCN). La mise à jour du guide du catalogueur (en ligne) se fait ensuite manuellement après échange par mail et validation de DPI.

Une plateforme web intégrée de gestion des référentiels (modification, validation, mise en conformité des règles et modification de la base Catalogue) permettrait aux différents acteurs et responsables de la production catalogue de suivre, controler en temps réel la qualité des champs des notices controlés par des référentiels externes.

### Référentiel Master

> Le référentiel des référentiels

Le référentiel master renvoie l'ensemble des informations communes  à tous les référentiels: leur gestion globale

  * le nom et l'identifiant du référentiel
  ```json
  { "nom": "code_pays",
    "id_ref": 0,
    "description": "Code à deux caractères désignant un pays contemporain.",
    "type": "liste|code" # prendre la dénomination originelle
  }
  ```
  * les zones bibliographiques touchées par ce référentiel
  ``` json
  zones: [
  "A8P12-14",
  "B4P1",
  "B8P28-30",
  "B21$p",
  "B25$p",
  "B314$p"
  "B316$p",
  "B40$a",
  "A40$a",
  ]
  ```

  * le ou les responsables de ce référentiel
  > Ici penser à utiliser les modes d'identification des perssonnes interne à la BN
  > Quels niveaux d'information Organisme? Habilitation? Role?

  ```json
  responsables :[
  "c24b",
  "bem",
  ]
  ```

  * les dates de mise à jour du référentiel
  ```
  version:{"date": "01/01/2013", "ref": "3166-1A2:2013"}
  ```
  * l'historique de modification du référentiel

  > calculé a partir des opérations faites sur le référentiel?

  ```json
  history :[{ "before":"fr=franse",  
              "after":"fr=france",
              "author": "c24b",
              "date":"09/12/2015",
              "operation": "correction"
            },
            {"before":"",  
            "after":"bg=bengale",
            "author": "c24b",
            "date":"17/02/2016",
            "operation": "ajout",
            },
            ]
  ```

  * le mode de mise à jour du référentiel
  ```json
  { "sync_mode": "automatic|manuel",
    "source": "https://restcountries.eu/"}
  ```
  * le standard et les responsables du standard
  ```json
  standard: {
    "code":"ISO 3166-1 alpha2",
    "maintainer":"https://www.iso.org/standard/63545.html",
    "reference": "https://www.iso.org/obp/ui/#search"
  }
  ```

Un tableau récapitulatif sous forme de tableau de bord web.
Il pourra ainsi etre corrigé, modifié, mis à jour et consulté facilement **en ligne** par les responsables de chaque référentiel.

> **Next Step** Rappatrier les règles de gestion de ADCAT 90 pour chaque zone et sous zones en vérifiant les interdépendances

### Référentiel spécifique

> Exemple: le référentiel codePays

Le référentiel spécifique renvoie toutes les informations détaillées du référentiel soit a liste des codes/valeurs. Les informations ajoutées sont placées au niveau du code et de sa valeur

``` json

{"fr": "France",
"ref_name": "codePays",  
"date":[2017/01/06,2003/01/01],
"operations":["mise à jour", "création"],
"author":["c24b", "bem"],
"rule": "fixed"
}
{ "gb": "Grande Bretagne",
  "ref_name": "codePays",  
  "date":[2017/01/06,2003/01/01],
  "operations":["mise à jour", "création"],
  "author":["c24b", "bem"],
  "rule": "sync"  
}

```
> **Next Step** Les labels par défault ne sont pas indiqués pour le moment
dans le cas des CodePays la norme défini les labels  dans 3 langues et la BNF n'utilise que le code en français avec quelques variations parfois dans l'écriture ex {"gb": {"en": "Great Britain", "fr": "Grande-Bretagne"}}


### Objectifs
 1. Création et mise à jour de la table master des référentiels:

    1.1. Créer la table de référentiel master initiale

    1.2. Créer une interface pour la consultation et l"édition en ligne

2. Création et mise à jour de chaque référentiel

    2.1. Créer la table de chaque référentiel
    2.2.  Créer une interface pour la consultation et l'édition en ligne de chaque référentiel
 * quand ceux-ci sont définis en interne: les fixer
 * quand ceux ci sont défini par des normes: proposer une methode de synchronisation
 depuis le standard ou affilié

3. Proposant une interface pour gérer les conflits de synchronisation et l'autentification des responsables des référentiels
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
=> Création d'une base de données de ref
=> Exposition des valeurs
=> Edition des valeurs

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


#### code pays
* Norme
(https://restcountries.eu)









ou directement de http://www-01.sil.org/iso639-3/chg_detail.asp?id=2017-002

- code pays:
https://restcountries.eu/rest/v2/alpha/col
LANGUE => PAYS
https://restcountries.eu/rest/v2/lang/es
<!-- https://restcountries.eu -->
