# Exemples de requetes
# Compter les notices d'autorité / bibliographique
db.notices.count({"type":"Bibliographic"})
db.notices.count({"type":"Authority"})
# Aggreger le nombre d'exemplaires pour une notice
db.notices.aggregate(
  [{ $match:
    {'pexs': {$exists: true}, 'nb_pex':{$exists:false}}
    },
    {
     $addFields: {
       nb_pex: { $size: "$pexs" } ,

     },
     {
       $out: "notices"
     }

   ]

  )
# Compter le nombre d'exemplaires total dans le catalogue
```
  db.notices.aggregate({
    $group: {
        _id: '',
        total_pex: { $sum: '$nb_pex' }
    }
 }, {
    $project: {
        _id: 0,
        total_pex: '$total_pex'
    }
})
```

# Recherche d'exemplaires
Rechercher tous les exemplaires qui contiennent mottaïnaï dans le titre

```
> db.notices.find({"245$a.value": {$regex:"mot(t)?a(i|ï)na(i|ï)"}})
```


Recherche tous les exemplaires qui sont en magasin et dont l'auteur a le prénom Ernest
```
> db.notices.find({"100$m.value": "Ernest", "pexs":{$elemMatch:{"conditioncommunication.value":"M"}}})
```
