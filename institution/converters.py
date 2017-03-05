# coding: utf-8
#/usr/bin/env/python
import json
import csv
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader, select_autoescape

import graphviz as gv
import networkx as nx
import igraph as ig
import plotly.plotly as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go

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
    return filehandler
    '''
    listin = txt2list(fin)
    env = Environment(
        loader=FileSystemLoader('./templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('jargon.html')
    htmlout = template.render(data=listin, title="Jargon de la BNF")
    with open(fout, "w") as f:
        f.write(htmlout)
        return f

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
    listin = csv2list(fin)
    env = Environment(
        loader=FileSystemLoader('./templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('jargon.html')
    htmlout = template.render(data=listin, title="Jargon de la BNF")
    with open(fout, "w") as f:
        f.write(htmlout)
        return f


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

def json2html(fin, fout):
    with open(fin, "r") as f:
        jsonin = json.loads(f)
    listin = json2list(jsonin)
    env = Environment(
        loader=FileSystemLoader('./templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('jargon.html')
    htmlout = template.render(data=listin, title="Jargon de la BNF")
    with open(fout, "w") as f:
        f.write(htmlout)
        return f

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
    '''convert given JSON to DICT'''
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
    tree = []
    for n in in listin:
        tree.append([n[2].split("/"))
    return tree

def dict2tree(dictin):
    tree = []
    for n in in dictin.values():
        tree.append([n["hierarchy"].split("/"))
    return tree

def dict2digraph(dictin, module="nx"):
    '''create a graph specifying the python module'''
    if module = "nx":
        G = nx.DiGraph()
        for k, v in dictin.items():
            G.add_node(k, definition=v["definition"])
            G.add_path(v["hierarchy"].split("/"))
        return G
    elif module == "gv":
        G = gv.DiGraph()
        for k, v in dictin.items():
            G.node(k, v["definition"])
            G.edges(v["hierarchy"].split("/"))
        return G
    elif module == "ig":
        G = gv.DiGraph()
        for k, v in dictin.items():
            G.add_vertice(k, definition= v["definition"])
            G.add_edges((v["hierarchy"].split("/"))
        return G
    else:
        raise Exception("Module %s Not Found" %module)

def graph2img(G, imgout, module="ig"):
    if module == "ig":
        layout = G.layout('rt')
        #https://plot.ly/python/tree-plots/#basic-treeplot-in-plotly-with-igraph
    elif module == "gv":
        G["format"]=imgout.split(".")[-1]
        return g1.render(filename=imgout)
    elif module == "nx":
        nx.draw(g, with_labels=True, with_arrows=True)
        plt.savefig(imgout) # save as png
        plt.show()
    else:
        raise Exception("Module %s Not Found" %module)
def graph2html(G, imgout, module="ig"):
    raise NotImplementedError

class FileConverter():
    ACC_FORMAT = ["txt", "csv", "json", "html"]
    def __init__(self, fin, fout):
        fmtin, fmtout = fin.split(".")[-1], fout.split(".")[-1]
        if fmtin not in self.ACC_FORMAT:
            raise Exception("Incorrect input filetype")
        if fmtout not in self.ACC_FORMAT:
            raise Exception("Incorrect output filetype")
        method = eval(fmtin+"2"+fmtout)
        method(fin, fout)


if __name__ == "__main__":
    f = FileConverter("jargon.txt", "jargon2.html")
