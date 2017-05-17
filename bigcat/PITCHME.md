# BIG CAT
####*Modélisation des métadonnées du catalogue*

---
## Défi EIG initial

Préfigurer une plateforme de **co-production de données bibliographiques**
qui permette la collaboration
en temps réel avec d'autres institutions

---

## Contexte du projet

Ce projet s'inscrit dans une feuille de route de développement à 4 ans

Développement de **pilote MD**

* Un nouvel outil de production des notices bibliographiques (ce qu'on appelle métadonnées).
* Refonte complète d'une application `ADCAT02` qui permet l'edition de la BDD catalogue
* Modélisation d'une architecture pour ces métadonnées
* Prise en compte des modifications du format

## Objectifs:

* permette la mise à jour, l'insertion en base des données des catalogueurs, simple ou multiple manuel et automatique
* suivre les modifications, corrections et l'historique d'une notice
* raccourcir les temps d'indexation et de publication dans l'interface catalogue
* controler la qualité et la granularité de la production des données
* synchronisations avec d'autres institutions productrices de métadonnées

----

Prise en compte :
* des nouveaux besoins en terme de catalogage,  [Feuille de route]
* de l'évolution du format interne de description des métadonnées, [Atelier InterMarcNG]
* des questions techniques soulevées par ces besoins, [Documentation technique] et entretiens des experts DL/GCA/MET/DSI
* des modes de production, de stockage et d'utilisation existant des données de catalogue
[Rapport d'étonnnement]
* des différents technologies utilisés [Schema CATSI]

----

Choix technique:
* Base de données Mongo (NOSQL orienté document):
  - base de données orientée sur une notice une notice = un document
  - applatissement du format Intermarc (4 niveaux)
  - gestion des ensembles et des listes d'items dans les sous-documents embarqués
  - pas de schéma pour des données diverses (+ 200 types de documents)
  - éviter les resolutions de tuples creux et les jointures complexes
  - gestion souple des références (relations entre document)
  - conserver la séparation entre les données et le controle du format
  - parallélisation des taches (aggregation, dénombrement,mise en relation)

* Environnement distribué en grappe de serveurs avec replication et redondance

* Format JSON (Conversion depuis le XML): plus compact, moins de place en mémoire et simplification à 1 niveau

* SOAP/ REST interface

----
## Flux de métadonnées

Toute l'activité de catalogage repose sur une base de données PCA dont le modèle est très complexe. Fonctionnement en silo avec pour centre nerveux la base de données.
Entrées ==> BDD Catalogue ==> Sorties
                  ^
                  |
        RIM <=> ADCAT O2


Flux d'entrées:
* Dépot légal:
  - flux automatique (ONIX)
  - flux manuel (DAE)
* Acquisition:
  - flux automatique (ONIX)
  - flux manuel (DAE)
* Coopération autres institutions:
  - Versement dans la base (DPI)
* Numérisation d'autres fonds:
  - Versement dans la base (DPI)

-----

Traitement:
- Conversion
- Insertion en base PostgresQL
- Correction/édition/fusion
- Indexation (SolR)
- Conversion XML -> Insertion dans FS

----
Flux de sortie:
* Portail consultation
  - BgF (XML > HTML)
  - presse locale ancienne(XML > HTML)
  - Nouveautés Editeurs (XML> HTML)
  - Interface catalogue (WebCCA) (XML> OAI> WebCCA)
* SI Spécifique/Tiers
  - Infos Dépot Legal (ONIX > XML)
  - Entrepot OAI (XML)
  - autres bibliothèques (XML)
  - data.bnf.fr (XML> RDF)
  - Produits (dump SQL> files)
  - ISNI  (XML[Atom]> BDD [OCLC])
* Manuel
- VIAF (WorldCat Manuel)

---
## Contexte
---

### Une longue tradition  de l'ingénierie documentaire:

Les données bibliographiques bénéficient d'une très longue tradition
de catalogage et de référencement qui justifient leur spécificité

  * format de catalogage interne (Intermarc)
  * protocole d'échange spécifique (SRU, Z39.50, AtomPub, ONIX, OAI)
  * format des données multiples (XML, RDF, HTML, fichiers)
  * contexte normatif international (normes ISO, AFNOR etc...)

Très différent des contextes de développement Big Data
---

### Le contexte spécifique des données

Les données bibliographiques en ce qu'elle décrivent des ressources documentaires, patrimoniales et culturelles ont des enjeux spécifiques propre à leur context de production et d'usage
  * Qualité, conservation, pérennité et réutiliabilité des données
  * Fonctionnement en silos centré autour d'un catalogue (Référence doc)
  * Spécificité des données: descriptives d'objet et d'entité

Dans un contexte d'évolution numérique
  * Evolution du métier du catalogueur (+ d'autonomie)
  * Mise en tension du métier d'informaticien documentaire (fonction support, évolution des technologies)

---

### Des métiers divers qui gravitent autour de ses données:

* Diversité des métiers qui gravitent autour de la production des données bibliographiques:
  - éditeurs et distributeurs,
  - conservateurs,
  - archivistes,
  - bibliotécaires,
  - catalogueurs
  - bibliographes
  - responsables qualité et normalisation
  - informaticien GED
---

### Des usages divers des données
* Diversité des profils qui utilisent ses données bibliographiques
  - académiques (étudiants/chercheurs)
  - professionnels & spécialistes (ex: juristes, métiers d'art)
  - documentalistes
  - éditeurs
  - grand publics
---
### Des enjeux spécifiques pour chacun des acteurs
L'écosystème justifie la diversité des enjeux autour de ses données:
  - obligation légale et promotion commerciale
  - mise en valeur d'un fond documentaire
  - conservation, pérennisation des ressources
  - accès, circulation et diffusion des ressources documentaires
  - ordre, granularité, fiabilité des descriptions des ressources
  - recensement exhaustif et selection de qualité
  - adaptation des données aux standards et aux normes: générique/spécifique
  - stockage, traitement, accès aux données enjeu transversal de support des enjeux

---
### Représentation d'une notice

Notice bibliographique est un document qui vise à décrire une ressource

3 types de notices:
* `Notices BIBliographique` description d'un ouvrage
* Notices AUTorité description d'une entité (personne, lieu, évènement, etc..)
* Notices ANAlytique ensemble de notices ordonnées autour d'une notice ou d'une entité

Une notice bibliographique est une métadonnée qui décrit une ressource
à la BnF le modèle de notice est ainsi constitué

* Notice BIB 1

* PEX
* UC


### Les différents modèles de données

* Modèle descriptif des données (format| grammaire| langue)
* Modèle logique de données (ordre| tri | selection| projection| agregation)
* Modèle conceptuel de données (sens | usage)















> BIG CAT
