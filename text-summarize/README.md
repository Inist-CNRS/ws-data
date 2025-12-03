# text-summarize

Nous proposons ici les codes utilisés pour comparer plusieurs méthodes toutes dans le dossier `all-methods`: 

- Une méthode extractive naïve (`all-methods/extractive.py`), qui extrait les phrases les plus populaires d'un textes. Des tests ont été réaliser pour déterminer le nombre de phrases de manière automatique avec le programme `create-sentences-curves.py`
- Une méthode générative naïve (`all-methods/generative-simple.py`), qui prend uniquement en entrée les 1024 premiers tokens de l'article après suppression du résumé.
- une méthode générative (`all-methods/generative.py`), qui essauie d'étendre la méthode ci dessus au 10 000 premiers tokens par résumés successifs.
- du prompt engineering (`all-methods/prompt-generative.py`), en utilisant un modèle par inférence juste comme comparaison
- Une extraction complètement aléatoire (`all-methods/random-extractive.py`), pour avoir une fourchette minimale des métriques.

Chaque méthode génère un fichier `json` qui sert de corpus d'évaluation (contenant le gold dans un champ `y_true` et les résumés générés dans un champ `y_pred`) Nous utilisons ensuite `evaluation-methods.py` pour évaluer la méthode associée.

## Différents résultats obtenus

En cours d'élaboration.