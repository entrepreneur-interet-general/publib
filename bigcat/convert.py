#!usr/bin/env python3
# -*- coding: utf-8 -*-
'''
filename: convert.py
Convert interxmarc to json: flatten hierarchy,
and cast date and index into db
'''
from settings import ROOT
from db import *
import os
import sys
import re
from multiprocessing import Pool
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt

U_INT = re.compile(r'\d+', re.UNICODE)
U_NONINT = re.compile(r'[^(\d|\s)+]+', re.UNICODE)


def convert(fname):
    '''Convertir un fichier XML en JSON
    toutes hierarchies applaties a partir d'un numero de notice
     qui correspond a document interXmarc dans le filesystem
    '''
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
    def cast(value,key, sens=None):
        '''casting value using tips(based on keys and meaning) and basic patterns'''
        #replace _
        value = value.replace("_","0")
        nb = re.findall(U_INT, value)
        inv = re.findall(U_NONINT, value)
        if not "date" in key or "date" in sens:
            #search by key: max int overflow error > 8Bytes
            if len(nb) > 0 and len(inv) == 0:
                sizeofv = len(value)
                #default zerofill
                # if len(str(int(value))) == sizeofv:
                #     return int(value)
                # elif value.startswith("0"):
                #     return int(value).zfill(sizeofv)
                # else:
                return int(value).zfill(sizeofv)

        else:
            nb = re.findall(U_INT, value)
            inv = re.findall(U_NONINT, value)
            if len(nb) > 0:
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
            try:
                rang = attr.get("range")
                if rang is not None:
                    try:
                        pex_d[key].append({"sens":sens, "value": value, "range": int(rang)})
                    except KeyError:
                        pex_d[key] = [{"sens":sens, "value": value, "range": int(rang)}]
                else:
                    try:
                        pex_d[key].append({"sens":sens, "value": value, "range": None})
                    except KeyError:
                        pex_d[key] = [{"sens":sens, "value": value, "range": None}]
            except KeyError:
                pex_d[key] = {"sens":sens, "value": value}

        return pex_d

    record = {}
    record["source_file"] = path(fname)
    record["_id"] = fname
    try:
        with open(record["source_file"], "r", encoding="utf-8") as f:
            try:
                notice = f.read()
                r = bs(notice, "lxml").record

                record["format"] = r.get("format")
                record["type"] = r.get("type")

                record["nno"] = r.get("numero")

                positions = [get_pos(pos) for pos in r.find_all("pos")]
                subfields = [get_subfield(sub) for sub in r.find_all("subfield")]
                attributes = [get_attribute(att) for att in r.find_all("attr")]
                fields = positions+subfields+attributes
                fields_d = {n[0]:{"value":n[1], "sens":n[2]} for n in fields if n[0] is not None or n[1] is not None}
                # try:
                record.update(fields_d)
                if r.find("pex") is not None:
                    record["pexs"] =  [get_pex(pex) for pex in r.find_all("pex")]
                    record["nb_pex"]= len(record["pexs"])

                try:
                    print(fname, record["type"])
                    record["status"] = True
                    return coll.update({"_id": record["_id"]}, record, upsert=True)
                except Exception as e:
                    record["step"] = "upsert notice"
                    record["status"] = False
                    record["msg"] = str(e)
                    return coll.update({"_id": record["_id"]}, record, upsert=True)
                # except Exception as e:
                #     record["status"] = False
                #     record["msg"] = str(e)
                #     record["step"] = "adding fields"
                #     return coll.update({"_id": record["_id"]}, record, upsert=True)
            except Exception as e:
                print(e)
                record["status"] = False
                record["msg"] = str(e)
                record["step"] = "mapping conversion"
                return coll.update({"_id": record["_id"]}, record, upsert=True)
            # except Exception as e:
            #     print(e)
            #     sys.exit()
                # record["status"] = False
                # record["msg"] = str(e)
                # record["step"] = "reading file"
                # return coll.update({"_id": record["_id"]}, record, upsert=True)
    except FileNotFoundError:
        # record["status"] = False
        # record["flag"] = "new"
        # record["msg"] = "File not found"
        # record["step"] = "File not found"
        # return db.new.insert(record)
        # print(fname, record["source_file"], "not found")
        pass




def path(i):
    i = str(i)
    return os.path.join(ROOT, "/".join([str(i)[0], str(i)[1], str(i)[2:5], str(i)+".xml"]))

if __name__ == "__main__":
    from multiprocessing import Pool
    with Pool(9) as p:
        p.map(convert, [n for n in range(10000000, 17105274)])
        p.map(convert, [n for n in range(30000000, 45205089)])
