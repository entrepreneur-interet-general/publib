# Big CAT

Proposer un modèle de données orienté documents (notices)
Test initial avec Mongo DB pour le stockage et ElasticSearch pour l'indexation et la recherche

## Objectifs

**PISTE TAM**
* Exposer simplement les données du catalogue via une API qui permet:
  - la consultation
  - l'insertion
  - la modification/correction
  - la suppression

des notices par unité ou par paquets qui seront indexées automatiquement par le numéro de notices.


**PISTE RIM NG**
* Proposer un [tableau de bord](dashboard.md) pour le suivi des zones, sous zones utilisés dans le catalogue et permettre l'administration du format, la modification  et l'alignement
à d'autres référentiels et le suivi des règles d'interdépendances des zones au niveau de la  notice


**PISTE EXO_REF /FNE**
* Permettre le suivi, et le controle qualité sur les insertions et modifications au catalogue grace à l'historique et au logs par versions

* Permettre l'indexation et la modification en temps réel ainsi que la collaboration avec d'autres institutions

## Etape 0:  Mise en place de l'environnement

Les prérequis pour ce genre d'opération consiste principalement dans la mise en place d'un environnement de travail adapté et capable de traiter les 19M de notices de la BNF dans un temps relativement court.

Etape négligée dans les premiers temps dont toutes les étapes ont été décrites
dans le document [Environnement](environnement.md)
On y trouve notamment les instructions sur l'
- Installation et configuration de MongoDB
- Installation et configuration de ElasticSearch
en standalone et/ou en cluster distribué

## Etape 1: Modélisation des données autour de la notice

### Les données à disposition

#### Parcours des données dans le SI
* Les données de catalogue arrivent depuis de nombreuses applications SI et sont insérées dans la Base de données PCN (Postgresql).
* Le format initial des données consiste dans du texte formattée selon le format/ langage à balise interne à la BNF InterMarc.
* Elle sont ensuite transformées en xml, additionnées de données de gestions et versées dans un puits /notices reparties dans le filesystem en fonction de leur numéro de notices.
* Pour être exposées dans le catalogue,exportées en produit bibliographique ou convertit en d'autres formats pour export


#### Types de données

Les données du catalogue correspondent aux notices  modifiées par les catalogueurs dans l'application AD CAT 02.

Il y en a deux types:
- les notices d'AUTORITE
- les notices Bibliographiques

##### Notices d'AUTORITE
10000000 =< numéro de notice >30000000

représentent une entité: personne, lieu, réalisation, oeuvre intellectuelle etc...

voir un [exemple de notices d'autorité](./exampleA.xml)

##### Notices BIBLIOGRAPHIQUES

numero de notice >= 30000000
représentent un ouvrage
voir un [exemple de notices bibliographique](./exampleB.xml)

A ces types de notices s'ajoutent les notices Analytiques (Notice Bibliographiques d'Oeuvre en tant qu'ensemble mais rangées comme des notices biblographiques)


Une notice regroupe l'ensemble des ouvrages physiques ou numériques concernant une oeuvre, elles sont désignées:
- par des PEX (Partie d'exemplaire) qui correspondent aux élements intellectuel constituant de l'oeuvre (Symphonie Pastorale, A la recherche du temps perdu)
- et par des U.C (Unité de conservation) qui correspondent à l'élement physique d'un ouvrage (Tome1, fichier, boite)

#### Format des données

Le format de catalogage est un format texte inspiré du MARC: InterMarc est le format de chaque notice produite par la BnF.

[A propos du format InterMarc](http://www.bnf.fr/fr/professionnels/f_intermarc/s.format_intermarc_biblio.html)

Il consiste dans un langage à balise.
Ces balises consistent dans des zones, sous zones, des positions,des sous zones à position.

Les valeurs contenues dans ses balises peuvent être controlées ou libres en fonction de ce que le format prévoit et qui est communiqué aux catalogueurs via le guide KITCAT.

La gestion, la validation et l'évolution de ses champs ou zones sont controlés par le RIM (Référentiel InterMarc) qui définit les règles de gestion et interdépendance du format appuyé par une base de données et une application spécifique (AD CAT 90)
Ce langage à balise est un format hiérarchique controlé, parfaitement compatible avec le XML.

Chaque notice est donc transformée en XML: InterXmarc est le format pivot pour la consultation, la diffusion à des tiers et la conversion.

Le format Intermarc est un format complexe qui rend compte de la diversité des usages, des départements et des objets catalogués.

Une notice bibliographique est donc caractérisées au minimum par une dizaine de champs descriptifs ainsi qu'au moins une PEX et une UC.


#### Modèle Logique de données

Le modèle logique de données existant repose sur un schema SQL avec un ensemble de tables dont une colonne qui stocke l'ensemble de la notice et un ensemble de tables liées qui stockent les PEX et les UC. Les valeurs contenues dans les tables sont controlées par une autre base de données, les insertions spécifique et les
corrections se font par DPI de même que l'export et la conversion dans d'autres format.

#### Modéle Orienté document
Un (SGBD)Système de Gestion de Base de données orientée documents s'adapte assez bien au problématiques de gestion documentaire et bibliographique. Le format de stockage est en JSON qui représente la donnée sont forme de dictionnaire de clé valeur et
avec éventuellement des niveaux.

Les premiers développement on consiste dans le changement de paradigme de stockage des données.

On stocke dans une seule table (*collection* en NOSQL) et dans une seule base.
Chaque document (ici une notice) est caractérisée par un **ensemble de clé/valeurs adapté à son cas particulier** avec des clés obligatoires (numéro de notice et type de notices).


    Cela évite de stocker toutes les clés possibles
    pour une notice dans une table et leur assigner la valeur nulle


Au élement descriptif de la notice s'ajoute dans notre cas, une clé "pex" qui stocke sous forme de liste des diférents ouvrages réunit dans cette notice

LA premiere étape de développement consistait dans un script qui formatter chaque notice XML en **JSON** puis insère dans uen seule base de données et dans une seule table
IL s'agit
- *applatir* la structure XML  de la notice  du format [Intermarc](http://www.bnf.fr/fr/professionnels/f_intermarc/s.format_intermarc_biblio.html)
* en permettant pour **certaines zones** les valeurs multiples en **liste** et parfois en liste de dictionnaires:
  * les pex
  * les données de gestion

* en transformant des valeurs textuelles en types de données informatiques (cast)
  * les dates seront au format date (datetime.date)
  * les nombres (integer, float, long)
  * les textes (string) avec controle automatique de taille autorisé
* en réutilisant le travail de traduction déjà réalisé dans le XML
qui donne un "sens" explicite à certaun code

le champ des notices est donc converti et transposé en json et stocké ainsi:

  ` { <zone>$<sous_zone>P<position>: {"value":<valeur>, "sens:"} `

  y sont ajouté au meme niveau les données de gestion
  ainsi que les parties d'exemplaires sous forme de liste de dictionnaires

Voir le script python `parallel_index2.py`


## Etape 2: Interface de consultation/recherche/modification
