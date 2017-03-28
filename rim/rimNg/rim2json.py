#!/usr/bin/venv35 python3
# -*- coding: utf-8 -*-

import os
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt




def get_notices(ref="./index_notices.txt"):
    with open(ref, "r") as f:
        notice_name = f.read()
    return notice_name.split('\n')

typologie = {"Bibliography":{
                "notice":{
                        "ANL" : "Sous-notice analytique"
                        "COL" : "Notice de collection éditoriale",
                        "ENS" : "Notice d’ensemble monographique",
                        "HIS" : "Notice historique",
                        "MON" : "Notice autonome de monographie",
                        "PER" : "Notice de périodique",
                        "REC" : "Notice de recueil",
                        "SPE" : "Spectacle",
                        },
                "document": {
                    "CP" : "Ressource cartographique",
                    "IA" : "Image animée",
                    "IF" : "Image fixe",
                    "IMP" : "Texte imprimé",
                    "INF" : "Ressource électronique",
                    "MM" : "Multimédia multisupport",
                    "MSM" : "Manuscrit moderne et document d'archives",
                    "MUS" : "Musique",
                    "OBJ" : "Objet",
                    "SON" : "Document sonore",
                    "SPE" : "Spectacle"},
                },
            "Authority":{
                "GEO" : "Noms géographiques",
                "MAR" : "Marques",
                "ORG" : "Organismes",
                "PEP" : "Personnes physiques",
                "RAM" : "Autorités RAMEAU",
                "TIC" : "Titres uniformes conventionnels",
                "TUM" : "Titres uniformes musicaux",
                "TUT" : "Titres uniformes textuels"
            }

range_zones = {
    000:"guide",
    100:"vedette",
    200: "usage",
    300: "renvoi",
    400: "exclusion",
    500: "renvoi",
    600: "notes",
    900: "historique",
        }
zones_fixes = {
                "000": "guide",
                "001": "_id",
                "003": "uri",
                "008": "context",
                "017": "n_id_ext",
                "031": "isni"
              }
