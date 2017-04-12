#!/usr/bin/venv35 python3
# coding: utf-8

__doc__ = "Statistiques CATALOGUE"
from db import coll, db
from bson.son import SON
from bson.code import Code

def add_nb_pexs(coll_name = notices):
    '''agregation: insert nb_pexs with len(pexs)'''
    pipeline = [
    { $match:
      {'pexs': {$exists: true}, 'nb_pex':{$exists:false}}
     },
     {
       $addFields: {
         nb_pex: { $size: "$pexs" } ,

      },
      {
         $out: str(coll_name)
      }
     ]
    results = coll.aggregate(pipeline)
    print(results.find({"nb_pex":{"$gte":2000}})

def count_pexs():

def count_keys():
    '''exporter le nombre d'occurences des codes et positions utilisées'''
    # mr = db.runCommand({
    #   "mapreduce" : "my_collection",
    #   "map" : function() {
    #     for (var key in this) { emit(key, null); }
    #   },
    #   "reduce" : function(key, stuff) { return null; },
    #   "out": "my_collection" + "_keys"
    # })
    # db[mr.result].distinct("_id")
    from bson.code import Code

    mapper = Code("""
        function() {
                      for (var key in this) { emit(key, null); }
                   }
    """)
    reducer = Code("""
        function(key, stuff) { return null; }
    """)

    distinct_fields = db[str(col)].map_reduce(mapper, reducer
        , out = {'inline' : 1}
        , full_response = True)

    for n in distinct_fields["results"]:
        # print(n)
        print(n["_id"], db[col].find({n["_id"]:{"$exists":True}}).count())
        ## do something with distinctThingFields['results']
