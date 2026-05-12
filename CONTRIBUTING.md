# Pour contribuer

## Répertoire

Quel que soit le travail à faire, il se fait dans un répertoire sous la racine
du dépôt.

S'il n'existe pas encore il faut le créer (nous l'appellerons `repertoire` dans
la suite de ce document).  
Idéalement il doit correspondre au nom du web service pour lequel on crée les
données.  

Chaque répertoire dispose de son propre environnement virtuel python.  
Cela permet d'avoir un version de DVC à jour quand on crée un nouveau
répertoire, et de ne pas avoir de conflit avec les autres répertoires pour les
dépendances python / node à utiliser pour traiter les données.  

## Installer DVC

Ne pas oublier de se déplacer dans le répertoire de travail:

```bash
cd repertoire
```

Pour installer DVC, il faut créer un environnement virtuel.

```bash
python3 -m venv .venv/
```

Pour activer :

```bash
source .venv/bin/activate
```

Les commandes pour installer dvc sont :

```bash
pip install wheel
pip install dvc[webdav]
```

Pour rendre les traitements reproductibles, on fige les dépendances dans le
fichier `requirements.txt`:

```bash
pip freeze > requirements.txt
```

Ainsi, lorsqu'on récupère le dépôt sur une autre machine, il suffit pour
installer les dépendances python de faire:

```bash
pip install -r requirements.txt
```

### Configurer le remote DVC

Dans un fichier `.env` dans `repertoire` mettre les trois lignes suivantes (à
compléter avec vos données personnelles):

```bash
export WEBDAV_URL=webdav://????????
export WEBDAV_LOGIN=????
export WEBDAV_PASSWORD=?????
```

Pour configurer le remote DVC (ça ne se fait qu'une fois):

```bash
source .env
dvc init --subdir
dvc remote add --local -d origin $WEBDAV_URL
dvc remote modify --local origin user $WEBDAV_LOGIN
dvc remote modify --local origin password $WEBDAV_PASSWORD
dvc config core.autostage true
```

### Envoyer un répertoire

On peut être dans le cas où on a plusieurs fichiers à envoyer (par exemple
plusieurs modèles, comme dans
[openalex-classification](./openalex-classification/)).

Mettons que ces fichiers soient rassemblés dans le répertoire `models`.

Pour envoyer le contenu de tout le répertoire sur le *remote* DVC:

```bash
dvc add models
dvc push models.dvc
```

### Envoyer un fichier

Pour envoyer un fichier unique, on procède comme pour un répertoire.

Mettons que ce fichier se nomme `file`.

```bash
dvc add file
dvc push file.dvc
```

> [!WARNING]  
> Pour envoyer un fichier de plus de 500M :
>
> - Mettre le fichier dans un répertoire nommé `data`
> - Découper le fichier avec `split -b 500m nom_du_fichier`
> - Faire un `dvc add data`
> - `dvc push data.dvc`

### Récupération du fichier du côté des web services

Voir [CONTRIBUTING.md](https://github.com/Inist-CNRS/web-services/blob/main/CONTRIBUTING.md#utilisation-de-dvc-pour-charger-des-donn%C3%A9es-ou-des-mod%C3%A8les).  
Voir le [Dockerfile de sciencemetrix-classification](https://github.com/Inist-CNRS/web-services/blob/f9f96827233239b4bb98add3a12fe85aad6ac61d/services/sciencemetrix-classification/Dockerfile#L14).  
