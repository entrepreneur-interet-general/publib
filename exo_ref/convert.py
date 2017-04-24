#!/usr/bin/venv3 python3
# coding: utf-8
__doc__ == '''
Depuis le fichier XLS constitué à partir des documents pdf donnés:
conversion et manipulation en CSV.
Conversion initiale des données vers une base de données structurée
Import/Export CSV BDD
'''
import csv
import json

class Convertor(object):
    def __init__(self, infile, outfile):
        self.infile = in
        self.outfile = out
    def csv2json(self):
        '''delimiter = '\t', subdelimiter=","'''
