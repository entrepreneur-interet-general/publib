# Lang API

Prototype de mise à jour automatique des référentiels de langue utilisés dans le catalogage des notices bibliographique et d'autorités
## Architecture et fonctionnement


## Référentiel officiel:

http://id.loc.gov/vocabulary/iso639-2/<lang_code>

* Collecter l'ensemble du référentiel
`build_ref()`
		# 506 codes  de langues référencés
		dans un fichier temporaire

Example:
```json
{
	"_id" : ObjectId("58d3b177dabe6e0da499fd11"),
	"identifier" : "iba",
	"label" : [
		"Iban",
		"iban",
		"Iban-Sprache"
	],
	"default_labels":{
		"en": "Iban",
		"fr": "iban",
		"de": "Iban-Sprache",
	},
	"date" : [
		ISODate("2017-03-23T12:28:55.555Z")
	],
	"uri" : "http://id.loc.gov/vocabulary/iso639-2/iba",
	"subdivision" : "",
	"id" : "21.",
	"concept_type" : "Authority",
	"vocabulary" : "ISO639-2 Languages"
}
```
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
