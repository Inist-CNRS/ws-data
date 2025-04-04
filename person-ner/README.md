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

- Le corpus_aij_wikiner_wp3.txt (anglais) et COLNN-03 pour le modèle anglais
- Le corpus_aij_wikiner_wp3.txt (anglais) et COLNN-03 corpus_aij_wikiner_wp3.txt (Français) pour le modèle multilingue.

### Les traitements opérés sur les données

Le corpus COLNN est déjà split en train/dev/test. Les parties train et dev ont été fusionnées.
Ce n'est pas le cas des corpus WIKINER-EN et WIKINER-FR. Nous avons pris aléatoirement 20% des phrases dans les corpus wikiner que nous avons ajoutés au jeu de données `test` de COLNN03. Les codes pour séparés les données se trouvent dans le dossier `preprocess-data`

*remarque* : Tous les prétraitements des données qui suivent sont faits à la volée au début de l'entraînement du modèle.
Les jeux de données de validations sont constitués aléatoirement au début de l'entraînement : 20% des phrases sont prises du jeu de données d'entraînement pour consituer le jeux de données de validation.

De tous les labels, nous gardons que 4 labels : **O, ORG, PER, LOC.**
Les labels type **B-LOC** et **I-LOC** sont regroupés.

## Entraînement

### Codes

Les codes d'entraînement et de test des deux modèles sont :

- `./en/train.py` `./en/test.py` pour le modèle anglais.
- `./multilingual/train.py` `./multilingual/test.py` pour le modèle multilingue.

### paramètres d'entrainements

Le modèle est un BiLSTM avec une couche d'attention. Les structures des modèles sont dans le code d'entraînement.
Les réseaux sont uniquement entraînés avec Pytorch et les paramètres se trouvent aussi dans les fichiers d'entraînement.

## Résultats

### Modèle multilingues

**COLNN**

              precision    recall  f1-score   support

         LOC       0.86      0.72      0.78      1925
           O       0.98      0.98      0.98     39472
         ORG       0.65      0.82      0.73      2496
         PER       0.89      0.86      0.88      2773

    accuracy                           0.95     46666
   macro avg       0.85      0.84      0.84     46666
weighted avg       0.96      0.95      0.95     46666

**WIKINER-EN**

         LOC       0.87      0.84      0.85     24582
           O       0.99      0.99      0.99    623862
         ORG       0.81      0.77      0.79     18675
         PER       0.93      0.91      0.92     28062

    accuracy                           0.98    695181
   macro avg       0.90      0.88      0.89    695181
weighted avg       0.98      0.98      0.98    695181


**WIKINER-FR**

              precision    recall  f1-score   support

         LOC       0.91      0.85      0.88     31298
           O       0.99      0.99      0.99    634889
         ORG       0.80      0.81      0.81      8842
         PER       0.94      0.93      0.93     25513

    accuracy                           0.98    700542
   macro avg       0.91      0.90      0.90    700542
weighted avg       0.98      0.98      0.98    700542


### Modèle Anglais

**COLNN**

              precision    recall  f1-score   support

         LOC       0.82      0.77      0.80      1925
           O       0.98      0.98      0.98     39472
         ORG       0.75      0.79      0.77      2496
         PER       0.88      0.85      0.86      2773

    accuracy                           0.96     46666
   macro avg       0.86      0.85      0.85     46666
weighted avg       0.96      0.96      0.96     46666

**WIKINER**

              precision    recall  f1-score   support

         LOC       0.86      0.84      0.85     24582
           O       0.99      0.99      0.99    623862
         ORG       0.80      0.77      0.78     18675
         PER       0.91      0.90      0.91     28062

    accuracy                           0.98    695181
   macro avg       0.89      0.88      0.88    695181
weighted avg       0.98      0.98      0.98    695181