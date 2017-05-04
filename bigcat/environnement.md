# Environnement

1. Environnement de travail  et tests
2. Architecture: Infrasture unique vs environnement distribué
3. Infrastructure imaginée:
    - Base de données Mongo + extension de la recherche et des interactions avec Elastic Search
    - Mise en place en place d'un tableau de bord Kibana?
    - Interface minimale Flask/bottle?
4. Procédure d'installation et configuration:
  * Base de données Mongo
    * Installation/ Configuration de Mongo DB Standalone
    * Mongo DB Sharding et Replica

  * Moteur de recherche : Elastic Search
    * Installation/configuration de Elastic Search Standalone
    * Installation/configuration de Elastic Search Cluster

## 1. Environnement de travail et tests

* Installation en local sur une machine virtuelle de test
de MongoDB

      OS distrib: CentOS
      System Requirements:
        64-bit Architecture
        8 GB RAM
        2 Cores
        30 GB disk space

A noter: Les performances de MongoDB sont meilleures si l'intégralité des données correspondent à la taille de la RAM pour l'insertion, la recherche, et la modification.
De plus, l'acces à la mémoire est ici non uniforme (Non-Uniform Access Memory (NUMA)) ce qui implique une instanciation de mongo particulière et fragilisie la persistence des données

Premiers tests d'insertion de notices dans un seule instance Mongo Daemon:
5 échecs successifs d'insertion en base MONGODB en standalone:
(Compter entre 5 et 9 jours d'insertion des 19M de notices)

**Test1**
Insertion non parallélisée des notices, pas de changement de type. SImple transformation json des notices xml.

Temps d'insertion un par un très long: compter 9 jours pour insérer les 19M2 de notices.
La base de données finales pèse 32 Go (sans compter la place pour les journaux/logs).
Correction multiples sur la base

Le daemon de mongo s'arrete après quelques recherches et agrégations.
> Perte de données au moment de la recherche, CPU limit
> Rechargement de la VM et tentative d'export des données
notices AUT Ok


**Test2**
```
$ mongo catalogue
> db.notices.count()
> 18 360 944
> db.logs.count()
> 29
```
Il en manquait presque 1 M

* Depuis la base préexistantes: séparer les notices AUT(6M) des notices BIB( 13M2)
dans 2 tables différents pour correction et réinsertion des notices BIB manquantes
> Crash et perte des données au moment de l'agrégation

dumps trop lourd pour etre sauvegardés (Taille des index)
export des données en json
Le dump de la base remplissait tout l'espace disque
 ```
 mongoexport -d catalogue -c aut -o notices_aut.json
 ```
> Crash de la VM après export, Mémory Overflow
> Rechargement de la VM et supression du folder contenant les données

**mise à l'échelle verticale**
* Mise à disposition d'un serveur interne

  CPU : 16 x Intel(R) Xeon(R) CPU           E5620  @ 2.40GHz
  RAM : 64 Go
  DD : ~3 To
  OS : CentOS 7.3


insertion en 5 j (Yeah!)
- première tentative réussies de recherche
- opération map/reduce, et d'agregations (nb_pexs)

MongoD crash et perte de données
Premières stats sur les pex:
Au global
- 22M226577 pexs
- 13M043295 notices avec au moins une pex => bizarrerie 13 M de notices? manque 6 M de notices

 Stats (sur les 13 M)
|Nb pex | nb notices|
|-------|-----------|
|> 10   | 63 591    |
|> 100  | 940       |
|> 10   | 6         |
|> 2000 | 1         |
|> 10000| 0         |

La notices avec 2000M de Pex correspond à Indéfini
perte de données : 6 M notices AUT?


**Test3**

Après mise à disposition d'un serveur plus puissant:
version parallélisée (multithread) 12 thread
> erreur d'écriture sur le disque du srv de test: corruption de blocks et déconnexion du disque /notices.

> Redémarrage du serveur et suppression du dossier contenant les donnés et le journal
par un tiers

**Test4**
Après mise à disposition d'un serveur plus puissant:
version parallélisée (multithread) avec moins de thread (5)

> erreur d'écriture sur le disque du srv de test: corruption de blocks et déconnexion du disque /notices.

Deconnection de mongo incompatibilité avec  Virtual Box
MongoDB requires a filesystem that supports fsync() on directories. For example, HGFS and Virtual Box’s shared folders do not support this operation.

 https://docs.mongodb.com/manual/administration/production-notes/#kernel-and-file-systems

> erreur d'écriture sur le disque du srv de test: déconnexion du disque /notices ou latence trop longue + plus d'espace disque (oubli de conf le stockage dans la bonne partition)
> Suppression du dossier contenant les donnés et le journal

**Test5**: **reduire le nombre de notices**
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
cf script `./insertion.py`


* dans serveur puissant:
- import des notices AUT (~5M6) 5M566 615 notices AUT
- notices BIB :  (~1M4) 1M396.601 notices BIB

:folder: Archives BIB: sample_bib10_0.json
:folder: Archives AUTH: authority.json

* dans env de travail:
- notices AUT (5 566 615 notices)
- notices BIB :  1549000 soit +10% mais non samplées

:folder: Archives BIB: sample_bib10_1.json
:folder: Archives AUTH: authority.json

10% des notices BIB + 100% des notices AUT


## 2. Architecture BIG DATA: Infrasture unique vs environnement distribué

*Les SGBD avec de gros datasets  et de nombreuses applications (modifications multiples en concurrences) peuvent
mettre à l'épreuve les capacité d'un serveur unique*

Ici rentre les considération de mise à l'échelle pour éviter la mise à l'épreuve des capacités machine

Considération de mise à l'échelle de Mongo : https://www.mongodb.com/blog/post/capacity-planning-and-hardware-provisioning-mongodb-ten-minutes

Considération de mise à l'échelle de ES:
https://www.elastic.co/guide/en/elasticsearch/guide/current/hardware.html


A ces difficultées on propose deux solutions:
* mise à l'échelle verticale
* mise à l'échelle horizontale

**Mise à l'échelle verticale**: augmenter la taille de stockage, le CPU et la RAM
Ok: limite le temps d'insertion mais difficulté lié au type de stockage des données sources serveur distant




La particularité du NoSQl base de données orientée documents est de permettre la **mise à l'échelle horizontale**
en répartissant une seule collection sur plusieurs *shards* (morceaux partagés) en cluster pour permettre de répartir l'espace de stockage et la capacité de calcul sur plusieurs noeuds.




#### Sharding en Mongo: création d'un cluster de calcul
A propos:
https://docs.mongodb.com/v3.0/core/sharding-introduction/

Requiert:
- 64G de RAM sur le serveur
- création de 3 serveurs Mongo en réseau sur une même machine
https://www.digitalocean.com/community/tutorials/how-to-set-up-apache-virtual-hosts-on-centos-7
https://crunchify.com/how-to-run-multiple-tomcat-instances-on-one-server/
:idea: Création de trois Dockers?

### Sharding avec Elastic Search: création d'un Cluster
A propos:
https://www.elastic.co/guide/en/elasticsearch/reference/current/_basic_concepts.html

Requiert 1 noeud master et 2 noeuds esclave
http://www.tuxfixer.com/install-and-configure-elasticsearch-cluster-on-centos-7-nodes/

# 3. Infrastructure imaginée
Exposer les données catalogue via une API

- Base de données Mongo + extension de la recherche et des interactions avec Elastic Search
:question:
    peut on se passer de Mongo? d'ES?
- Mise en place en place d'un tableau de bord Kibana?
- Interface de consultation/modification en flask /bottle

# 4. Procédure d'installation et configuration:

## Mongo
Installer mongo sur CentOS

### Mongo standalone
Une seule instance mongod (daemon)
avec l'intégralité de la base

- Editer la configuration de mongo
nano /etc/mongod.conf
  * path
    dbpath=YOUR_PATH_TO_DATA/DB
    logpath=YOUR_PATH_TO_LOG/MONGO.LOG

journal=

- Permettre la connexion multiple sur une machine NUMA


### Mongo Sharding
Plusieurs instance de mongos (serveur)


* **Créer des replicas**
* Transformer la BDD mongo en replicaset
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
```
config = { "_id" : "rs0", "members" : [ { "_id" : 0, "host" : "127.0.0.1:27017" } ] }
rs.initiate(config)
rs.slaveOk() // allows read operations to run on secondary members.
```

## Elastic Search
### Elastic Search standalone

Depuis Mongo

https://coderwall.com/p/sy1qcw/setting-up-elasticsearch-with-mongodb

### Elastic Search cluster

2. Installer ElasticSearch
- Installer Java8
```bash
$ sudo yum install java-1.8.0-openjdk.x86_64
```

- Installer ElasticSearch
Last version : elastic-search 5.3.2
```bash
sudo vim /etc/yum.repos.d/elasticsearch.repo
```
```
[elasticsearch-5.x]
name=Elasticsearch repository for 5.x packages
baseurl=https://artifacts.elastic.co/packages/5.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
```

sudo yum install elasticsearch

3. Configurer ElasticSearch

https://www.tecmint.com/install-elasticsearch-logstash-and-kibana-elk-stack-on-centos-rhel-7/
nano /etc/elasticsearch/elasticsearch.yml

cluster.name : big-foot
node.name : node-1
path.data = /data/es/
path.logs = /data/logs/es/
network.host: #specific adress
network.port: #specific port

**Configurer le srv**

:warning: Make sure that the heap size is set to about half the memory available
on the system and that the owner of the process is allowed to use this
limit.

Elasticsearch performs poorly when the system is swapping the memory.

HEAP SIZING https://www.elastic.co/guide/en/elasticsearch/guide/current/heap-sizing.html

https://www.elastic.co/guide/en/elasticsearch/reference/2.3/setup-configuration.html

```
sudo systemctl daemon-reload
sudo systemctl enable elasticsearch.service
sudo systemctl start elasticsearch.service
```

Démarrer elastic search au moment du boot
```
sudo chkconfig --add elasticsearch
```

Shortcuts de systemd/systemctl
```
sudo service elasticsearch start
sudo service elasticsearch stop
sudo service elasticsearch reload
sudo service elasticsearch status
```

Impossible de se connecter via Curl SQUID reponse:404
mais via requests si !
>>> import requests
>>> r = requests.get("http://127.0.0.1:9200")
>>> print(r)
<Response [200]>
>>> print(r.text)
{
  "name" : "noJ1kO9",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "8S_mtigZS7-KepEZQfr8JQ",
  "version" : {
    "number" : "5.3.2",
    "build_hash" : "3068195",
    "build_date" : "2017-04-24T16:15:59.481Z",
    "build_snapshot" : false,
    "lucene_version" : "6.4.2"
  },
  "tagline" : "You Know, for Search"
}

```
netstat -tunlp
```
Test insertion dans Elastic
Test -XPUT
Install logstach
