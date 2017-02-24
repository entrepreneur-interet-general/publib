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
import networkx as nx
import matplotlib.pyplot as plt


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
def read_notice(fname):
    '''read and build the soup'''
    fname = fname.replace("./bnopalex", "./notices")
    with open(fname, "r", encoding="utf-8") as f:
        notice = f.read()
        r = bs(notice, "lxml")
        # print(r.encoding)
        return r.record


def flatten_notice(r):
    '''flatten xml notice and index it converters next time :) '''
    record["format"] = r.get("format")
    record["type"] = r.get("type")
    record["_id"] = int(r.get("numero"))
    record.update({n.get("tag"): n.text.split('\n')[0] for n in r.find_all("controlfield")})
    for pos in r.find_all("pos"):
        #sous- zone à position
        if pos.parent.name == "subfield":
            print(pos.parent.parent)
            print(pos.parent.parent.parent)
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

def build_tree(r):
    record = {}
    record["format"] = r.get("format")
    record["type"] = r.get("type")
    record["_id"] = int(r.get("numero"))
    #level 0
    root = "record"
    level = 0
    print("______")
    print(record["_id"])
    for pos in r.find_all("pos"):
        if pos.parent.name == "controlfield":
            pass
            # if pos.get("sens") is None:
            #     pass
            # else:
                #level 3
            # print("root>",pos.parent.get("tag"),">",pos.get("code"), ">", pos.text)
                # print(pos.parent.get("tag"), pos.get("code"), pos.get("sens"), pos.text)
            # pass
        elif pos.parent.name == "leader":
            pass
            # print("root>","000",">",pos.get("code"),  pos.get("sens"), ">", pos.text)
            #level 1
            # print("root", ">", "000", pos.get("code"),">", pos.text)
            # pass

        elif pos.parent.parent.name == "datafield":
            pass
            # print("root>",pos.parent.parent.get("tag"),">",pos.parent.get("code"), ">", pos.get("code"), ">", pos.text)
            # print(pos.parent.parent.get("tag"), pos.parent.get("code")
#             <datafield ind1=" " ind2=" " tag="621">
            # <subfield code="u">19220824<pos code="0003">1922</pos>
        else:
            print("!!!!!!", pos.parent.name)
    #pos a déjà été traité
    clean = [pos.extract() for pos in r.find_all("pos")]

    for subf in r.find_all("subfield"):
        #pos a déjà été traité
        clean = [pos.extract() for pos in subf.find_all("pos")]
        if subf.parent.parent.name == "record":
            #subf.Parent = "datafield"
            print("root>", subf.parent.get("tag"),">", subf.get("code"),">", subf.text.strip())
            pass
        else:
            print("root",">>", subf.parent.parent.get("ori"))
            #issu notice d'autorite subf.parent.parent.get("ori"))
            #subf.parent.name == "datafield"
            print("root>", subf.parent.get("tag"),">", subf.get("code"),">", subf.text.strip())
            # print("root",">", "400", subf.parent.parent.get("ori"))

    # G = nx.DiGraph()
    #
    # G.add_node(record.values())
    #
    # for i in xrange(5):
    #     G.add_node("Child_%i" % i)
    #     G.add_node("Grandchild_%i" % i)
    #     G.add_node("Greatgrandchild_%i" % i)
    #
    #     G.add_edge("ROOT", "Child_%i" % i)
    #     G.add_edge("Child_%i" % i, "Grandchild_%i" % i)
    #     G.add_edge("Grandchild_%i" % i, "Greatgrandchild_%i" % i)
    #
    #     # write dot file to use with graphviz
    #     # run "dot -Tpng test.dot >test.png"
    #     nx.write_dot(G,'test.dot')
    #
    #     # same layout using matplotlib with no labels
    #     plt.title("draw_networkx")
    #     pos=nx.graphviz_layout(G,prog='dot')
    #     nx.draw(G,pos,with_labels=False,arrows=False)
    #     plt.savefig('nx_test.png')

if __name__ == "__main__":
    for i, n  in enumerate(scan_notices_dir(notices_dir="./notices")):

        record = read_notice(n)
        build_tree(record)
