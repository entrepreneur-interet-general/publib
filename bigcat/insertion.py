#!/usr/bin/venv35 python3
# -*- coding: utf-8 -*-

__doc__ = "Exploration des notices d'autorité INTERMARC"
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
import os
from datetime import datetime as dt
from multiprocessing import Pool
import json
import re

U_INT = re.compile(r'\d+', re.UNICODE)
U_NONINT = re.compile(r'[^(\d|\s)+]+', re.UNICODE)

def to_index(fname):
    exists = db.notices.findOne({"source_file": fname})
    return(exists is None)

def reindex(fname):
    '''evaluate which one has be to be reindex or index'''
    exists = db.notices.findOne({"source_file": fname})
    if exists is not None:
        print()
        return(exists["status"] is False)
    else:
        return(True)

def get_notices_f(notices_dir="/notices/xml/ixm/bnopalex/"):
    ''' retourner l'ensemble des notices présentes dans l'arborescence '''
    for d in sorted(os.listdir(notices_dir), reverse=False):
        for d1 in sorted(os.listdir(os.path.join(notices_dir,d)), reverse=False):
            d2 = os.path.join(notices_dir,d, d1)
            for d3 in sorted(os.listdir(d2), reverse=True):
                d3 = os.path.join(d2, d3)
                for f in sorted(os.listdir(d3),reverse=False):
                    yield os.path.join(d3, f)

def get_new_notices(db, notices_dir="/notices/xml/ixm/bnopalex/"):
    ''' retourner l'ensemble des notices présentes dans l'arborescence '''
    for d in sorted(os.listdir(notices_dir), reverse=False):
        for d1 in sorted(os.listdir(os.path.join(notices_dir,d)), reverse=False):
            d2 = os.path.join(notices_dir,d, d1)
            for d3 in sorted(os.listdir(d2), reverse=False):
                d3 = os.path.join(d2, d3)
                for f in sorted(os.listdir(d3),reverse=False):
                    fname = os.path.join(d3, f)
                    print(fname)
                    if db.notices.find_one({"source_file":fname}) is None:
                        print(fname, "index")
                        # yield os.path.join(d3, f)
                        yield db.notices.insert({"source_file": fname, "status":False, "msg": "to index"})



def convert_notice(fname):
    '''lire et applatir la notice xml'''
    record = {}



    #fname = fname.replace("./bnopalex", "./notices")
    with open(fname, "r", encoding="utf-8") as f:
        try:
            notice = f.read()
            r = bs(notice, "lxml")
            # print(r.encoding)
            r = r.record
            record["format"] = r.get("format")
            record["type"] = r.get("type")
            record["_id"] = int(r.get("numero"))
            record["source_file"] = fname

            positions = [get_pos(pos) for pos in r.find_all("pos")]
            subfields = [get_subfield(sub) for sub in r.find_all("subfield")]
            attributes = [get_attribute(att) for att in r.find_all("attr")]
            fields = positions+subfields+attributes
            fields_d = {n[0]:{"value":n[1], "sens":n[2]} for n in fields if n[0] is not None or n[1] is not None}
            try:
                record.update(fields_d)
                if r.find("pex") is not None:
                    pexs = {"pexs": [get_pex(pex) for pex in r.find_all("pex")]}
                    record.update(pexs)
                record["status"] = True
                try:
                    return db.notices.update({"_id": record["_id"]}, record, upsert=True)
                except Exception as e:
                    record["status"] = False
                    record["msg"] = str(e)
                    return db.notices.update({"_id": record["_id"]}, record, upsert=True)
            except Exception as e:
                record["status"] = False
                record["msg"] = str(e)
                return db.notices.update({"_id": record["_id"]}, record, upsert=True)
        except Exception as e:
            print(e)
            record = {}
            record["status"] = False
            record["msg"] = str(e)
            record["source_file"] = fname
            return db.notices.insert(record)

def cast(value,key, sens=None):
    '''casting value using tips(based on keys and meaning) and basic patterns'''
    nb = re.findall(U_INT, value)
    inv = re.findall(U_NONINT, value)
    if len(nb) > 0:
        #search by key: max int overflow error > 8Bytes
        # if key is not None:
        #     if "num" in key:
        #         if len(inv) == 0:
        #             try:
        #                 return int(value)
        #             except ValueError:
        #                 return value.strip()
        #                 # return long(value)
        #         else:
        #             return value
            if "date" in key:
                if len(nb) == 3:
                    if len(nb[-1]) == 4:
                        #31 jours 12 mois
                        try:
                            return dt.strptime("-".join(nb), "%m-%d-%Y")
                        except ValueError:
                            try:
                                return dt.strptime("-".join(nb), "%m-%d-%Y")
                            except:
                                return "-".join(nb)

                    elif len(nb[0]) == 4:
                        try:
                            return dt.strptime("-".join(nb), "%Y-%d-%m")
                        except ValueError:
                            try:
                                return dt.strptime("-".join(nb), "%Y-%d-%m")
                            except:
                                return "-".join(nb)

                    else:

                        try:
                            #default fr
                            return dt.strptime("-".join(nb), "%d-%m-%Y")
                        except:
                            return "-".join(nb)
                else:
                    if int(value) == 0:
                        return None
                    else:
                        return "-".join(nb)

    return value

def detect_date(v):
    '''transormer les dates de gestion en les formattant en type date
    not used
    '''
    if type(v) == dict:
        value = v["value"]
    else:
        value = v
    if "/" in v:
        if "__" in v:
            date = dt.strptime(v.replace("_", "00"), "%d/%m/%Y")
        else:
            date = dt.strptime(v.replace(" ", ""), "%d/%m/%Y")

    elif v == "00000000":
        date = None

    else:
        if v.startswith("20") or v.startswith("19"):
            date =  dt.strptime(v, "%Y%m%d")
        else:
            print("Error casting date:", v)
            date = v
    return date




def count_keys(db, col):
    '''statistiques: exporter le nombre d'occurences des codes et positions utilisées'''
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
def is_new(f):
    client = MongoClient("127.0.0.1", 27019, maxPoolSize=75, waitQueueMultiple=10, connect=False)
    #client = MongoClient()
    db = client.bigcat
    # simple function as an example
    if db.notices.find_one({"source_file":f}) is None:
        return f

def to_index():
    # client = MongoClient("127.0.0.1", 27019, maxPoolSize=75, waitQueueMultiple=10, connect=False)
    #client = MongoClient()
    # db = client.bigcat
    pool = Pool(processes=9)
    for f in pool.imap(is_new,get_notices_f,chunksize=10):
        print(f)
        convert_notice(f)
        pool.close()



if __name__ == "__main__":
    client = MongoClient("127.0.0.1", 27019, maxPoolSize=75, waitQueueMultiple=10, connect=False)
    #client = MongoClient()
    db = client.bigcat
    # client = MongoClient("127.0.0.1", 27017, maxPoolSize=75, waitQueueMultiple=10, connect=False)
    #client = MongoClient()
    # db = client.catcat
    # print("Notices", db.notices.count())
    # print("Erreurs", db.logs.count())
    # p = Pool(5)
    # listr = db.notices.distinct("fname")
    #db.refs.update([{"fname":n},{"$set":{"status":True}} for n in listr], multi=True)
    # bulk = db.initialize_ordered_bulk_op()
    # for fname in db.notices.distinct("source_file"):
    #     db.refs.update({'fname': fname}, {'$set': {'status': True}})
    # bulk.execute()
    # print(listr)
    #p.map(add_status, listr)
    # p.map =
    # to_index = [f for f in get_notices_f() if db.find_one({"source_file":f['name']}) is None]
    # to_index =
    #to_index = [n["fname"] for n in db.refs.find({"status":False}, {"_id":False, "fname":True})]
    # already_done = db.notices.distinct("source_file")
    # print(len(already_done))

    # for n in get_notices_f():
    #     doc = db.notices.find_one({"source_file":n})
    #     if doc is None:
    #         print("Index notice")
    #         print(convert_notice(n))

        # else:
        #     print("Done", n)


    # get_new_notices(db)
    # p.map(convert_notice, to_index)
    # from multiprocessing import Pool

    # if f not in list_in])

    # col = db.nn
    # print(count_keys(db, "nn"))
    # r_ids = db.notices.distinct("_id")
    # index_notices(db)
    # correct_logs(db)
    to_index()
