#!/usr/bin/venv35 python3
# -*- coding: utf-8 -*-

__doc__ = "Exploration des notices d'autorité INTERMARC A"

import os
#from lxml import etree, minidom
from io import StringIO, BytesIO
#import xmltodict, json
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
from datetime import datetime as dt
import random
import json




def get_notices(ref="./index_notices.txt"):
    with open(ref, "r") as f:
        notice_name = f.read()
    return notice_name.split('\n')
            # yield(line)
def read_notice(fname):
    record = {}

    fname = fname.replace("./bnopalex", "./notices")
    with open(fname, "r") as f:
        notice = f.read()
        r = bs(notice, "lxml").record
        record["format"] = r.get("format")
        record["type"] = r.get("type")
        record["_id"] = int(r.get("numero"))
        # record["rules"] = {n.get("tag"): {p.get("code"):p.text for p in n.find_all("pos")} for n in r.find_all("controlfield")}
        # record["code_n_ bnf"] = {n.get("code"): n.text for n in r.leader.find_all("pos")}
        if record["type"] ==  "Authority":
            record["notice"] = {n.get("tag"): {sf.get("code"): sf.text \
                                        for sf in n.find_all("subfield")} \
                                        for n in r.find_all("datafield")}

    print(json.dumps(record, indent=4, sort_keys=True))
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


if __name__ == "__main__":
    client = MongoClient()
    db = client.test_database
    # notices = random.sample(get_notices(), 1800)
    # for n in notices:
    for i,n in enumerate(get_notices()):
        record = read_notice(n)
        print(record)
        #record = cast_record(record)
        # print(record)
        # if i == 100:


        db.autorite.update({"_id":record["_id"]}, record, upsert=True)
