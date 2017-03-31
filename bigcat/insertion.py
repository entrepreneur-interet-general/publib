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

def get_pos(pos):
    '''pour chaque tag "pos"
    renvoyer son tag parent ou grand parent
    le code, le sens
    '''

    if pos.parent.name == "subfield":
        tag = pos.parent.parent.get("tag")
        code = pos.parent.get("code")
        key = tag+"P"+code

        try:
            sens = pos.get("sens")
            value = cast(pos.text, key, sens)
        except KeyError:
            sens = None
            value = cast(pos.text, key)
        return (key, value, sens)
    elif pos.parent.name == "controlfield" or pos.parent.name == "leader":
        tag = pos.parent.get("tag")
        if tag is None:
            tag = "000"
        code = pos.get("code")
        key = tag+"P"+code
        value = pos.text
        try:
            sens = pos.get("sens")
            value = cast(value, key, sens)
        except KeyError:
            sens = None
            value = cast(value, key)
        return (key, value, sens)
    else:
        print("Error", post.parent.name,">", "P", pos )
        return (None, None, None)



def get_subfield(sub):
    '''
    Pour une sous-zone récupérer tous les champs data
    '''

    if sub.parent.name == "datafield":
        tag = sub.parent.get("tag")
        code = sub.get("code")
        key = tag+"$"+code
        value = sub.text
        try:
            sens = sub.get("sens")
            value = cast(value, key, sens)
        except KeyError:
            sens = None
            value = cast(value, key)
        return (key, value , sens)

    else:
        print("Error:", sub.parent.name,">$", sub)
        return (None, None, None)

def get_attribute(at):
    '''
    Pour une notice récupérer tous les attributs (données de gestion)
    '''
    if at.parent.name == "record":
        try:
            key = at.get("nom").lower()
            value = at.text
            try:
                sens = at.get("sens")
                value = cast(at.text, key, sens)
            except KeyError:
                sens = None
                value = cast(at.text, key)
            return (key, value, sens)
        except KeyError:
            return (None, None, None)
    else:
        return (None, None, None)

def get_pex(pex):
    '''chaque partie d'exemplaire correspond à un dictionnaire stockés dans la notice dans une liste non ordonnée
    elle dispose d'un ensemble de nom, sens explicite et attribut codé.
    Le sens a vocation a se substituer à l'attribut codé pour etre plus explicite
    Le nom est mis en minuscule
    Une pex est un dictionnaire
    '''
    nr, no = int(pex.get("nr")), int(pex.get("no"))
    pex_d = {"nr": nr, "no":no}
    for attr in pex.findAll("attr"):
        key = attr.get("nom").lower()
        value = attr.text
        try:
            sens = attr.get("sens")
            value = cast(value, key, sens)
        except KeyError:
            sens = None
            value = cast(value, key)
        pex_d[key] = {"sens":sens, "value": value}
    return pex_d

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
        record["source_file"] = fname
        try:
            positions = [get_pos(pos) for pos in r.find_all("pos")]

            subfields = [get_subfield(sub) for sub in r.find_all("subfield")]
            attributes = [get_attribute(att) for att in r.find_all("attr")]
            fields = positions+subfields+attributes
            fields_d = {n[0]:{"value":n[1], "sens":n[2]} for n in fields if n[0] is not None or n[1] is not None}
            record.update(fields_d)
            if r.find("pex") is not None:
                pexs = {"pexs": [get_pex(pex) for pex in r.find_all("pex")]}
                record.update(pexs)
            record["status"] = True
            return db.notices.insert(record)
        except Exception as e:
            record["status"] = False
            record["msg"] = str(e)
            return db.logs.insert(record)

def cast(value,key, sens=None):
    '''casting value using tips(based on keys and meaning) and basic patterns'''
    nb = re.findall(U_INT, value)
    inv = re.findall(U_NONINT, value)
    if len(nb) > 0:

        #serach by key
        if key is not None:
            if "num" in key:

                if len(inv) == 0:
                    try:
                        return int(value)
                    except ValueError:
                        return value.strip()
                        # return long(value)
                else:
                    return value
            if "date" in key:
                if len(nb) == 3:
                    if len(nb[-1]) == 4:
                        try:
                            #31 jours 12 mois
                            if nb[0] < 32 and nb[1]< 13:
                                return dt.strptime("-".join(nb), "%d-%m-%Y")
                            elif nb[1] < 32 and nb[0]< 13:
                                return dt.strptime("-".join(nb), "%m-%d-%Y")
                            else:
                                return dt.strptime("-".join(nb), "%d-%m-%Y")
                        except ValueError:
                            return dt.strptime("-".join(nb), "%m-%d-%Y")
                    elif len(nb[0]) == 4:
                        try:
                            #31 jours 12 mois
                            if nb[1] < 32 and nb[2]< 13:
                                return dt.strptime("-".join(nb), "%Y-%d-%m")
                            elif nb[2] < 32 and nb[1]< 13:
                                return dt.strptime("-".join(nb), "%Y-%m-%d")
                            else:
                                return dt.strptime("-".join(nb), "%Y-%m-%d")
                        except ValueError:

                            return dt.strptime("-".join(nb), "%Y-%d-%m")
                else:
                    if int(value) == 0:
                        return None
                    else:
                        print("Date ko", value)
                        return value
            else:
                try:
                    return int(value)
                except ValueError:
                    return(value)
    return value

def detect_date(v):
    '''transormer les dates de gestion en les formattant en type date'''
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



if __name__ == "__main__":
    client = MongoClient(host, port, maxPoolSize=150, waitQueueMultiple=10)
    db = client.catalogue

    p = Pool(9)
    p.map(convert_notice, [f for f in scan_notices_dir()])

    # col = db.nn
    # print(count_keys(db, "nn"))
    # r_ids = db.notices.distinct("_id")
    # index_notices(db)
    # correct_logs(db)
