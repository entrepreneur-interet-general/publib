#!/usr/bin/venv35 python3
# -*- coding: utf-8 -*-
from settings import ROOT, COLL, pymongo
from bs4 import BeautifulSoup as bs

import os
from datetime import datetime as dt
from multiprocessing import Pool
import json
import re

U_INT = re.compile(r'\d+', re.UNICODE)
U_NONINT = re.compile(r'[^(\d|\s)+]+', re.UNICODE)


from multiprocessing import Pool

def get_notices_f(notices_dir="/notices/xml/ixm/bnopalex/"):
    ''' retourne les notices présentes dans l'arborescence une par une'''
    for d in sorted(os.listdir(notices_dir), reverse=False):
        for d1 in sorted(os.listdir(os.path.join(notices_dir,d)), reverse=False):
            d2 = os.path.join(notices_dir,d, d1)
            for d3 in sorted(os.listdir(d2), reverse=False):
                d3 = os.path.join(d2, d3)
                for f in sorted(os.listdir(d3),reverse=False):
                    fname = os.path.join(d3, f)
                    yield(fname)
                    #croisé avec la base de données
                    # if COLL.findOne({"source_file": fname}) is None:
                    #     yield fname


def is_new(fname):
    '''Le fichier n'est pas dans la base'''
    if COLL.find_one({"source_file": fname}) is None:
        print(fname)
        return fname
    else:
        return None

def get_new_notices_f():
    '''Distinct list of notices not indexed'''
    return list(filter(is_new(x), get_notices_f))

def get_indexed_files():
    for i in range(10000000, 20000000):
        print(i)

def convert(i):
    '''Convertir un fichier XML en JSON
    toutes hierarchies applaties
    '''
    def get_file(i):
        fname = str(i)+".xml"
        return os.path.join(ROOT, "/".join([fname[0], fname[1], fname[2:5],fname]))

    def get_subfield(sub):
        '''
        Pour une sous-zone récupérer tous les champs data
        '''

        if sub.parent.name == "datafield":
            tag = sub.parent.get("tag")
            code = sub.get("code")
            if code == ".":
                code = "0"
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

    def get_pos(pos):
        '''pour chaque tag "pos"
        renvoyer son tag parent ou grand parent
        le code, le sens
        '''

        if pos.parent.name == "subfield":
            tag = pos.parent.parent.get("tag")
            #pymongo.errors.WriteError: The dotted field '144$.' in '144$.' is not valid for storage
            code = pos.parent.get("code")
            if code == ".":
                code = "*"
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
            #pymongo.errors.WriteError: The dotted field '144$.' in '144$.' is not valid for storage
            code = pos.get("code")
            if code == ".":
                code = "*"
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

    def cast(value,key, sens=None):
        '''casting value using tips(based on keys and meaning) and basic patterns'''
        nb = re.findall(U_INT, value)
        inv = re.findall(U_NONINT, value)

        #si toutes les valeurs sont numériques
        if len(inv) == 0 and len(nb) > 0:
            if len(nb) == 1:
                if len(nb[0]) > 1 and nb[0].startswith("0"):
                    #maintenir le zerofill
                    return nb[0]
                else:
                    #sinon  '0' > 0
                    return int(value)
            else:
                try:
                    return int(value)
                except:
                    return value
        #si on trouve 3 suite de nombres
        elif len(nb) == 3:
            if key is not None and "date" in key:
                return cast_date(nb)
            if sens is not None and "date" in sens:
                return cast_date(nb)
            else:
                return value
        #si la valeur est de 0 => None
        elif len(nb) == 1 and  int(nb[0]) == 0:
            return None
        else:
            return value

    def cast_date(nb):
        size_of = [len(n) for n in nb]
        if size_of == [2,2,4]:
            return dt.strptime("-".join(nb), "%d-%m-%Y")
        elif size_of == [4,2,2]:
            return dt.strptime("-".join(nb), "%Y-%m-%d")
        else:
            return "-".join(nb)


    fname = get_file(i)
    if fname is not None:
        #debug:
        try:
            with open(fname, "r", encoding="utf-8") as f:
                record = {}
                record["source_file"] = fname
                record["_id"] = i
                try:
                    notice = f.read()
                    r = bs(notice, "lxml").record
                    try:
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

                        except Exception as e:
                            record["status"] = False
                            record["msg"] = str(e)
                            record["step"] = "adding fields"

                    except Exception as e:
                        record["status"] = False
                        record["msg"] = str(e)
                        record["step"] = "get data from <record>"

                except Exception as e:
                    record["status"] = False
                    record["msg"] = str(e)
                    record["step"] = "mapping conversion"
            try:
                COLL.insert(record)
            except pymongo.errors.DuplicateKeyError:
                pass
        except FileNotFoundError:
            pass
    else:
        pass

def get_file(i):
    '''recomposition du chemin du fichier notice.xml a partir de son numéro'''
    fname = str(i)+".xml"
    return os.path.join(ROOT, "/".join([fname[0], fname[1], fname[2:5],fname]))

def sampling_f():
    '''sampling 10% of total nBIB when 200000<= nbib > 460000
    total_nBib = 13659395
    sample_10 = int(round((total_nBib/10)))
    we take more than 10% because notice_nb can either exists or not
    '''
    import numpy as np
    return(list(np.random.randint(20000000, 46000000, 2000000)))

def get_notices_auth():
    '''generer l'ensemble des notices XML
    Les notices AUT  sont comprises entre 10M et 17M106000'''
    return [get_file(i) for i in range(10000000, 17106000)]

def get_notices_bib():
    '''generer l'ensemble des notices BIB qui sont comprises entre
    20M et 46M'''
    return [get_file(i) for i in range(20000000, 46000000)]


if __name__ == "__main__":
    #Multithreading via Cython using POOL
    p = Pool(5)
    #Sampling nBIB
    #p.map(convert, sampling_f())
    #AUT
    #p.map(convert, get_notices_auth())
    #BIB
    #p.map(convert, get_notices_bib())
