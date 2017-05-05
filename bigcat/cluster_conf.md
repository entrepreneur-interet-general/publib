Déclarer les hotes
```
$ sudo vim /etc/hosts
```

```
127.0.2.1   config0
127.0.2.2   config1
127.0.2.3   config2
127.0.2.4   query-router
127.0.2.5   shard1
127.0.2.6   shard2
127.0.2.7   shard3
127.0.2.7   shard4
127.0.2.8   shard5

```
Lancer les serveurs de conf:
```
$ mongod --configsvr --dbpath /data/config0 --logpath /data/log/config0 --bind_ip config0 --replSet replSet0 &
$ mongod --configsvr --dbpath /data/config1 --logpath /data/log/config1 --bind_ip config1 --replSet replSet0 &
$ mongod --configsvr --dbpath /data/config2 --logpath /data/log/config2 --bind_ip config2 --replSet replSet0 &
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
      { _id : 0, host : "config0:27019" },
      { _id : 1, host : "config1:27019" },
      { _id : 2, host : "config2:27019" }
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


Create the Shard Replica Sets
