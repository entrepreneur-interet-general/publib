# coding: utf-8
#/usr/bin/env/python
import json
import csv
import pdfminer
#import docx
import os
from docopt import docopt
from jinja2 import Template, Environment, FileSystemLoader , select_autoescape


import graphviz as gv
import networkx as nx
import jgraph as ig
import plotly.plotly as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go
# __name__ = "Converter"
__version__="0.0.1"
__doc__ = '''
        File converter
        Trying to solve the format nightmare:
        * fileconverter
        * datatype cast
        Filetype supported:
        - pdf
        - text
        - csv
        - json
        - html
        - png (only from graph to png)
        Datatype supported:
        - txt(str)
        - list
        - dict
        - digraph (directed graph)

        Usage:
        converters.py -i <file_in> -o <file_out>

         '''


class FileConverter():

    ACC_TYPE = ["str", "list", "dict", "digraph"]
    def __init__(self, fin, fout):
        self.ACC_EXT = ["pdf","png", "txt", "csv", "json", "html", "str", "list", "dict", "digraph"]
        ext_in, ext_out = fin.split(".")[-1], fout.split(".")[-1]
        print(ext_in, ">>>>", ext_out)
        if ext_in not in self.ACC_EXT:
            raise Exception("Incorrect input filetype")
        if ext_out not in self.ACC_EXT:
            raise Exception("Incorrect output filetype")
        method = eval("self."+ext_in+"2"+ext_out)
        print("%s sucessfully converted to %s" %(fin, fout))
    def pdf2doc(self, fin, fout="jargon.docx"):
        pass

    def doc2pdf(self, fin, fout="jargon.pdf"):
        pass

    def pdf2txt(self, fin, fout="jargon.txt"):
        os.system('pdf2txt %s %s' %(fin,fout))
        return

    def txt2pdf(self,fin, fout="jargon.pdf"):
        pass

    def doc2txt(self, fin, fout="jargon.txt"):
        pass
    def txt2doc(self, fin, fout="jargon.docx"):
        pass

    def txt2csv(self, fin, fout="jargon.csv"):
        '''
        convert txt to csv
        return filehandler
        '''
        listin = txt2list(fin)
        with open(fout, "w") as f:
            for n in listin:
                f.write("\t".join(n)+"\n")
        return f

    def txt2json(self, fin="jargon.txt", fout="jargon.json"):
        '''convert txt to json
        return filehandler
        '''
        listin = txt2list(fin)
        dictin = list2dict(listin)
        with open(fout, "w") as f:
            data = json.dumps(dictin, indent=4)
            f.write(data)
        return f

    def txt2html(self, fin="jargon.txt", fout="jargon.html"):
        '''convert txt to html
        return filehandler
        '''
        listin = txt2list(fin)
        env = Environment(
            loader=FileSystemLoader('./templates'),
            #autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('jargon.html')
        htmlout = template.render(data=listin, title="Jargon de la BNF")
        with open(fout, "w") as f:
            f.write(htmlout)
            return f

    def csv2text(self, fin="./jargon.csv", fout="./jargon.txt"):
        '''convert csv to txt
        return filehandler
        '''
        with open(fin, "r") as f:
            reader = csv.reader(f)
            txtout = "/n".join([line for line in reader])
        with open(fout, "w") as f:
            f.write(txtout)
            return f

    def csv2json(self, fin="./jargon.csv", fout="./jargon.json"):
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

    def csv2html(self, fin="jargon.csv", fout="jargon.html"):
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


    def json2txt(self, fin="./jargon.json", fout="./jargon.txt"):
        '''convert given JSON to TXT
        return filehandler'''
        with open(fin, "r") as f:
            jsonin = json.loads(f)
        with open(fout, "w") as f:
            txtout = "/n".join(jsonin.values())
            f.write(txtout)
            return f

    def json2csv(self, fin="./jargon.json", fout="./jargon.txt"):
        '''convert given JSON to CSV
        return filehandler'''
        with open(fin, "r") as f:
            jsonin = json.loads(f)

        with open(fout, "w") as f:
            for v in jsonin.values():
                f.write("\t".join(v)+"\n")
            return f

    def json2html(self, fin, fout):
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

    def txt2list(self, fin="./jargon.txt"):
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

    def csv2list(self, fin="./jargon.csv"):
        '''convert given CSV to LIST'''
        # trig, desc, tree = [], [], []
        with open(fin, "r") as f:
            reader = csv.reader(f)
            listout = [line for line in reader]
        return listout

    def json2list(self, fin="./jargon.json"):
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

    def txt2dict(self, fin="./jargon.txt"):
        '''convert given TXT to DICT'''
        listin = txt2list(fin)
        return list2dict(listin)

    def csv2dict(self, fin="./jargon.csv"):
        '''convert given CSV to DICT'''
        with open(fin, "r") as f:
            reader = csv.reader(f)
            dictout = {line[0]:{"hierarchy":line[2], "description": line[1]} \
                        for line in reader}
        return dictout

    def json2dict(self, fin="./jargon.json"):
        '''convert given JSON to DICT'''
        with open(fin, "r") as f:
            dictout = json.loads(f)
            return dictout

    def list2dict(self, listin):
        '''
        from a list of 3 element convert it 2 dict with unique trigram
        {trig:{"hierarchy": "XXX/XXX/XXX/", "definition":"txt"}
        '''
        dictout = {}
        for n in listin:
            dictout[n[0]] = {"hierarchy": paths, "definition":n[1]}
        return dictout

    def list2tree(self, listin):
        tree = []
        for n in listin:
            tree.append(n[2].split("/"))
        return tree

    def dict2tree(self, dictin):
        tree = []
        for n in dictin.values():
            tree.append(n["hierarchy"].split("/"))
        return tree

    def dict2digraph(self,dictin, module="nx"):
        '''create a graph specifying the python module'''
        if module == "nx":
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
                G.add_edges(v["hierarchy"].split("/"))
            return G
        else:
            raise Exception("Module %s Not Found" %module)

    def graph2img(self, G, imgout, module="ig"):
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
    def graph2html(self, G, imgout, module="ig"):
        raise NotImplementedError

if __name__ == "__main__":
    args = docopt(__doc__)
    print(args)
    try:
        FileConverter(args["<file_in>"], args["<file_out>"])
    except KeyError:
        print("Invalid arguments")
        print(__doc__)
