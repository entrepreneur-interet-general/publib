#!/usr/bin/venv35 python3
# -*- coding: utf-8 -*-

__doc__ = "Echantillonage des notices INTERMARC"

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
from collections import Counter


def scan_notices_dir(notices_dir="./notices"):
    for d in sorted(os.listdir(notices_dir), reverse=False):
        for d1 in sorted(os.listdir(os.path.join(notices_dir,d)), reverse=False):
            d2 = os.path.join(notices_dir,d, d1)
            for d3 in sorted(os.listdir(d2), reverse=False):
                d3 = os.path.join(d2, d3)
                for f in sorted(os.listdir(d3),reverse=False):
                    yield os.path.join(d3, f)

def get_notices(ref="./index_notices.txt"):
    with open(ref, "r") as f:
        notice_name = f.read()
    return notice_name.split('\n')

def read_notice(fname):
    '''read and build the soup'''
    fname = fname.replace("./bnopalex", "./notices")
    with open(fname, "r", encoding="utf-8") as f:
        notice = f.read()
        r = bs(notice, "lxml")
        # print(r.encoding)
        return r.record


def flatten_notice(r):
    '''flatten xml notice and index data are not casted :) '''
    record = {}
    record["format"] = r.get("format")
    record["type"] = r.get("type")
    record["_id"] = int(r.get("numero"))
    record.update({n.get("tag"): n.text.split('\n')[0] for n in r.find_all("controlfield")})
    for pos in r.find_all("pos"):
        #sous- zone à position
        if pos.parent.name == "subfield":
            # print(pos.parent.parent)
            # print(pos.parent.parent.parent)
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


def sampling():
    for n in scan_notices_dir(notices_dir="../notices"):
        print(n)

if __name__ == "__main__":
    sampling()
    # for i, n  in enumerate(scan_notices_dir(notices_dir="./notices")):
    #
    #     record = read_notice(n)
    #     build_tree(record)
