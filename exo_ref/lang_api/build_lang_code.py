#!/usr/bin/env python3
# coding: utf-8

import string
import requests
from requests_futures.sessions import FuturesSession
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
import csv
from datetime import datetime as dt
import json

session = FuturesSession()
# conn = MongoClient()
# db = conn.referentials


def search_ref(code, lang = None):
    '''
    rechercher dans le référentiel officiel
    par nom de code ou de label dans les langues supportées
    (fr, de, en)
    '''
    if len(code) < 3:
        raise ValueError("Code must be set with 3 characters")

    url = 'http://id.loc.gov/search/?q='+code+'&q=cs%3Ahttp%3A%2F%2Fid.loc.gov%2Fvocabulary%2Fiso639-2'
    r = requests.get(url)
    results = []
    if r.status_code < 399:
        data = bs(r.text,"lxml")
        headers = [n.text.strip().lower().replace(" ", "_") for n in data.findAll("th")]
        cells = [(n.text).strip() for n in data.find("tbody").findAll("td")]
        ref = dict(zip(headers, cells))
        try:
            ref["labels"] = ref["label"].split(" | ")
            # ref.pop("label")

            ref["default_labels"] = dict(zip(["en", "fr", "de"], ref["label"].split(" | ")))
            if lang is not None and lang in ["en", "fr", "de"]:
                if len(code) > 3:
                    if ref["default_labels"][lang] == code:

                        return ref
                    else:
                        print("Name %s not Found" %code)
                        return None
                else:
                    return ref["default_labels"][lang]
            else:
                return ref
        except:
            print("Code %s not Found" %code)
            return None
    else:
        raise Exception("Network or provider is not available Error:", r.status_code)


# def search_labels():
#     '''
#     rechercher les labels depuis le référentiel bnf
#     '''
#
#     pass
#
# def search_code():





if __name__ =="__main__":

    # build_datastore_IDLOC()
    # conn = MongoClient()
    # db = conn.referentials
    build_datastore_BNF()
    # print(len(ref.keys()), len(db.lang_code.distinct("identifier")))
    # print(bnf_ref)
    # for record in db.lang_code.find():
    #     iid = record["identifier"]
    #     try:
    #         if record["label"][1] in ref[iid]:
    #             print('OK la valeur  pour %s est par défaut:%s' %(iid, record["label"][1]))
    #     except:
    #         ref[iid] = [record["label"][1]]
    #         print("Added", iid, ref[iid])
    # for k, v in ref.items():
    #     print(k,v)
    # for record in referentials.lang_code.find():
    #     print(record)
    #     print(record["code"], record["label"][1])
