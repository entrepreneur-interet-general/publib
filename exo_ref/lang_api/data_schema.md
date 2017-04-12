## Référentiel de langues

Un format commun pour les référentiels de la BNF

doc = {
    "identifier": <code>
    "history":[
                {

                "action": (<subject>, <action>, <value>),
                "date":ISODate("2017-04-04T12:19:26.4243Z"),
                "author":"c24b",
                "source_uri":"http://data.bnf.fr/vocabulary/lang",
                "org":"roBiNeF",
                },
                {
                "action": "updated",
                "scope": "default_label.fr",
                "date":ISODate("2017-04-04T12:19:26.4243Z"),
                "author":"c24b",
                "source_uri":"http://id.loc.gov/vocabulary/iso639-2",
                "org":"roBiNeF",
                "version":1
                },
                {
                  "action": "created",
                  "scope": ""
                  "date":ISODate("2017-04-04T12:18:19.524Z"),
                  "author":"c24b",
                  "org":"roBiNeF",
                  "source_uri":"http://id.loc.gov/vocabulary/iso639-2",
                  "version":0
                 },
                ]

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
