#!/usr/bin/venv35 python3
# -*- coding: utf-8 -*-

__doc__ = "Exploration des notices d'autorité INTERMARC"

import os
#from lxml import etree, minidom
from io import StringIO, BytesIO
#import xmltodict, json
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
from datetime import datetime as dt
import random
import json
import sys
from collections import defaultdict


def scan_notices_dir(notices_dir="./notices"):
    for d in sorted(os.listdir(notices_dir), reverse=True):
        for d1 in sorted(os.listdir(os.path.join(notices_dir,d)), reverse=True):
            d2 = os.path.join(notices_dir,d, d1)
            for d3 in sorted(os.listdir(d2), reverse=False):
                d3 = os.path.join(d2, d3)
                for f in sorted(os.listdir(d3),reverse=True):
                    yield os.path.join(d3, f)

def get_notices(ref="./index_notices.txt"):
    with open(ref, "r") as f:
        notice_name = f.read()
    return notice_name.split('\n')
            # yield(line)

def read_notice(fname):
    '''flatten xml notice and index it converters next time :) '''
    record = {}
    fname = fname.replace("./bnopalex", "./notices")
    with open(fname, "r", encoding="utf-8") as f:
        notice = f.read()
        r = bs(notice, "lxml")
        # print(r.encoding)
        r = r.record

        record["format"] = r.get("format")
        record["type"] = r.get("type")
        record["_id"] = int(r.get("numero"))
        record.update({n.get("tag"): n.text.split('\n')[0] for n in r.find_all("controlfield")})
        for pos in r.find_all("pos"):
            #sous- zone à position
            if pos.parent.name == "subfield":
                tag = pos.parent.parent.get("tag")
                code = pos.parent.get("code")
                # sens = pos.get("sens")
                value = pos.text
                record[tag+"p"+code] =  value
            elif pos.parent.name == "controlfield" or pos.parent.name == "leader":
                tag = pos.parent.get("tag")
                if tag is None:
                    tag = "000"
                code = pos.get("code")
                value = pos.text
                record[tag+"p"+code] =  value
            else:
                print(">>>>>", pos.parent.name)
        for sub in r.find_all("subfield"):
            if sub.parent.name == "datafield":
                tag = sub.parent.get("tag")
                code = sub.get("code")
                value = sub.text
                record[tag+"$"+code] = value
            else:
                print(">>>>>", pos.parent.name)
        for at in r.find_all("attr"):
            if at.parent.name == "record":
                record[at.get("nom")] = at.text

        if r.find("pex") is not None:
            record["pexs"] = []
        for p in r.find_all("pex"):
            pex = {"no":p.get("no"), "nr":p.get('nr')}
            atts_l = [(at.get("rang"), at.get("nom"), at.text)
                        for at in p.find_all("attr")]
            atts_d = {n[1]:[] for n in atts_l}
            for n in atts_l:
                if n[0] is not None:
                    atts_d[n[1]].append(n[2])
                else:
                    atts_d[n[1]] = n[2]
            pex.update(atts_d)
            record["pexs"].append(pex)
    return record

def detect_date(v):
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
    #por l'instant on ne fait pas de mapping expicite du ref avec du texte
    for k, v in record.items():

        if "date" in k:
            if not "type" in k:
                record[k] = detect_date(v)
        if "nb" in k:
            record[k] = int(v)
    return record
def index_notices(db):
    '''indexation brutale de toutes les notices présentes dans l\'entrepot'''
    for i, fname in enumerate(scan_notices_dir()):
        fname = fname.replace("./bnopalex", "./notices")
        with open(fname, "r") as f:
            try:
                record = read_notice(fname)
                record["file"] = fname
                # if record["_id"] not in r_ids:
                try:
                    db.notices.insert(record)
                    print("Ok", i)
                except Exception as e:
                    print(fname, i)
                    db.logs.insert({"file":fname, "error": str(e)})
            except Exception as e:
                db.logs.insert({"file":fname, "error": str(e)})

def correct_logs(db):
    for n in db.logs.find():
        with open(n["file"], "r") as f:
            notice = f.read()
            r = bs(notice, "lxml")
            record = {}
            r = r.record
            record["format"] = r.get("format")
            record["type"] = r.get("type")
            record["_id"] = int(r.get("numero"))
            record.update({n.get("tag"): n.text.split('\n')[0] for n in r.find_all("controlfield")})
            for pos in r.find_all("pos"):
                if pos.parent.name == "subfield":
                    tag = pos.parent.parent.get("tag")
                    code = pos.parent.get("code")
                    # sens = pos.get("sens")
                    value = pos.text
                    record[tag+"p"+code] =  value
                elif pos.parent.name == "controlfield" or pos.parent.name == "leader":
                    tag = pos.parent.get("tag")
                    if tag is None:
                        tag = "000"
                    code = pos.get("code")
                    value = pos.text
                    record[tag+"p"+code] =  value
                else:
                    print(">>>>>", pos.parent.name)
            for sub in r.find_all("subfield"):
                if sub.parent.name == "datafield":
                    tag = sub.parent.get("tag")
                    code = sub.get("code")
                    value = sub.text
                    record[tag+"$"+code] = value
                else:
                    print(">>>>>", pos.parent.name)
            for at in r.find_all("attr"):
                if at.parent.name == "record":
                    record[at.get("nom")] = at.text

            if r.find("pex") is not None:
                record["pexs"] = []
            for p in r.find_all("pex"):
                pex = {"no":p.get("no"), "nr":p.get('nr')}
                atts_l = [(at.get("rang"), at.get("nom"), at.text)
                            for at in p.find_all("attr")]
                atts_d = {n[1]:[] for n in atts_l}
                for n in atts_l:
                    if n[0] is not None:
                        atts_d[n[1]].append(n[2])
                    else:
                        atts_d[n[1]] = n[2]
                pex.update(atts_d)
                record["pexs"].append(pex)
            try:
                db.notices.insert(record)
                db.logs.delete({"_id":n["_id"]})
            except Exception as e:
                print(e)

#raw mongodb operation
#get all distinct keys for the entire collections
def count_keys(db, col):
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
    db = client.test_database
    col = db.nn
    print(count_keys(db, "nn"))
    # r_ids = db.notices.distinct("_id")
    # index_notices(db)
    # correct_logs(db)
