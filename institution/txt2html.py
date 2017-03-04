# coding: utf-8
#/usr/bin/env/python
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import json
import graphviz as gv
# from networkx.drawing.nx_agraph import write_dot
# from nxpd import draw

def txt2list(fname="./jargon.txt"):
    '''from jargon list return a list'''
    with open(fname, "r") as f:
        data = f.read().split("\n")
        # print(f.readline())
        trig, desc, tree = [], [], []
        for no, line in enumerate(data):
            # print(line, no%3)
            if no%3 == 0:
                if len(line) == 3:
                    trig.append(line)
                # else:
                #     print(line)
            elif no%3 == 1:
                desc.append(line)
            elif no%3 == 2:
                tree.append(line)
    return list(zip(trig, desc, tree))

def txt2csv(fname, listA):
    with open("jargon.csv", "w") as f:
        for n in listA:
            f.write("\t".join(n)+"\n")
    return
def list2tree(listA):
    tree = {}
    for n in listA:
        paths = n[2].split("/")
        tree[n[0]] = {"tree": paths, "def":n[1]}
    return tree

def tree2graph(trees):
    G = nx.DiGraph()
    for k, v in trees.items():
        # for n in v["tree"]:

        G.add_cycle(v["tree"])
    pos = nx.spectral_layout(G)
    # pos=nx.spring_layout(G)
    nx.set_node_attributes(G,'pos',pos)
    return G

def draw_tree(g, index):
    g1 = gv.Digraph(comment='Les trigrammes', format="svg")
    for e in g.edges():
        # print(e)
        # try:
        #     g1.node(e[0], index[e[0]])
        # except:
        #     pass
        g1.edge(e[0], e[1])
    filename = g1.render(filename='trigrammes')
    print(g1)
    # g1.write_png('example1_graph.png')
def draw_graph(g):
    nx.draw(g, with_labels=True, with_arrows=True)
    plt.savefig("digraph.png") # save as png
    plt.show()
    return g


def graph2gexf(graph):
     nx.write_gexf(graph, "test.gexf")

def tree2json(fname ="./jargon.txt"):
    listA = txt2list(fname)
    indexA = {n[0]: n[1] for n in listA}
    tree = list2tree(listA)

    G = tree2graph(tree)
    print(G.nodes())

    nodes= []
    for i,n in enumerate(G.nodes()):
        try:
            nodes.append({"id":n, "label": indexA[n], "size": G.degree(n)})
        except KeyError:
            nodes.append({"id":n, "label": "Pas de correspondance trouvée", "size": G.degree(n)})
    edges = [{"id":"e"+str(i), "source":n[0], "target":n[1]} for i,n in enumerate(G.edges())]
    obj = {"nodes":nodes, "edges":edges}
    return json.dumps(obj, indent=4)

def build_static(G):
    # use 'with' if you are writing a script and want to serve this up forever
    with d3py.NetworkXFigure(G, width=500, height=500) as p:
        p += d3py.ForceLayout()
        p.show()
    # return static

#http://intranotes/bnf/organigrammebnf.nsf/wsearch?SearchView&Start=1&Count=0&SearchMax=0&SearchWV=FALSE&SearchOrder=4&SearchFuzzy=FALSE&Seq=1&Query=FIELD%20NOM%20CONTAINS%20A*%20OR%20FIELD%20PRENOM%20CONTAINS%20A*%20OR%20FIELD%20LOCATIONNAME%20CONTAINS%20A*%20OR%20FIELD%20TELEPHONE%20CONTAINS%20A*%20OR%20FIELD%20TELEPHONE2%20CONTAINS%20A*&prov=4&requete=A
if __name__=="__main__":
    jargon_list = txt2list(fname="./jargon.txt")
    jargont = list2tree(jargon_list)
    graph = tree2graph(jargont)
    # draw_graph(graph)
    draw_tree(graph)
    # build_static(graph)
    # graph2gexf(graph)
    # data = tree2json("./jargon.txt")
    # with open("jargon.json", "w") as f:
    #     f.write(data)
    # with open("jargon.html", "w") as f:
    #     data = build_static("jargon.json")
    #     f.write(data)
