# Jargon BNF

## Contexte d'utilisation du Jargon
La Bibliothèque nationale de France utilise un vocabulaire interne en trigramme pour désigner ces départements, services et projets.
Ce jargon est mis à jour une fois l'an en interne et en pdf.
C'est un document très utile pour les nouveaux arrivant pour s'acculturer, "traduire"et comprendre l'organisation interne.
Mais le format actuel ne permettait pas de chercher dans le texte sous sa forme initiale 'PDF' ni d'être mis à jour facilement.

## Module
Ce module est un convertisseur de référentiel de format à format:

il gère des formats de documents:
* PDF <> DOC
* DOC <> TXT
* TXT <> CSV
* TXT <> JSON
* TXT <> HTML


et gère de conversion en *types* de données informatiques:
* TXT <> [LIST| DICT| GRAPH]
* CSV <> [LIST| DICT| GRAPH]
* JSON <> [LIST| DICT| GRAPH]

## Comment il fonctionne

Pour le moment, le module ne dispose pas d'une interface web ni d'un appel en ligne de commande.
Les méthodes sont implémentées pour permettre
en spécifiant un fichier d'entrée et un fichier de sortie de convertir dans le format désiré

## Prochaines étapes

* Appel en ligne de commande
* Interface web
* Mise à jour automatique du jargon via un CSV + cron (tache programmee)
