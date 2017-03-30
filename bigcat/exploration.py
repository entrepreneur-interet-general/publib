#!/usr/bin/venv35 python3
# -*- coding: utf-8 -*-

__doc__ = "Exploration des notices d'autorité INTERMARC"
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
import os
from datetime import datetime as dt
from multiprocessing import Pool
import json

# import re
# def cast_str_2_int(value):
#     regex.find("\d+")
def scan_notices_dir(notices_dir="/notices/xml/ixm/bnopalex/"):
    ''' retourner l'ensemble des notices présentes dans l'arborescence '''
    for d in sorted(os.listdir(notices_dir), reverse=True):
        for d1 in sorted(os.listdir(os.path.join(notices_dir,d)), reverse=True):
            d2 = os.path.join(notices_dir,d, d1)
            for d3 in sorted(os.listdir(d2), reverse=False):
                d3 = os.path.join(d2, d3)
                for f in sorted(os.listdir(d3),reverse=True):
                    yield os.path.join(d3, f)


def convert_notice(fname):
    '''lire et applatir la notice xml'''
    record = {}
    #fname = fname.replace("./bnopalex", "./notices")
    with open(fname, "r", encoding="utf-8") as f:
        notice = f.read()
        r = bs(notice, "lxml")
        # print(r.encoding)
        r = r.record
        record["format"] = r.get("format")
        record["type"] = r.get("type")
        record["_id"] = int(r.get("numero"))
        try:
        #record.update({n.get("tag"): n.text.split('\n')[0] for n in r.find_all("controlfield")})
            for pos in r.find_all("pos"):
                #sous- zone à position
                if pos.parent.name == "subfield":
                    tag = pos.parent.parent.get("tag")
                    code = pos.parent.get("code")
                    # sens = pos.get("sens")
                    value = pos.text
                    try:
                        sens = pos.get("sens")
                    except KeyError:
                        sens = None
                    record[tag+"p"+code] =  {"value": value, "sens": sens}

                elif pos.parent.name == "controlfield" or pos.parent.name == "leader":
                    tag = pos.parent.get("tag")
                    if tag is None:
                        tag = "000"
                    code = pos.get("code")
                    value = pos.text
                    try:
                        sens = pos.get("sens")
                    except KeyError:
                        sens = None
                    record[tag+"P"+code] =  {"value": value, "sens": sens}

                else:
                    print(">>>>>", pos.parent.name)
            for sub in r.find_all("subfield"):
                if sub.parent.name == "datafield":
                    tag = sub.parent.get("tag")
                    code = sub.get("code")
                    value = sub.text
                    try:
                        sens = pos.get("sens")
                    except KeyError:
                        sens = None
                    record[tag+"$"+code] =  {"value": value, "sens": sens}
                else:
                    print(">>>>>", pos.parent.name)
            for at in r.find_all("attr"):
                if at.parent.name == "record":
                    record[at.get("nom")] = at.text

            if r.find("pex") is not None:
                records["pexs"] = [index_pex(pex) for p in r.find_all("pex")]
            print(db.notices.insert(cast_record(record)))
        except Exception as e:
            print(fname, e)
            pass

def detect_date(v):
    '''transormer les dates de gestion en les formattant en type date'''
    if "/" in v:
        if "__" in v:
            return dt.strptime(v.replace("_", "00"), "%d/%m/%Y")
        return dt.strptime(v.replace(" ", ""), "%d/%m/%Y")

    elif v == "00000000":
        return None
    else:
        if v.startswith("20") or v.startswith("19"):
            return dt.strptime(v, "%Y%m%d")
        else:
            print("Error", v)
            return v

def cast_record(record):
    '''etape 0: cast des valeurs numériques et des dates a partir de leur nom'''
    for k, v in record.items():

        if "date" in k:
            if not "type" in k:
                record[k] = detect_date(v)
        if "nb" in k:
            record[k] = int(v)
    return record

def index_pex(pex):
    '''chaque partie d'exemplaire correspond à un dictionnaire stockés dans la notice dans une liste non ordonnée
    elle dispose d'un ensemble de nom, sens explicite et attribut codé.
    Le sens a vocation a se substituer à l'attribut codé pour etre plus explicite
    '''
    nr, no = int(pex.get("nr")), int(pex.get("no"))
    pex_d = {"nr": nr, "no":no}
    for attr in pex.findAll("attr"):
        try:
            key, val = attr.get(nom), attr.get("sens")
        except KeyError:
            key, val = attr.get(nom), attr.text
        pex_d[key] = val
    return pex_d


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



if __name__ == "__main__":
    client = MongoClient()
    # db = client.catalogue
    db = client.catalogue
    p = Pool(9)
    p.map(convert_notice, [f for f in scan_notices_dir()])
    # col = db.nn
    # print(count_keys(db, "nn"))
    # r_ids = db.notices.distinct("_id")
    # index_notices(db)
    # correct_logs(db)
