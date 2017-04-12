from requests_futures.sessions import FuturesSession
from pymongo import MongoClient
import pymongo
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
import csv


def detect_pagination():
    #<span class="pagination">
    pass
def store_ref(db):
    '''Write the full table of country codes from standard maintener
    inside a db
    '''
    # db.dropCollection()
    #labels de langues avec la norme iso
    default_lang = ["eng", "fre", "deu"]

    session = FuturesSession()

    urls = ["http://id.loc.gov/search/?q=cs:http://id.loc.gov/vocabulary/iso639-2&start=%i"%i for i in range(1, 541, 20)]
    conn = MongoClient()
    db = conn.ref
    db.lang_ref.create_index( [("identifier", pymongo.ASCENDING),("uri",pymongo.ASCENDING)], unique=True)

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
                doc["default_labels_lang"] =
                doc["uri"] = "http://id.loc.gov/vocabulary/iso639-2/%s" %doc["identifier"]
                doc["date"] = [dt.today()]
                doc["author_uri"] = ["http://id.loc.gov/"]
                doc["action"] =  ["creation"]
                nb_default = len(doc["labels"])
                doc["default_labels"] = dict(zip(default_lang[0:nb_default], doc["labels"][0:nb_default]))
                doc["alt_labels"]= dict(zip(default_lang[0:nb_default], []*3))
                doc["ref_name"] = "language"
                try:
                    db.lang_ref.update({"uri":doc["uri"]}, doc, upsert=True)
                    print(doc["identifier"])
                except pymongo.DuplicateKeyError:
                    pass

    for url in urls:
        future = session.get(url)
        future.add_done_callback(store_results)
def log_history(subject,action, value, author, source ):
    {
    "action": (<subject>, <action>, <value>),
    "date":ISODate("2017-04-04T12:19:26.4243Z"),
    "author":"c24b",
    "source_uri":"http://data.bnf.fr/vocabulary/lang",
    "org":"roBiNeF",
    }
    db.update(doc[_id"psuh["history"]

def add_new_id(code, ):
    doc = {
        "identifier": <code>


        #full list of labels list not sorted by lang
        "labels":[

        ],
        referential :{"name":'lang'
                      "standard":"ISO639-2"
                      "source_uri":http://id.loc.gov/vocabulary/iso639-2
                      "maintainer":< org officialy in charge code>
                      "author": <username in charge>
                      "organisation": <BNF|Official Maintainer>
                      "type":<code|list>
      },
      usages: [<zone>$<sszone>P<pos>,
                <zone>$<sszone>P<pos>,
      ],
      rules:[

      ],
      "default_label" : {
        "fre" : "",
        "eng" : "",
        "deu" : ""
      },
      "alt_labels": {
        "fre": [, , ],
        "eng":[],
        "deu":[],
      }

      }


def update_code():
    ref= {"concept_type":data["concept_type"],
            "history":data["history"],
            "subdivision" : "",
            "labels":[],
            "ref_name" : "language",
            "default_label" : {
              "fre" : "",
              "eng" : "",
              "deu" : ""
            },
            "alt_labels": {
              "fre": [, , ],
              "eng":[],
              "deu":[],
            }
            "id" : "",
        }
            }

def merge_bnf():
    ''' le référentiel de la BNF est structuré ainsi
    code_lang libellé (=> renvoi vers la forme canonique)
    on fait donc un prétraitement qui consiste
    a mapper
    '''
    ref = {}
    with open("./data/code_lang_BNF.csv", "r", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            code = row["code"]
            labels = row['Libellé'].replace(".", "",).split(" => ")
            if len(labels) > 1:
                alt_label_fr, d_label_fr = labels
            else:
                d_label_fr = labels

            doc = db.lang_ref.find_one({"identifier": code})

            if doc is not None:
                #verifier le libellé par défault
                if d_label_fr != doc["default_labels"]["fre"]:
                    #remplacer le label par défault
                    db.lang_ref.update({"_id":doc["_id"]}, "$set":{"default_labels.fre": d_label_fr})
                    #logger le changement
                    #db.lang_ref.update({"_id":doc["_id"]}, "$push":{"history": {"when": dt.now(), "author": "c24b", "org", "what":"'default_labels.fre': '%s'}})


                #update
            else:
                #create

def build_bnf():
    '''mise à jour du référentiel officiel avec les valeurs propres à la BNF référentiel de la BNF
    en partant pour le moment du fichier csv exporté de la documentation du catalogueur
    {"fre":[Label1, Label2, Label3, ...]}
    '''
    ref = {}
    with open("./data/code_lang_BNF.csv", "r", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            labels = row['Libellé'].replace(".", "",).split(" => ")
            default_label = labels[-1]
            try:
                exists = db.lang_ref.find_one({"identifier": row["Code"]})
                if exists is None:
                    print(row["Code"], "not found")
                else:
                    print (found")
                    if exists["default_label"]["fre"] == default_label:
                        #update values
                        print("ok")
                        db.lang_ref.udpate({"_id": exists["_id"]},
                                                {"$push":{  "alt_labels.fre":{"$each":labels},
                                                            "action": "added alt_labels",
                                                            "date": dt.now(),
                                                            "author_uri": "http://data.bnf.fr/vocabulary/lang",
                                                            }
                                                })

                    else :
                        print(exists["default_label"]["fre"],default_label)


                # print(exists["labels"])
                # print(row["Code"], labels)
                # print(exists)
            except Exception as e:
                print(e)

                print("Not found")
                # print(row["Code"], labels)

            #     #     ref[row["Code"]] = {"default_label":{"fr": default}}
            # try:
            #     ref[row["Code"]]["labels"].append(labels[0])
            #     if len(labels) > 1:
            #         ref[row["Code"]]["default_label"] = {"fr":labels[1]}
            #
            # except KeyError:
            #     ref[row["Code"]]= {"labels":[labels[0]]}
            #     if len(labels) > 1:
            #         ref[row["Code"]]["default_label"] = {"fr":labels[1]}
            # ref[row["Code"]]["date"] = [dt.now()]
    return ref

# def store_bnf(db):
#     '''stocker le referentiel dans une BDD
#     pour une première fois action: creation
#     '''
#     ref = build_bnf()
#     conn = MongoClient()
#     db = conn.ref
#     for k, v in ref.items():
#         try:
#             default = v["default_label"]
#         except KeyError:
#             default = {"fr":None}
#         db.bnf_ref.insert({
#                     "identifier":k,
#                     "labels":v["labels"],
#                     "default_label": default,
#                     "author_uri": ["http://data.bnf.fr/vocabulary/codelang"],
#                     "date": v["date"],
#                     "action": ["creation"]})
# def merge_ref(db):
#     ''' croisement des données depuis le normalisateur '''
#     for record in db.lang_ref.find({"author_uri.0":"http://id.loc.gov/"}):
#         r2 = db.lang_ref.find_one({"identifier":record["identifier"], "author_uri.0": "http://data.bnf.fr/vocabulary/codelang"})
#         print(r2["default_label"]["fr"], record["default_label"]["fr"])




if __name__ == '__main__':
    conn = MongoClient()
    db = conn.ref
    # db.drop_collection("lang_ref")
    # store_ref(db)
    build_bnf()
    # store_bnf(db)
    # merge_ref(db)
