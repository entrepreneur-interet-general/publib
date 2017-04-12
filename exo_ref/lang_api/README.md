# Lang API

Prototype de mise à jour automatique des référentiels de langue utilisés dans le catalogage des notices bibliographique et d'autorités.

* Collecte initiale de la base depuis le référentiel officiel
* Mise à jour de la base a partir du référentiel BNF
* Système de publication des modifications (CRON ==> RSS?)
* Controle et vérification via une API



## Référentiel officiel:

	http://id.loc.gov/vocabulary/iso639-2/<lang_code>

* Collecter l'ensemble du référentiel

`store_ref.build_ref()`


506 codes  de langues référencés uniques (uri, identifier)
dans la base de données `ref` et la table `lang_ref`
structuré ainsi:
```json
{
	"_id" : ObjectId("58e372eb4f1b1c2f0b4f5409"),
	"concept_type" : "Authority",
	"action" : [
		"creation"
	],
	"subdivision" : "",
	"ref_name" : "language",
	"label" : "Munda languages | mounda, langues | Mundasprachen (Andere)",
	"default_label" : {
		"fr" : "mounda, langues",
		"en" : "Munda languages",
		"de" : "Mundasprachen (Andere)"
	},
	"uri" : "http://id.loc.gov/vocabulary/iso639-2/mun",
	"id" : "1.",
	"identifier" : "mun",
	"author_uri" : [
		"http://id.loc.gov/"
	],
	"vocabulary" : "ISO639-2 Languages",
	"labels" : [
		"Munda languages",
		"mounda, langues",
		"Mundasprachen (Andere)"
	],
	"date" : [
		ISODate("2017-04-04T12:18:19.524Z")
	]
}
```
* Ajouter les référentiels et renvois de la BNF
`store_ref.build_ref()`

* Recherche d'un label langue dans le référentiel `search_label(code, [lang="fr"])`
* Recherche d'un code pour un label
`search_code(code, [lang="fr"])`

## Référentiel BNF
* Collecter l'ensemble du référentiel BNF `build_bnf()`

	# 495 codes pays référencés
	dans une base temporaire
* Rechercher un ou plusieurs labels par code `search_labels()`
* Rechercher la forme retenue par code `search_default_label()`
* Rechercher le code par son nom
`search_code()`

## Mise à jour du référentiel BNF

* Ajouter les référentiels manquants
* Marquer les valeurs par défault de la BNF comme prioritaire

 # Country Codes API
 http://data.bnf.fr/vocabulary/countrycodes/
