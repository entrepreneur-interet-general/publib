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

## Insertion initiale en base (standalone)
4 echecs successifs d'insertion en base MONGODB en standalone:
(Compter entre 5 et 7 jours d'insertion des 19M de notices)

### Première tentative
Insertion non parallélisée des notices, pas de changement de type


### Deuxième tentative

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
Trop lourd donc à découper selon une logique soit volumétrique soit par paramêtre.
> Crash de la VM après agrégation: Memoire et CPU insuffisant
> Rechargement de la VM et supression du folder contenant les données


### Deuxième insertion en Base
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

> Crash de la VM après recherche: Memory Overflow
> Rechargement de la VM et supression du folder contenant les données

### Troisième insertion en base
Après mise à disposition d'un serveur plus puissant:
version parallélisée (multithread)
> erreur d'écriture sur le disque du srv de test: corruption de blocks et déconnexion du disque /notices

> Redémarrage du serveur et suppression du dossier contenant les donnés et le journal

### Quatrième insertion en base:
Après mise à disposition d'un serveur plus puissant:
version parallélisée (multithread) avec moins de coeur (5)
Deconnection de mongo incompatibilité avec  Virtual Box
MongoDB requires a filesystem that supports fsync() on directories. For example, HGFS and Virtual Box’s shared folders do not support this operation.

 https://docs.mongodb.com/manual/administration/production-notes/#kernel-and-file-systems


> erreur d'écriture sur le disque du srv de test: déconnexion du disque /notices

> Redémarrage du serveur et suppression du dossier contenant les donnés et le journal




## 3. Insertion en base (cluster)

La particularité du NoSQl base de données orientée documents est de permettre la **mise à l'échelle horizontale**
en répartissant une seule collection sur plusieurs *shards* en cluster
pour permettre de répartir l'espace de stockage et la capacité de calcul.


Sur le concept du sharding
en Mongo: https://docs.mongodb.com/v3.0/core/sharding-introduction/
en ElasticSearch https://www.elastic.co/guide/en/elasticsearch/reference/current/_basic_concepts.html


*Les SGBD avec de gros datasets  et de nombreuses applications (modifications multiples en concurrences) peuvent
mettre à l'épreuve les capacité d'un serveur unique*


### Installation d'un environnement distribué (cloud) de 3 serveurs pourMongoDB

Créer 3 VirtualHost sur le srv pour mettre 3 serveurs Mongo en réseau
- https://www.digitalocean.com/community/tutorials/how-to-set-up-apache-virtual-hosts-on-centos-7

Requiert 64G de RAM sur le serveur

http://www.tuxfixer.com/install-and-configure-elasticsearch-cluster-on-centos-7-nodes/


Mettre 3 serveurs APACHE sur une seule machine pour créer le cluster requis
https://crunchify.com/how-to-run-multiple-tomcat-instances-on-one-server/

### Installation d'un environnement distribué (cluster) pour ElasticSearch avec 3 nodes


## LITTLE CAT: echantillon au hasard de 10%
#### Reduire le périmêtre de notices pour POC
Réduire à 10% de l'ensemble des notices BIBLIOGRAPHIQUES

10% des notices BIB et
1O0% des notices AUT

* stats expresses
19M 226 013 notices:
- 5M566616 notices aut
- 13M659397 notices bib


1M4 notices BIB
+ 55616 notices AUT?
Selection au hasard parmis les notices  BIB
cf script `./parallel_index2.py`


* dans bac à sable:
- import des notices AUT (~5M6) 5M566 615 notices AUT
- notices BIB :  (~1M4) 1M396.601 notices BIB

:folder: Archives BIB: sample_bib10_0.json
:folder: Archives AUTH: authority.json


* dans env de travail:
- notices AUT (5 566 615 notices)
- notices BIB :  1549000 soit +10% mais non samplées

:folder: Archives BIB: sample_bib10_1.json
:folder: Archives AUTH: authority.json


#### Configuer mongo pour ES

1. Transformer la BDD mongo en replicaset
- Stopper le daemon
sudo systemclt stop mongo

- Editer la configuration de mongo
nano /etc/mongod.conf
Ajouter

replSet=rs0
dbpath=YOUR_PATH_TO_DATA/DB
logpath=YOUR_PATH_TO_LOG/MONGO.LOG

- Ouvrir mongo et réinitialiser la BDD
mongo DATABASE_NAME
config = { "_id" : "rs0", "members" : [ { "_id" : 0, "host" : "127.0.0.1:27017" } ] }
rs.initiate(config)
rs.slaveOk() // allows read operations to run on secondary members.

:ok: Fait sur env de travail

https://coderwall.com/p/sy1qcw/setting-up-elasticsearch-with-mongodb


2. Installer ElasticSearch
- Installer Java8
wget --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/8u73-b02/jdk-8u73-linux-x64.rpm"

sudo yum -y localinstall jdk-8u73-linux-x64.rpm
- Installer ElasticSearch
* Télécharger le packet ES 5
https://www.elastic.co/downloads/elasticsearch

sudo rpm -ivh elasticsearch-1.7.3.noarch.rpm

3. Configurer ElasticSearch

https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-elasticsearch-on-centos-7#step-4-%E2%80%94-securing-elastic

nano /etc/elasticsearch/elasticsearch/
### NOT starting on installation, please execute the following statements to configure elasticsearch service to start automatically using systemd
 sudo systemctl daemon-reload
 sudo systemctl enable elasticsearch.service
### You can start elasticsearch service by executing
 sudo systemctl start elasticsearch.service

>>> Se connecter en sudo


- télécharger elasticsearch-mapper-attachments pour Mongo-River
http://stackoverflow.com/questions/9140661/setting-up-mongodb-river-for-elasticsearch
- télécharger mongoriver
