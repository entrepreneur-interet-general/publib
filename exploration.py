#!/usr/bin/venv35 python3

import os
#from lxml import etree, minidom
from io import StringIO, BytesIO
import xmltodict, json
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
from datetime import datetime as dt
import random




def get_notices(ref="./index_notices.txt"):
    with open(ref, "r") as f:
        notice_name = f.read()
    return notice_name.split('\n')
            # yield(line)
def read_notice(fname):
    record = {}
    # print(fname)
    fname = fname.replace("./bnopalex", "./notices")
    with open(fname, "r") as f:
        notice = f.read()
        r = bs(notice, "lxml").record
        record["format"] = r.get("format")
        record["type"] = r.get("type")
        record["_id"] = int(r.get("numero"))
        #record management info
        #record["leader"]= {p.get("code"): p.text for p in soup.record.leader.find_all("pos")}
        for df in r.find_all("datafield"):
            record[df.get("tag").lower()] = {p.get("code"): p.text for p in df.find_all("subfield")}

        for att in r.find_all("attr"):
            # print(att)
            record[att.get("nom").lower()] = att.text
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
            print(v)
            return v

def cast_record(record):
    #por l'instant on ne fait pas de mapping expicite du ref avec du texte
    for k, v in record.items():

        if "date" in k:
            if not "type" in k:
                record[k] = detect_date(v)
        if "nb"  in k:
            record[k] = int(v)
    return record
def add_in_db():
    '''methode stupide pour insérer en base'''
    pass# trop stupide pour etre utile

if __name__ == "__main__":
    client = MongoClient()
    db = client.test_database
    notices = random.sample(get_notices(), 1800)
    for n in notices:
        record = read_notice(n)
        record = cast_record(record)
        db.notices.upsert(record)
