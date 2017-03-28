#!/usr/bin/env/python3
# coding: utf-8
__doc__ ==  '''build a master dataset by merging master_ref
            with the corresponding referentials
            key = 1 **code** is a simple value composed by
            - format (type of notice)
            - zone, subzone, position
            value = acceptable values extracted
            from the corresponding referentials expressed as
            key: value
            #key being the code used in the targeted format
            #value being the signification of the code
            e.g:
            #Référentiels externes
            {<ref_name>:{"values":{<code_k>:<definition>, ....}
                         "zones":[<zone$sszone£pos_type>, ...]
                        },

            '''
import csv
from collections import Counter
import plotly
from plotly.graph_objs import Scatter, Layout

def create_master(fn="./ref_exo_master.csv"):
    '''create a database with all the referentials name alongs with the values and the corresponding
    zones from csv'''
    zone_d = {}
    zone_l = []
    referential_d = {}
    referential_l = []
    with open(fn) as f:
        reader = csv.DictReader(f, delimiter= "\t")
        for row in reader:
            #['Position(s)', 'Type', 'Sous-zone', 'Format', 'Zone', 'Référentiel', 'Lignes']
            zone, name = row["Type"]+"_"+row["Zone"]+row["Sous-zone"]+"P"+row["Position(s)"], row["Référentiel"]
            zone_l.append(zone)
            referential_l.append(name)
    for zone, freq in Counter(zone_l).items():
        if freq > 1:
            print(zone)
    # print(Counter(referential_l))
            # break


if __name__ == "__main__":
    create_master()
