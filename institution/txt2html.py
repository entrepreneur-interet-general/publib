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
def create_html(fname="jargon.csv"):
    import csv

    with open(fname, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        header = '''<!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>%s</title>

    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

    <!-- Optional theme -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

    <!-- Latest compiled and minified JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->

  </head>
  <body><div id="container" class="container"><h2 align=center>Jargon interne de la BNF</h2>
  <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
  <!-- Latest compiled and minified JavaScript -->
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
                    '''%("Jargon BNF")
        search = '''<div class="form-group pull-right">
                    <input type="text" id="myInput" onkeyup="myFunction()" placeholder="Rechercher un trigramme..">
                    </div>
                    <span class="counter pull-right"></span>'''

        page = '''<table id="jargonTable" class="table  table-list-search table-bordered">
                      <thead class="thead-inverse">
                        <tr>
                        <th>Trigramme</th>
                        <th>Explication</th>
                        <th>Organigramme</th>
                        </tr>
                      </thead>
                      <tbody>'''
        footer = '''</div><body></html>'''
        for line in reader:
            page +='''<tr id="%s">
                          <td class="trigramme">%s</td>
                          <td class="trigramme-edit">%s</td>
                          <td class="organigramme">%s</td>
                        </tr>'''%(line[0],line[0], line[1], line[2])
        page += '''</tbody>
                    </table>'''
        script = '''<script type="text/javascript">

function myFunction() {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("jargonTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}
</script>
                '''

        return header+search+page+script+footer



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

def plotly_graph():
    # import plotly.plotly as py
    # from plotly.graph_objs import *
    # import igraph
    # from igraph import *
    pass
#http://intranotes/bnf/organigrammebnf.nsf/wsearch?SearchView&Start=1&Count=0&SearchMax=0&SearchWV=FALSE&SearchOrder=4&SearchFuzzy=FALSE&Seq=1&Query=FIELD%20NOM%20CONTAINS%20A*%20OR%20FIELD%20PRENOM%20CONTAINS%20A*%20OR%20FIELD%20LOCATIONNAME%20CONTAINS%20A*%20OR%20FIELD%20TELEPHONE%20CONTAINS%20A*%20OR%20FIELD%20TELEPHONE2%20CONTAINS%20A*&prov=4&requete=A
if __name__=="__main__":
    jargon_list = txt2list(fname="./jargon.txt")
    jargont = list2tree(jargon_list)
    with open("jargon.html", "w") as f:
        html = create_html(fname="./jargon.csv")
        f.write(html)
    # graph = tree2graph(jargont)
    # draw_graph(graph)
    # draw_tree(graph)
