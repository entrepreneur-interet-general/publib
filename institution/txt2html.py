#/usr/bin/env/python
import networkx as nx
import matplotlib.pyplot as plt

with open("./jargon.txt", "r") as f:
    data = f.read().split("\n")
    # print(f.readline())
    trig, desc, tree = [], [], []
    for no, line in enumerate(data):
        # print(line, no%3)
        if no%3 == 0:
            if len(line) == 3:
                trig.append(line)
            else:
                print(line)
        elif no%3 == 1:
            desc.append(line)
        elif no%3 == 2:
            tree.append(line)
with open("jargon.csv", "w") as f:
    G = nx.DiGraph()
    for n in zip(trig, desc, tree):
        G.add_node(n[0])
        f.write("\t".join(n)+"\n")
        tree = n[2].split("/")
        G.add_path(tree)
    nx.draw_graphviz(G, hold=False, with_labels=True)
    # plt.savefig("testA.png") # save as png
    plt.show()

        # for i,d in enumerate(tree):
        #     G.add_edges(d, tree[i])

#http://intranotes/bnf/organigrammebnf.nsf/wsearch?SearchView&Start=1&Count=0&SearchMax=0&SearchWV=FALSE&SearchOrder=4&SearchFuzzy=FALSE&Seq=1&Query=FIELD%20NOM%20CONTAINS%20A*%20OR%20FIELD%20PRENOM%20CONTAINS%20A*%20OR%20FIELD%20LOCATIONNAME%20CONTAINS%20A*%20OR%20FIELD%20TELEPHONE%20CONTAINS%20A*%20OR%20FIELD%20TELEPHONE2%20CONTAINS%20A*&prov=4&requete=A
