from requests_futures.sessions import FuturesSession
from pymongo import MongoClient
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
import csv
default_lang = ["en", "fr", "de"]

def store_ref(db):
    '''Write the full table of country codes from standard maintener
    inside a db
    '''
    # db.dropCollection()

    session = FuturesSession()
    urls = ["http://id.loc.gov/search/?q=cs:http://id.loc.gov/vocabulary/iso639-2&start=%i"%i for i in range(1, 521, 20)]
    conn = MongoClient()
    db = conn.ref


    def store_results(future):
        response = future.result()
        headers = ["id", "label", "vocabulary","concept_type","subdivision","identifier"]
        # defaultdict.fromkeys(headers)
        data = bs(response.text, "lxml").find("tbody")
        #print(data)
        for i, n in enumerate(data.findAll("tr")):
            if i%2 == 1:
                pass
            else:
                # print(len(n.findAll("td")))
            # print([cell.text.strip() for cell in n.findAll("td")])
                doc = dict(zip(headers, [cell.text.strip() for cell in n.findAll("td")]))
                doc["labels"] = [n.strip() for n in doc["label"].split("|")]
                doc["uri"] = "http://id.loc.gov/vocabulary/iso639-2/%s" %doc["identifier"]
                doc["date"] = [dt.today()]
                doc["author_uri"] = ["http://id.loc.gov/"]
                doc["action"] =  ["creation"]
                nb_default = len(doc["labels"])
                doc["default_label"] = dict(zip(default_lang[0:nb_default], doc["labels"][0:nb_default]))
                db.lang_ref.insert(doc)


    for url in urls:
        future = session.get(url)
        future.add_done_callback(store_results)

def build_bnf():
    '''construire le référentiel de la BNF
    {"fre":[Label1, Label2, Label3, ...]}
    '''
    ref = {}
    with open("./data/code_lang_BNF.csv", "r", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            labels = row['Libellé'].replace(".", "",).split(" => ")

                #     ref[row["Code"]] = {"default_label":{"fr": default}}
            try:
                ref[row["Code"]]["labels"].append(labels[0])
                if len(labels) > 1:
                    ref[row["Code"]]["default_label"] = {"fr":labels[1]}


            except KeyError:
                ref[row["Code"]]= {"labels":[labels[0]]}
                if len(labels) > 1:
                    ref[row["Code"]]["default_label"] = {"fr":labels[1]}
            ref[row["Code"]]["date"] = [dt.now()]
    return ref

def store_bnf(db):
    '''stocker le referentiel dans une BDD
    pour une première fois
    '''
    ref = build_bnf()
    conn = MongoClient()
    db = conn.ref
    for k, v in ref.items():
        try:
            default = v["default_label"]
        except KeyError:
            default = {"fr":None}
        db.lang_ref.insert({
                    "identifier":k,
                    "labels":v["labels"],
                    "default_label": default,
                    "author_uri": ["http://data.bnf.fr/vocabulary/codelang"],
                    "date": v["date"],
                    "action": ["creation"]})
def merge_ref(db):
    ''' croisement des données depuis le normalisateur '''
    for record in db.lang_ref.find({"author_uri.0":"http://id.loc.gov/"}):
        r2 = db.lang_ref.find_one({"identifier":record["identifier"], "author_uri.0": "http://data.bnf.fr/vocabulary/codelang"})
        print(r2["default_label"]["fr"], record["default_label"]["fr"])




if __name__ == '__main__':
    conn = MongoClient()
    db = conn.ref
    # db.drop_collection("lang_ref")
    # store_ref(db)
    # store_bnf(db)
    merge_ref(db)
