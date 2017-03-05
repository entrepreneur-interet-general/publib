# coding: utf-8
#/usr/bin/env/python
import json
import csv
import graphviz as gv
import plotly.plotly as py
import plotly.graph_objs as go
import networkx as nx
import matplotlib.pyplot as plt

# import jgraph
# from jgraph import *

__doc__ = '''
        The format nightmare:
        * fileconverter
         TXT > CSV
         TXT > JSON
         TXT > HTML

         CSV > TXT
         CSV > JSON
         CSV > HTML

         JSON > TXT
         JSON > CSV
         JSON > HTML
        * datatype cast:
        TXT > LIST
        TXT > DICT
        TXT > GRAPH

        CSV > LIST
        CSV > DICT
        CSV > GRAPH

        JSON > LIST
        CSV > DICT
        CSV > GRAPH
         '''

def txt2csv(fin, fout="jargon.csv"):
    '''
    convert txt to csv
    return filehandler
    '''
    listin = txt2list(fin)
    with open(fout, "w") as f:
        for n in listin:
            f.write("\t".join(n)+"\n")
    return f

def txt2json(fin="jargon.txt", fout="jargon.json"):
    '''convert txt to json
    return filehandler
    '''
    listin = txt2list(fin)
    dictin = list2dict(listin)
    with open(fout, "w") as f:
        data = json.dumps(dictin, indent=4)
        f.write(data)
    return f

def txt2html(fin="jargon.txt", fout="jargon.html"):
    '''convert txt to html
    return staticfile
    '''
    pass
def csv2text(fin="./jargon.csv", fout="./jargon.txt"):
    '''convert csv to txt
    return filehandler
    '''
    with open(fin, "r") as f:
        reader = csv.reader(f)
        txtout = "/n".join([line for line in reader])
    with open(fout, "w") as f:
        f.write(txtout)
        return f

def csv2json(fin="./jargon.csv", fout="./jargon.json"):
    '''convert given CSV to JSON
    return filehandler'''
    with open(fin, "r") as f:
        reader = csv.reader(f)
        dictout = {line[0]:{"hierarchy":line[2], "description": line[1]} \
                    for line in reader}
    with open(fout, "w") as f:
        data = json.dumps(dictout, indent=4)
        f.write(data)
        return f

def csv2html(fin="jargon.csv", fout="jargon.html"):
    '''convert csv to html
    return staticfile
    '''
    pass

def json2txt(fin="./jargon.json", fout="./jargon.txt"):
    '''convert given JSON to TXT
    return filehandler'''
    with open(fin, "r") as f:
        jsonin = json.loads(f)
    with open(fout, "w") as f:
        txtout = "/n".join(jsonin.values())
        f.write(txtout)
        return f

def json2csv(fin="./jargon.json", fout="./jargon.txt"):
    '''convert given JSON to CSV
    return filehandler'''
    with open(fin, "r") as f:
        jsonin = json.loads(f)

    with open(fout, "w") as f:
        for v in jsonin.values():
            f.write("\t".join(v)+"\n")
        return f

def json2html():
    with open(fin, "r") as f:
        jsonin = json.loads(f)
    pass

def txt2list(fin="./jargon.txt"):
    '''convert given TXT to LIST'''
    trig, desc, tree = [], [], []
    with open(fin, "r") as f:
        data = f.read().split("\n")
        # print(f.readline())
        for no, line in enumerate(data):
            if line != "":
                if no%3 == 0:
                    trig.append(line)
                elif no%3 == 1:
                    desc.append(line)
                elif no%3 == 2:
                    tree.append(line)
    return list(zip(trig, desc, tree))

def csv2list(fin="./jargon.csv"):
    '''convert given CSV to LIST'''
    # trig, desc, tree = [], [], []
    with open(fin, "r") as f:
        reader = csv.reader(f)
        listout = [line for line in reader]
    return listout

def json2list(fin="./jargon.json"):
    '''convert given JSON to LIST
    not interest but complete
    '''
    listout = []
    with open(fin, "r") as f:
        reader = json.loads(f)
        for k, v in reader.items():
            v.prepend(k)
            listout.append(v)
    return listout

def txt2dict(fin="./jargon.txt"):
    '''convert given TXT to DICT'''
    listin = txt2list(fin)
    return list2dict(listin)

def csv2dict(fin="./jargon.csv"):
    '''convert given CSV to DICT'''
    with open(fin, "r") as f:
        reader = csv.reader(f)
        dictout = {line[0]:{"hierarchy":line[2], "description": line[1]} \
                    for line in reader}
    return dictout

def json2dict(fin="./jargon.json"):
    '''convert given CSV to DICT'''
    with open(fin, "r") as f:
        dictout = json.loads(f)
    return dictout

def list2dict(listin):
    '''
    from a list of 3 element convert it 2 dict with unique trigram
    {trig:{"hierarchy": "XXX/XXX/XXX/", "definition":"txt"}
    '''
    dictout = {}
    for n in listin:
        dictout[n[0]] = {"hierarchy": paths, "definition":n[1]}
    return dictout

def list2tree(listin):
    pass
def dict2tree(dictin):
    pass

class FileConverter():
    ACC_FORMAT = ["txt", "csv", "json", "html"]
    def __init__(self, fin, fout):
        fmtin, fmtout = fin.split(".")[-1], fout.split(".")[-1]

        method = eval(fmtin+"2"+fmtout)
        method(fin, fout)

class TypeCast():
    def __init__(self, tin, tout):
        pass

if __name__ == "__main__":
    f = FileConverter("jargon.txt", "jargon2.csv")
