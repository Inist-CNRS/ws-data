# entraînement du modèle d'entityTag

## DVC

Pour installer DVC, il est conseillé de créer un environnement virtuel.

```bash
python3 -m venv .venv/
```

Pour activer :

```bash
source .venv/bin/activate
```

Les commandes pour installer dvc sont :

```bash
pip install -r requirements.txt
```

### Configurer le remote DVC

Dans le .env mettre les trois lignes suivantes :

```bash
export WEBDAV_URL=webdav://????????
export WEBDAV_LOGIN=????
export WEBDAV_PASSWORD=?????
```

Pour configurer le remote DVC :

```bash
source .env
dvc init --subdir
dvc remote add --local -d origin $WEBDAV_URL
dvc remote modify --local origin user $WEBDAV_LOGIN
dvc remote modify --local origin password $WEBDAV_PASSWORD
dvc config core.autostage true
```

Pour envoyer un fichier de plus de 500M :

- Mettre le fichier dans un répertoire
- Découper le fichier avec `split -b 500m nom_du_fichier`
- Faire un `dvc add répertoire`
- `dvc push répertoire.dvc`

## Les données d'entraînement

### Les données

Pour obtenir les données d'entraînement au bon format, il faut récupérer les données sur le github [softcite_dataset](https://github.com/softcite/softcite_dataset_v2/tree/master/json).

### Les traitements opérés sur les données

Une fois fait, on lance le code `formate-data.py` pour obtenir le jeu de donnée train et test au format requis par Flair. On obtient ainsi les jeux de données de train `softcite-data-conll-train.txt` et de test `softcite-data-conll-test.txt`.
Seul le label qui nous intéresse est gardé.

## Entraînement

### Codes

Le code pour entraîner le modèle à partir des jeux de données obtenus ci-dessus est `train-flair.py`. 

### paramètres d'entrainements

Le modèle est RNN-BiLSTM utilisant les embeddings Flair (calculés par stack de trois types d'embedding - normaux, backward et forward, calculés à partir de Glove). La structure du modèle et les paramètres d'entraînement sont explicités dans le code d'entraînement. Le modèle a été entraîné avec la version `0.15.1` de `Flair`.

## Résultats

Précision : `0.8631`
Rappel : `0.6453`
F-mesure : `0.7385`
