Déclarer les hotes
```
$ sudo vim /etc/hosts
```

```
127.0.2.0   srv_conf0 ---\
127.0.2.1   srv_conf1 ---|=== rs_srv
127.0.2.2   srv_conf2 --/
127.0.2.3   router
127.0.2.4   shard1---\
127.0.2.5   shard2 ---|=== rs_coll
127.0.2.6   shard3 --/
```

Préparer l'environnement
* le stockage des données
```
mkdir /data/srv_conf0 /data/srv_conf1 /data/srv_conf2 /data/shard1 /data/shard2 /data/log/

```
* le stockage des configuration
```
mkdir /opt/mongodb/
```
Créer les fichier de configuration pour chaque serveur de configuration
en prenant cet exemple

vim /opt/mongodb/srv_conf0

```yml
sharding:
  clusterRole: configsvr
replication:
  replSetName: rs_srv # le nom du réplicat
net:
   bindIp: srv_conf0 # l'adresse du srvconf
   port: 27017
storage:
  dbPath: "/data/srv_conf0/" #les données
systemLog:
   destination: file
   path: "/data/log/srv_conf0.log" #les logs
   logAppend: true
```

```
cp /opt/BNF/mongodb/srv_conf0 /opt/BNF/mongodb/srv_conf1
sed -i -e 's/srv_conf0/srv_conf1/g' /opt/BNF/mongodb/srv_conf1
cp /opt/BNF/mongodb/srv_conf0 /opt/BNF/mongodb/srv_conf2
sed -i -e 's/srv_conf0/srv_conf2/g' /opt/BNF/mongodb/srv_conf2
```

Pour changer le nom du réplicat

```
sed -i -e 's/rs_srv/<new_name>/g' /opt/mongodb/srv_conf0 /opt/mongodb/srv_conf1 /opt/mongodb/srv_conf2
```

Lancer les 3 serveurs de conf:
```
mongod --config /opt/BNF/mongodb/srv_conf0 &
mongod --config /opt/BNF/mongodb/srv_conf1 &
mongod --config /opt/BNF/mongodb/srv_conf2 &
```

Relier les 3 srv au replicat
se connecter à l'un des srv_conf

```
$mongo srv_conf0:27017
```
Relier les membres au réplica
```
>
conf = {
  _id: "rs_srv",
  configsvr: true,
  members: [
    { _id : 0, host : "srv_conf0:27017" },
    { _id : 1, host : "srv_conf1:27017" },
    { _id : 2, host : "srv_conf2:27017" }
  ]
}
> rs.initiate(conf)
> rs.conf()
> rs.status()
> exit
```
Créer les fichiers de configuration pour chaque shards
en prenant cet exemple

vim /opt/mongodb/shard1

```yml
sharding:
  clusterRole: shardsvr
replication:
  replSetName: rs_shard # le nom du réplicat
net:
   bindIp: shard0 # l'adresse du srvconf
   port: 27017
storage:
  dbPath: "/data/shard1/" #les données
systemLog:
   destination: file
   path: "/data/log/shard1.log" #les logs
   logAppend: true
```
cp /opt/BNF/mongodb/shard1 /opt/BNF/mongodb/shard2
cp /opt/BNF/mongodb/shard1 /opt/BNF/mongodb/shard3
cp /opt/BNF/mongodb/shard1 /opt/BNF/mongodb/shard4
sed -i -e 's/1/2/g' /opt/BNF/mongodb/shard2
sed -i -e 's/1/3/g' /opt/BNF/mongodb/shard3
sed -i -e 's/1/4/g' /opt/BNF/mongodb/shard4

Lancer un 
```
mongod --config /opt/BNF/mongodb/srv_conf0 &
mongod --config /opt/BNF/mongodb/srv_conf1 &
mongod --config /opt/BNF/mongodb/srv_conf2 &
```


Lancer les serveurs de conf:
```
$ mongod --configsvr --dbpath /data/srv_conf0 --logpath /data/log/srv_conf0.log --bind_ip config0 --replSet rs_srv &
$ mongod --configsvr --dbpath /data/srv_conf1 --logpath /data/log/srv_conf1.log --bind_ip config1 --replSet rs_srv &
$ mongod --configsvr --dbpath /data/srv_conf2 --logpath /data/log/srv_conf2.log --bind_ip config2 --replSet rs_srv &
```
Le même réplicat?
Vérifier que les serveurs écoutent sur le bon port
```
$ netstat -tl

Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 config2:27019           0.0.0.0:*               LISTEN     
tcp        0      0 config0:27019           0.0.0.0:*               LISTEN     
tcp        0      0 config1:27019           0.0.0.0:*               LISTEN
$
```

Stopper les servieurs de conf
```
mongod --dbpath /data/config0  --shutdown
mongod --dbpath /data/config1  --shutdown
mongod --dbpath /data/config2  --shutdown
```
Se connecter à un serveur de conf
```
$ mongo config0:27019
>
```
Configurer le replicat
```
rs.initiate(
  {
    _id: "replSet0",
    configsvr: true,
    members: [
      { _id : 0, host : "config0:27017" },
      { _id : 1, host : "config1:27017" },
      { _id : 2, host : "config2:27017" }
    ]
  }
)

{
	"ok" : 0,
	"errmsg" : "'config2:27019' has data already, cannot initiate set.",
	"code" : 110,
	"codeName" : "CannotInitializeNodeWithData"
}

# config avec un seul noeud et un seul replicat!!
config = {
  _id: "replSet0",
  configsvr: true,
  members: [
    { _id : 0, host : "config0:27019" },
  ]
}
rs.initiate(config)

rs.add(config1:27019)
rs.add(config2:27019)

rs.status()
```

mongos --configdb replSet0/config0:27019,config1:27019,config2:27019


## Create the Shard Replica Sets
Declare the cluster as a Service
https://www.linode.com/docs/databases/mongodb/build-database-clusters-with-mongodb
Add Shards to the Cluster


mongo query-router:27017
sh.addShard(replSet2/shard1:27017)
sh.addShard(shard2:27017)
sh.addShard(shard3:27017)
sh.addShard(shard4:27017)
sh.addShard(shard5:27017)
