# Installer DVC

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

## Configurer le remote DVC

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

# Constitution des données d'entrainement

Le corpus initial provient d'Istex et compte `2 700 000` documents (résumé de l'article en anglais et domaine scientifique issu de la classification Science-Metrix de la revue associée). Les données sont au format csv (une colonne `txt` pour les résumés et `label` pour le domaine Science-Metrix). On a remplacé les caractères en majuscule des labels par des caractères en minuscules et on a supprimé les espaces. La colonne `id` est utilsiée comme identifiant.

## Vectorisation

Nous utilisons le modèle `Bert` pour vectoriser les résumés en faisant la moyenne des embeddings de chaque phrase. L'embedding du document est stocké dans une nouvelle colonne `vect` (un exemple est donné dans le fichier `all-data-example.csv`). Ce nom est utilisé dans les programmes python et est à remplacer par le votre.

## Passage de l'algo des KPPV

Une fois l'ensemble de ces données obtenus, nous utilisons le programme `kppv.py` pour trouver pour chaque `label` la liste ordonnées des documents ayant le plus de voisins de la même classe. Les `id` des documents pour chaque label se trouve dans le fichier `./data/{label}` et le nombre de voisin correspondant `./nb-voisin/{label}`.

## constitution des données de train/test

on utilise le script `split-train-test.py` pour obtenir le jeu de donnée d'entrainement `train.csv` et de test `test.csv`. On a besoin des dossiers `data` obtenu par kppv dans la partie précédente. Les fichiers `data-domain.csv` et `test-domain.csv` ne sont pas utilisé mais sont gardé pour d'éventuelles améliorations.

# Entraînement du modèle

## formatage pour Fasttext

On utilise `fasttext` comme classifieur. On utilise `process-train-test.py` pour les mettre au format attendu et on obtient les deux fichiers `train.txt` et `test.txt` (correspondants aux données stockées dans notre webdav, pouvant être obtenues grâce au fichier `train-test.dvc`)

## paramètres d'entrainements

On utilise ces paramètres pour l'entraînement :

```text
dim 55
ws 5
epoch 47
minCount 1
neg 5
wordNgrams 1
loss softmax
model sup
bucket 0
minn 0
maxn 0
lrUpdateRate 100
t 0.0001
```

et on obtient le modèle `model.bin`, stocké dans notre webdav, pouvant être obtenu grâce au fichier `model.dvc`

## Sélection du seuil

Pour sélectionner le seuil, le code `select-thereshold.py` est utilisé. Il permet de voir la précision du modèle et le silence en fonction du seuil.
Voici un exemple de sortie :

```text
seuil:  0.1    precision:  0.83348    silence:  1.235513603004769e-05
seuil:  0.2    precision:  0.83767    silence:  0.005856334
seuil:  0.3    precision:  0.84491    silence:  0.018372087
seuil:  0.4    precision:  0.85794    silence:  0.044947984
seuil:  0.5    precision:  0.87608    silence:  0.086757765
seuil:  0.6    precision:  0.89931    silence:  0.144975166
seuil:  0.7    precision:  0.91845    silence:  0.205589463
```

# Autres

Plusieurs disctionnaires sont enregistré format Pickle. Pour simplifier le code nous avons utilisé des identifiants pour chaque label / domaine (domaine = premier niveau de la classification, label = 3eme). Leur nom parle d'eux même. Une précision cependant :

- id_domain2domain contient pour valeur les domaines avec majuscules et espaces.
- id2label aussi.

Cela permet à l'utilisateur ou l'utilisatrice d'avoir en sortie de label correctement écrit.
